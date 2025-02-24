# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import shortuuid
import json
from boto3.dynamodb.conditions import Key
import boto3

from observer.model.observations import Observation


def write_to_ddb(item, table):
    """
    Writes an item to Amazon DynamoDB
    :param item: The item to write
    :param table: The table name to write it to
    :return: response
    """
    table_client = boto3.resource('dynamodb').Table(table)
    response = table_client.put_item(Item=item)
    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        raise Exception("Error writing to DDB")
    return response

def get_item_by_key(pk, sk, table):
    """
    Gets an item from Amazon DynamoDB using its key
    :param pk: primary key
    :param sk: sort key
    :param table: table name
    :return: response
    """
    return table.get_item(Key={'pk': pk, 'sk': sk})

def get_observation(case_id, observation_id, table):
    """
    Gets an observation from Amazon DynamoDB by its key
    :param case_id: case identifier
    :param observation_id: observation identifier
    :param table: table name
    :return: Observation
    """
    pk = f"C#{case_id}#"
    sk = f"O#{observation_id}#"
    return get_item_by_key(pk, sk, table)

def write_observation(case_id, observation: Observation, table: str):
    """
    Write an observation to DynamoDB
    :param case_id: case identifier
    :param observation: Observation
    :param table: table name
    :return: response
    """
    observation_id = shortuuid.uuid()
    data = json.dumps(observation.to_dict())
    return write_to_ddb(
        item={
            "pk": f"C#{case_id}#",
            "sk": f"O#{observation.metadata['question_set']}#{str(observation.thought.question_number)}#{observation_id}#",
            "ddate": f"{observation.thought.document_date}",
            'qs': f"{observation.metadata['question_set']}",
            "qn": str(observation.thought.question_number),
            "data": data
        },
        table=table
    )

def write_observations(case_id, observations: list[Observation], table: str):
    """
    Writes a list of observations to Amazon DynamoDB
    :param case_id: case identifier
    :param observations: list of observations
    :param table: table name
    :return: responses
    """
    results = [write_observation(case_id, observation=observation, table=table) for observation in observations]
    return results

