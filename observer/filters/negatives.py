import instructor
from litellm import completion

from observer.model.observations import Observation
from observer.model.boolean import Boolean


def is_negative_observation(observation: Observation, verbose=False):
    # checks if this is a negative observation
    if verbose:
        print(f"Applying filter to {observation}")

    prompt = f"""You are part of a data extraction process. Your role is to filter out negative observations that simply
state that something was not found. 

Here are examples that you should filter:
- The document does not provide any information on vital signs like pulse, blood pressure, temperature, or heart rate.
- The medical record does not contain any information indicating whether the patient shows signs of substance dependency or not.
- The document does not mention any x-rays being performed or their results.

Return True to filter out an observation. Return False to allow the observation to pass through.

{observation}
"""

    message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            }
        ]
    }

    client = instructor.from_litellm(completion)
    resp = client.messages.create(
        model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
        max_tokens=1024,
        messages=[message],
        response_model=Boolean,
    )
    if verbose:
        print(f"Filter response: {resp}")
    return resp.result

def filter_negative_observations(observations: list[Observation]):
    '''Filters out negative observations
    ie: the report does not indicate an answer to this question'''

    return [obs for obs in observations if not is_negative_observation(obs)]






