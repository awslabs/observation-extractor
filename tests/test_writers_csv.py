# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import csv

import pytest

from observation_extractor.model.observations import Observation, Thought
from observation_extractor.writers.csv import write_observations_to_csv


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


def read_csv_rows(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def test_writes_observations(tmp_path):
    out = tmp_path / "out.csv"
    write_observations_to_csv([make_observation('a'), make_observation('b')], str(out))
    rows = read_csv_rows(out)
    assert [r['title'] for r in rows] == ['a', 'b']


def test_empty_list_does_not_crash(tmp_path):
    out = tmp_path / "out.csv"
    write_observations_to_csv([], str(out))
    # No file written, but no exception either
    assert not out.exists()


def test_skips_list_element(tmp_path):
    """The 'append-instead-of-extend' shape: a list nested as an element."""
    out = tmp_path / "out.csv"
    good = make_observation('keep')
    bad = [make_observation('nested'), make_observation('also nested')]
    write_observations_to_csv([bad, good], str(out))
    rows = read_csv_rows(out)
    assert [r['title'] for r in rows] == ['keep']


def test_skips_none_element(tmp_path):
    out = tmp_path / "out.csv"
    write_observations_to_csv([None, make_observation('keep'), None], str(out))
    rows = read_csv_rows(out)
    assert [r['title'] for r in rows] == ['keep']


def test_all_invalid_does_not_crash(tmp_path):
    out = tmp_path / "out.csv"
    write_observations_to_csv([None, [make_observation()]], str(out))
    assert not out.exists()
