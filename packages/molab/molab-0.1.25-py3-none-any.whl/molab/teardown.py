import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_instance_existence(url,headers,ids):
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.get(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            instance = resp.json()
            id = instance["instance"]["id"]
            instances.append(id)
    return(instances)

def unlock_instance(url,headers,ids):
    logger.info(f'Attempting to unlock instances: {ids}')
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.put(f'{url}{endpoint}{i}/unlock', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result().json()
        if resp["success"]:
            for k in resp["results"].keys():
                logger.info(f'Instance {k} unlocked')
                instances.append(k)
    return(instances)

def delete_instance(url,headers,ids):
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.delete(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result().json()
        if resp["success"]:
            logger.info(f'Successfully initiated teardowm of instance')
        return(resp)