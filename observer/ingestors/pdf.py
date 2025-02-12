import os

from datetime import datetime
from litellm import completion
import instructor

from pdf2image import convert_from_path
from pydantic import BaseModel
import base64
from io import BytesIO
import json

from observer.model.observations import Observation, Thought, Observations, Thoughts

def get_prompt(questions, verbose=False):
    prompt = f"""Process the document to return required fields if available. 

Output a list of Thoughts in the specified format based on these questions. If a thought is not aligned with one of these, discard it.
{questions}

Use the description field to describe what you found.

Use the evidence field to provide a direct quote from the document. 

Use the question field to indicate which question this thought relates to.

If you cannot find a field value in the reference document, omit the field. Don't speculate. Be concise.

The correct response is an empty list [] if none of the needed fields are in the reference document. If there is no relevant data, return an empty list.

use your <thinking></thinking> space to note your observations and then output them in the specified format."""

    if verbose:
        print(f"PROMPT: {prompt}")

    return prompt


def pdf_to_messages(pdf_path, prompt):
    """
    Convert a PDF file to a list of Claude API-formatted messages for AWS Bedrock,
    where each message contains one page of the PDF as a PNG image.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        list: List of messages in Bedrock API format

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: For other errors during conversion
    """
    try:
        # Check if file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Convert PDF to list of images
        images = convert_from_path(pdf_path)

        # Create messages list for each page
        messages = []

        # Process each page
        for idx, image in enumerate(images):
            prompt_text = f"Citation Page: {idx}"

            # Convert PIL Image to PNG bytes
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            png_bytes = buffer.getvalue()

            # Convert to base64
            base64_image = base64.b64encode(png_bytes).decode('utf-8')

            # Create message in Bedrock API format
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
            messages.append(message)

        return messages

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error converting PDF: {str(e)}")

def ingest_pdf(input_file_path, questions, metadata={}, verbose=False):
    print(f"Ingesting pdf file at {input_file_path}")
    prompt = get_prompt(questions, verbose)

    # metadata['something_else'] = 'a value for that extra field'
    metadata['timestamp'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    metadata['input_file'] = input_file_path

    page_messages = pdf_to_messages(input_file_path, prompt=get_prompt(questions, verbose))

    observations = []
    for idx, page_message in enumerate(page_messages):
        client = instructor.from_litellm(completion)
        page_metadata = metadata.copy()
        page_metadata['page_number'] = idx + 1 # start at page 1

        resp = client.messages.create(
            model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
            max_tokens=1024,
            messages=[page_message, ],
            response_model=Thoughts, # todo: these should be thoughts so we can add metadata
        )

        # for thought in resp:
        print(resp)
        thoughts = resp.thoughts
        print(f"Thoughts: {thoughts}")
        new_observations = [Observation(thought=thought, metadata=page_metadata) for thought in thoughts]
        print(new_observations)
        observations.extend(new_observations)

    return observations