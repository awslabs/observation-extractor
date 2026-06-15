# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import instructor
from litellm import completion

from observation_extractor.config import MODEL, MAX_TOKENS
from observation_extractor.model.observations import Observation
from observation_extractor.model.boolean import Boolean


def is_negative_observation(observation: Observation, is_retry=False, verbose=False):
    """
    Returns True for observations that a datapoint was not in the incoming data.
    :param observation:
    :param is_retry:
    :param verbose:
    :return:
    """
    # checks if this is a negative observation
    if verbose:
        print(f"Applying filter to {observation}")

    prompt = f"""You are part of a data extraction process. Your role is to filter out negative observations that simply
state that something was not found. 

Here are examples that you should filter:
- The document does not provide any information on vital signs like pulse, blood pressure, temperature, or heart rate.
- The medical record does not contain any information indicating whether the patient shows signs of substance dependency or not.
- The document does not mention any x-rays being performed or their results.

Return true to filter out an observation. Return false to allow the observation to pass through.

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

    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[message],
            response_model=Boolean,
        )
        if verbose:
            print(f"Filter response: {resp}")
        return resp.result
    except Exception as e:
        print(f"Encountered exception: {e}...retrying once")
        if not is_retry:
            is_negative_observation(observation, is_retry=True, verbose=True)


def filter_negative_observations(observations: list[Observation]):
    """
    Filters out negative observations from a list of observations.
    :param observations: list[Observation]
    :return: list[Bool]
    """
    return [obs for obs in observations if not (obs is None or is_negative_observation(obs))]






