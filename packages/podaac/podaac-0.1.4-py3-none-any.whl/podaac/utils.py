"""
Utility functions for accessing, reading, subsetting analyzing NASA Earth data with a focus on PO.DAAC data.
These functions are wrappers of the Earthdata basic tools.
"""
import requests
from pprint import pprint

CMR_OPS = 'https://cmr.earthdata.nasa.gov/search'
collection_url = 'https://cmr.earthdata.nasa.gov/search/collections'
var_url = "https://cmr.earthdata.nasa.gov/search/variables"

def find_dataset(provider='podaac', keywords=['swot', 'level-2']):
    """
    Find a list of collections/datasets that match all the keywords from the keywords list.

    Args:
        provider (str): Name of the provider. Default is 'podaac'.
        keywords (list): List of keywords to match. Default is ['swot', 'level-2'].

    Returns:
        list: A list of dictionaries containing the short_name and concept_id for each matching collection/dataset.
    """
    if 'podaac' in provider.lower().replace('.', ''):
        provider = 'POCLOUD'

    response = requests.get(collection_url, params={
        'cloud_hosted': 'True',
        'has_granules': 'True',
        'provider': provider,
        'page_size': 2000,
    }, headers={'Accept': 'application/json', })

    collections = response.json()['feed']['entry']

    entries = []
    for collection in collections:
        title = f'{collection["dataset_id"]} {collection["id"]}'
        match = 1
        for kw in keywords:
            match *= kw.lower() in title.lower()

        if match == 1:
            print(title)
            entries.append({'short_name': collection["dataset_id"],
                            'concept_id': collection["id"]})

    return entries


def find_data_files(concept_id, provider='podaac'):
    # TODO: Implement this function
    return


def find_variables(concept_id, provider='podaac'):
    """
    Find a list of variables associated with a collection/dataset.

    Args:
        concept_id (str): The concept ID of the collection/dataset.
        provider (str): Name of the provider. Default is 'podaac'.

    Returns:
        None
    """
    var_response = requests.get(var_url, params={
        'concept_id': concept_id,
    }, headers={'Accept': 'application/vnd.nasa.cmr.umm_results+json'})

    var_response = var_response.json()
    print(var_response)
    # var_list.append(var_response['items'][0]['umm']['Name'])
    return

import requests
import s3fs

def get_ready4S3(provider='podaac'):
    """
    Returns an S3FileSystem object that is ready to interact with NASA's PO.DAAC or LP.DAAC AWS S3 storage services.

    Args:
        provider (str): The data provider to get credentials for. Must be either 'podaac' (default) or 'lpdaac'.

    Returns:
        s3fs.core.S3FileSystem: An S3FileSystem object that is ready to interact with the provider's AWS S3 storage service.
    """

    s3_cred_endpoint = {
        'podaac': 'https://archive.podaac.earthdata.nasa.gov/s3credentials',
        'lpdaac': 'https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials'
    }

    temp_creds_url = s3_cred_endpoint[provider]
    creds = requests.get(temp_creds_url).json()
    s3 = s3fs.S3FileSystem(anon=False,
                           key=creds['accessKeyId'],
                           secret=creds['secretAccessKey'],
                           token=creds['sessionToken'])
    return s3
