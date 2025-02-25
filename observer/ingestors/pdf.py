# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
from pdf2image import convert_from_path
import base64
from io import BytesIO
from datetime import datetime

from pypdf import PdfReader
from litellm import completion
import instructor

from observer.model.observations import Observation, Thought, Observations, Thoughts


def get_prompt(questions, verbose=False):
    """
    Generate a prompt for the Claude model based on the given questions.

    Args:
        questions (list): List of questions to be included in the prompt.

    Returns:
        str: The generated prompt.
    """
    questions = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    prompt = f"""Process the document to return required fields if available. 

Output a list of Thoughts in the specified format based on these questions. If a thought is not aligned with one of these, discard it.

Use these questions as a guide to find relevant information from the <PageText> and page image.
<questions>
{questions}
</questions>

Use the description field to describe what you found.

Use the evidence field to provide a direct quote from the document. 

Use the question field to indicate which question this thought relates to.

If you cannot find a field value in the reference document, omit the field. Don't speculate. Be concise.

The correct response is an empty list [] if none of the needed fields are in the reference document. If there is no relevant data, return an empty list.

use your <thinking></thinking> space to note your observations and then output them in the specified format."""

    if verbose:
        print(f"PROMPT: {prompt}")

    return prompt

def get_text_pages(pdf_path):
    """
    Get the text content of each page in a PDF file.

    Args:
    :param pdf_path: the path to a padf file
    :return: list[str]
    """
    reader = PdfReader(pdf_path)
    page_texts = [page.extract_text() for page in reader.pages]
    return page_texts

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

        # Get the page texts
        page_texts: list[str] = get_text_pages(pdf_path)

        # Process each page
        for idx, image in enumerate(images):
            # prompt_text = f"Citation Page: {idx}"

            # Convert PIL Image to PNG bytes
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            png_bytes = buffer.getvalue()

            # Convert to base64
            base64_image = base64.b64encode(png_bytes).decode('utf-8')

            page_text = page_texts[idx]
            # print(f"{idx} - \n{page_text}")

            # Create message in Bedrock API format
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"<PageText>{page_text}</PageText>"
                    },
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
    """
    Ingest a PDF file into the system.
    :param input_file_path: path to local input file
    :param questions: the question set to apply to the file
    :param metadata: metadata that will be added to each observation
    :param verbose: enable verbose logging
    :return:
    """
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
        page_metadata['page_number'] = idx + 1 # start numbering at page 1
        print(f"Processing page: {idx + 1}")
        try:
            resp = client.messages.create(
                model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
                max_tokens=1024,
                messages=[page_message],
                response_model=Thoughts,
            )

            # for thought in resp:
            # print(resp)
            thoughts = resp.thoughts
            # print(f"Thoughts: {thoughts}")
            new_observations = [Observation(thought=thought, metadata=page_metadata) for thought in thoughts]
            print(new_observations)
            observations.extend(new_observations)
        except Exception as e:
            print(f"Exception processing page: {idx} of {input_file_path}")
            print(f"Exception: {e}")

    return observations