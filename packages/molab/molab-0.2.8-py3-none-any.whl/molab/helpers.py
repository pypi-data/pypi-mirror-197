import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time
from morpheuscypher import Cypher

def _get_instance_ids_from_names(url,headers,names:list):
    """
    The _get_instance_ids_from_names function accepts a list of names and returns a list of instance IDs.
    It does this by making an API call to the AS API for each name in the provided list, and then returning
    the ID from that response.
    
    :param url: Specify the url of the instance
    :param headers: Pass the api key to the _get_instance_ids_from_names function
    :param names:list: Pass a list of names to the _get_instance_ids_from_names function
    :return: A list of instance ids based on a list of names
    :doc-author: Trelent
    """
    session = FuturesSession()
    endpoint = "/api/instances"
    ids = []
    futures=[session.get(f'{url}{endpoint}?name={n}',headers=headers,verify=False) for n in names]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            i = resp.json()["instances"][0]
            ids.append(i["id"])
    return(ids)

def _get_morpheus_license_from_cypher(url,token,cypher_name):
    """
    The _get_morpheus_license_from_cypher function is a helper function that retrieves the Morpheus License from the Cypher
    database.  It accepts three parameters: url, token, and cypher_name.  The url parameter is required for making an API call to
    the Morpheus service.  The token parameter is required for making an API call to the Morpheus service.  The cypher_name
    parameter specifies which Cypher query will be used in order to retrieve license information from the database.
    
    :param url: Specify the morpheus api url
    :param token: Authenticate the user to morpheus
    :param cypher_name: Specify which cypher query to run
    :return: The license information from the morpheus api
    :doc-author: Trelent
    """
    logger.info(f'Begin get_morpheus_license_from_cypher')
    c = Cypher(url=url,token=token,ssl_verify=False)
    out = c.get(cypher_name)
    return(out)

def sleep(time):
    """
    The sleep function is used to pause the program for a specified amount of time.
    It can be useful when waiting for an external service to respond, or when polling
    a database.
    
    :param time: Specify how long the function should sleep for
    :return: None
    :doc-author: Trelent
    """
    logger.info(f'Sleeping for {time}')
    time.sleep(time)