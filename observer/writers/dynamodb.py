import shortuuid
import json
from boto3.dynamodb.conditions import Key
import boto3

from observer.model.observations import Observation


def write_to_ddb(item, table):
    table_client = boto3.resource('dynamodb').Table(table)
    response = table_client.put_item(Item=item)
    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        raise Exception("Error writing to DDB")
    return response

def get_item_by_key(pk, sk, table):
    return table.get_item(Key={'pk': pk, 'sk': sk})

def get_observation(case_id, observation_id, table):
    pk = f"C#{case_id}#"
    sk = f"O#{observation_id}#"
    return get_item_by_key(pk, sk, table)

def write_observation(case_id, observation: Observation, table: str):
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
    results = [write_observation(case_id, observation=observation, table=table) for observation in observations]
    return results

