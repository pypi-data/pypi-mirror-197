"""
Utility functions for accessing, reading, subsetting analyzing NASA Earth data with a focus on PO.DAAC data.
These functions are wrappers of the basic tools.
"""

import requests
from pprint import pprint
CMR_OPS = 'https://cmr.earthdata.nasa.gov/search'
collection_url = 'https://cmr.earthdata.nasa.gov/search/collections'
var_url = "https://cmr.earthdata.nasa.gov/search/variables"

def find_dataset(provider='podaac',
                 keywords=['swot','level-2']):
    """
    Find a list of collections/datasets that match all the keywords from the keywords list.
    
    
    """
    
    if 'podaac' in provider.lower().replace('.',''):
        provider='POCLOUD'
        
    response = requests.get(collection_url,params={'cloud_hosted': 'True',
                                        'has_granules': 'True',
                                        'provider': provider,
                                        'page_size':2000,},
                                headers={'Accept': 'application/json', } )
    
    collections = response.json()['feed']['entry']
    
    entries=[]
    for collection in collections:
        
        title=f'{collection["dataset_id"]} {collection["id"]}'
        match=1
        for kw in keywords:
            match *= kw.lower() in title.lower()
            
        if match==1:
            print(title)
            entries.append({'short_name':collection["dataset_id"],
                            'concept_id':collection["id"]})
    
    
    return entries

def find_data_files(concept_id,provider='podaac'):
    
    return


def find_variables(concept_id,provider='podaac'):
    var_response = requests.get(var_url,params={'concept_id': concept_id,},
                            headers={'Accept': 'application/vnd.nasa.cmr.umm_results+json'})
    var_response = var_response.json()
    print(var_response)
    #var_list.append(var_response['items'][0]['umm']['Name'])
    return