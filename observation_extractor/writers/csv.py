# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import csv

from observation_extractor.model.observations import Observation

def write_observations_to_csv(observations: list[Observation], outfile_path: str):
    """
    Writes a list of observations to a local csv file
    :param observations: list[Observations]
    :param outfile_path: output file path
    :return: keys
    """
    print(f"Writing output to {outfile_path}")

    observation_dicts = []
    for i, o in enumerate(observations):
        if not isinstance(o, Observation):
            print(f"Skipping element at index {i}: expected Observation, got {type(o).__name__}")
            continue
        observation_dicts.append(o.to_dict())

    if not observation_dicts:
        print(f"No observations to write to {outfile_path}")
        return

    keys = observation_dicts[0].keys()
    with open(outfile_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(observation_dicts)