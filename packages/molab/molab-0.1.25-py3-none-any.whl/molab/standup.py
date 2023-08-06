import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import logging
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_lab_terraform_inputs(morpheus_custom_options):
    if "adm" in morpheus_custom_options["classType"]:
        f = open("./template_files/admin_class_config.json")
        f = json.load(f)
    elif "ins" in morpheus_custom_options["classType"]:
        f = open("./template_files/install_class_config.json")
        f = json.load(f)
    elif 'atm' in morpheus_custom_options["classType"]:
        f = open("./template_files/automation_class_config.json")
        f = json.load(f)
    elif 'tbs' in morpheus_custom_options["classType"]:
        f = open("./template_files/troubleshooting_class_config.json")
        f = json.load(f)
    print(f)
    terraform_inputs = {}
    for k, v in morpheus_custom_options.items():
        print(f'Check {k}')
        if k in f:
            print(f'Found {k}, updating with value of {v}')
            update = {k: v}
            print(update)
            terraform_inputs.update(update)
    for k, v in f.items():
        if v != "":
            print(f'Item {k} with value of {v} discovered. Updating...')
            update = {k: v}
            terraform_inputs.update(update)
    return(terraform_inputs)

def get_instance_type_layouts(url,headers,instance_type_name):
    layouts = []
    endpoint = "/api/library/instance-types"
    resp = requests.get(f'{url}{endpoint}?name={instance_type_name}', headers=headers, verify=False).json()
    for k in resp["instanceTypes"]:
        if instance_type_name in k["name"]:
            layouts.append(k["instanceTypeLayouts"])
    return(layouts[0])
