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

    observation_dicts = [o.to_dict() for o in observations]
    keys = observation_dicts[0].keys()

    with open(outfile_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(observation_dicts)