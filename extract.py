"""Extract data from CSV and JSON infiles.

Extract data on near-Earth objects and close approaches from CSV
and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted
as described in the project instructions, into a collection of
`NearEarthObject`s.

The `load_approaches` function extracts close approach data from a
JSON file, formatted as described in the project instructions, into
a collection of `CloseApproach` objects.

The main module calls these functions with the arguments provided at
the command line, and uses the resulting collections to build an
`NEODatabase`.
"""
import csv
import json

import pandas as pd

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path='./data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about
    near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Create dataframe with select CSV columns:
    select_columns = ['pdes', 'name', 'pha', 'diameter']
    csv_dataframe = pd.read_csv(neo_csv_path,
                                usecols=select_columns,
                                low_memory=False)
    # Create temporary CSV file of select data:
    select_csv = csv_dataframe.to_csv('./data/csv_select.csv', index=False)
    # Extract only select data:
    with open('./data/csv_select.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
    # Generate and return neo collection with constructor:
        neo_coll = [NearEarthObject(**row) for row in csv_reader]
        return neo_coll


def load_approaches(cad_json_path='./data/cad.json'):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about
    close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # Create list of JSON dictionaries of all data (including extraneous):
    with open(cad_json_path, 'r') as json_file:
        json_data = json.load(json_file)
        json_listofdicts = [
            dict(zip(json_data['fields'], data))
            for data in json_data['data']
        ]
    # Filter out extraneous data fields:
        select_fields = ['des', 'cd', 'dist', 'v_rel']
        filtered_dict_list = [
            dict((k, d[k]) for k in select_fields if k in d)
            for d in json_listofdicts
        ]
    # Create temporary CSV file of select fields:
    keys = filtered_dict_list[0].keys()
    with open('./data/json_select.csv', 'w') as csv_out:
        csv_writer = csv.DictWriter(csv_out, fieldnames=keys)
        csv_writer.writeheader()
        csv_writer.writerows(filtered_dict_list)
    # Extract only select data:
    with open('./data/json_select.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
    # Return approach collection with constructor:
        approach_coll = [CloseApproach(**row) for row in csv_reader]
        return approach_coll


if __name__ == '__main__':
    print(f"First Module's Name: {__name__}\n")
