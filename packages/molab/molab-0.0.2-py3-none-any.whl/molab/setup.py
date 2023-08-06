import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_lab_terraform_inputs(morpheus_custom_options):
    # Validate the class type and import the correct file template for the template parameters to fill in
    if "administration" in morpheus_custom_options["class_type"]:
        logger.info(f'Administration class selected. Importing admin_class_config.json')
        f = pkgutil.get_data(__name__, "template_files/admin_class_config.json")
        f = json.loads(f)
    elif "installation" in morpheus_custom_options["class_type"]:
        logger.info(f'Installation class selected. Importing instal_class_config.json')
        f = pkgutil.get_data(__name__, "./template_files/install_class_config.json")
        f = json.loads(f)
    elif 'automation' in morpheus_custom_options["class_type"]:
        logger.info(f'Automation class selected. Importing automation_class_config.json')
        f = pkgutil.get_data(__name__, "./template_files/automation_class_config.json")
        f = json.loads(f)
    elif 'troubleshooting' in morpheus_custom_options["class_type"]:
        logger.info(f'Troubleshooting class selected. Importing troubleshooting_class_config.json')
        f = pkgutil.get_data(__name__, "./template_files/troubleshooting_class_config.json")
        f = json.loads(f)
    terraform_inputs = {}
    # Parse the key value pairs of the provided Morpheus custom options
    for k, v in morpheus_custom_options.items():
        logger.info(f'Checking for a match on the option type: {k}')
        try: 
            if k in f:
                logger.info(f'Found {k}, updating with a value of {v}')
                update = {k: v}
                terraform_inputs.update(update)
            else:
                logger.info(f'{k} not found in the template. Skipping it.')
        except Exception as e:
            logger.error(f'Something went wrong {e}')
    for k, v in f.items():
        try:
            if v :
                logger.info(f'Item {k} with a value of {v} discovered. Adding it to the payload.')
                update = {k: v}
                terraform_inputs.update(update)
            else:
                logger.info(f'{k} does not have a default value in the template. Skipping it')
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
    return(terraform_inputs)

def get_terraform_layout_id(url,headers,instance_type_code):
    endpoint = "/api/library/instance-types"
    try:
        logger.info(f'Attempting to get the instance type with the code of: {instance_type_code}')
        resp = requests.get(f'{url}{endpoint}?code={instance_type_code}', headers=headers, verify=False).json()["instanceTypes"][0]["instanceTypeLayouts"]
    except Exception as e:
        logger.error(f'Something went horribly wrong here: {e}')
    for l in resp:
        if "terraform" in l["provisionTypeCode"]:
            layout_id = l["id"]
    return(layout_id)

def get_morpheus_terraform_plan_id(url,headers):
    endpoint = "/api/service-plans?phrase=Terraform"
    try:
        logger.info(f'Attempting to get the Morpheus Terraform plan id.')
        resp = requests.get(f'{url}{endpoint}', headers=headers, verify=False).json()
    except Exception as e:
        logger.error(f'Something went horribly wrong {e}')
    return(resp["servicePlans"][0]["id"])

def get_instance_provisioning_payload(zone_id,instance_name,site_id,instance_type,instance_type_code,layout_id,plan_id,template_parameters):
    try:
        logger.info(f'Attempting to load the payload template file')
        f = pkgutil.get_data(__name__, "template_files/instance_provisioning_payload.json")
        f = json.loads(f)
    except Exception as e:
        logger.error(f'Something has gone awry. {e}')
    try:
        logger.info(f'Updating the payload template with the provided variables')
        f["zoneId"] = zone_id
        f["instance"]["name"] = instance_name
        f["instance"]["site"]["id"] = site_id
        f["instance"]["type"] = instance_type
        f["instance"]["instanceType"]["code"] = instance_type_code
        f["instance"]["layout"]["id"] = layout_id
        f["instance"]["plan"]["id"] = plan_id
        f["config"]["templateParameter"] = template_parameters
    except Exception as e:
        logger.error(f'Terrible failure herein {e}')
    return(f)

def set_cloud_availability(url,headers,cloud_id:int,available:bool = None):
    # Uses the location in conjunction with the Available Clouds option list to update the location to set availability
    try:
        logger.info(f'Attempting to get the cloud data')
        endpoint = "/api/zones"
        get = requests.get(f'{url}{endpoint}/{cloud_id}', headers=headers, verify=False).json()
        logger.info(f'Parsing the response...')
        location = get["zone"]["location"].split("_")[0]
    except Exception as e:
        logger.error(f'Something went wrong {e}')
    logger.info(f'Setting up the payload')
    if available:
        newLoc = f'{location}_available'
    else:
        newLoc = f'{location}_used'
    body = json.dumps({"zone":{"location": newLoc}})
    try:
        logger.info(f'Attempting to set location on the cloud to {newLoc}')
        put = requests.put(f'{url}{endpoint}/{cloud_id}', headers=headers, verify=False, data=body).json()
    except Exception as e:
         logger.error(f'Something went wrong {e}')
    return(put)

def create_instance(url,headers,payload):
    payload = json.dumps(payload)
    endpoint = "/api/instances"
    try:
        logger.info(f"Attempting to deploy the instance")
        resp = requests.post(f'{url}{endpoint}', headers=headers, verify=False, data=payload).json()
        time.sleep(30)
    except Exception as e:
        logger.error(f'Instance deployment critical failure')
    return(resp)

def deploy_class_labs(url,headers,payloads):
    session = FuturesSession()
    instances = []
    endpoint = "/api/instances"
    futures=[session.post(f'{url}{endpoint}', headers=headers, verify=False, data=json.dumps(p)) for p in payloads]
    for future in as_completed(futures):
        logger.info(f'Attempting to deploy instance for student')
        resp = future.result()
        if "200" in str(resp):
            logger.info("It appears the initiation of the deployment was successful")
            instance = resp.json()["instance"]["id"]
            instances.append(instance)
        else:
            logger.error(f'An error occurred: {resp.json()}')
    return(instances)

def lock_instance(url,headers,instance_id):
    result = requests.put(f"{url}/api/instances/{instance_id}/lock",headers=headers, verify=False)
    return(result)

def await_instance_deployment_status(url,headers,instance_ids):
    session = FuturesSession()
    endpoint = "/api/instances/"
    provisioning_instances = len(instance_ids)
    running = 0
    failed = 0
    while provisioning_instances > 0:
        logger.info(f'Current instance IDs to check: {instance_ids}')
        futures=[session.get(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in instance_ids]
        for future in as_completed(futures):
            resp = future.result()
            if "200" in str(resp):
                instance = resp.json()
                logger.info(f'Checking the status for the instance: {instance["instance"]["id"]}')
                if instance["instance"]["status"] == "running":
                    running = running + 1
                    logger.info(f'Found running instance: {instance["instance"]["id"]}')
                    logger.info(f'Removing instance {instance["instance"]["id"]} from list.')
                    logger.info(f'Running instance count: {running}')
                elif instance["instance"]["status"] == "failed":
                    failed = failed + 1
                    logger.info(f'Found failed instance: {instance["instance"]["id"]}')
                    logger.info(f'Removing instance {instance["instance"]["id"]} from list.')
                    logger.info(f'Failed instance count: {failed}')
                else:
                    logger.info("Instance still provisioning")
            else:
                logger.error(f'An error occurred: {resp.json()}')
        provisioning_instances = len(instance_ids)
    data = { "running_instances": running, "failed_instances": failed}
    return(data)
