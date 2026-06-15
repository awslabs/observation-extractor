# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch, MagicMock

from observation_extractor.model.observations import Observation, Thought
from observation_extractor.writers import dynamodb as ddb_writer


def make_observation(title='t', question_number=1):
    thought = Thought(
        title=title,
        document_date=None,
        document_type='d',
        description='desc',
        evidence='ev',
        question_number=question_number,
        question='q',
    )
    return Observation(thought=thought, metadata={'question_set': 'qs'})


def test_write_observations_skips_non_observation_elements():
    good = make_observation('keep')
    bad_list = [make_observation('nested')]
    bad_none = None

    with patch.object(ddb_writer, 'write_observation') as mock_write:
        mock_write.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        results = ddb_writer.write_observations(
            case_id='c1',
            observations=[bad_list, good, bad_none],
            table='t',
        )

    assert mock_write.call_count == 1
    assert mock_write.call_args.kwargs['observation'] is good
    assert len(results) == 1


def test_write_observations_empty_list():
    with patch.object(ddb_writer, 'write_observation') as mock_write:
        results = ddb_writer.write_observations(case_id='c1', observations=[], table='t')
    assert results == []
    mock_write.assert_not_called()
