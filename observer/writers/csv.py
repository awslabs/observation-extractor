import csv

from observer.model.observations import Observation

def write_observations_to_csv(observations: list[Observation], outfile_path: str):
    print(f"Writing output to {outfile_path}")
    keys = observations[0].keys()
    with open(outfile_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(observations)
    # todo: implement this