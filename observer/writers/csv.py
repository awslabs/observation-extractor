import csv

from observer.model.observations import Observation

def write_observations_to_csv(observations: list[Observation], outfile_path: str):
    print(f"Writing output to {outfile_path}")

    observaction_dicts = [o.to_dict() for o in observations]
    keys = observaction_dicts[0].keys()

    with open(outfile_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(observaction_dicts)