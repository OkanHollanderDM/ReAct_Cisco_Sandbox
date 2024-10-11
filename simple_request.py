from pprint import pprint

import requests

HOST = "devnetsandboxiosxe.cisco.com"
PORT = 443
USERNAME = "admin"
PASSWORD = "C1sco12345"

DEVICE = {
    "hostname": HOST,
    "port": PORT,
    "username": USERNAME,
    "password": PASSWORD,
}

URL = f"https://{DEVICE['hostname']}:{DEVICE['port']}/restconf/data/ietf-interfaces:interfaces"

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

response = requests.get(URL, headers=HEADERS, auth=(DEVICE["username"], DEVICE["password"]), verify=False)

if response.status_code == 200:
    response_dict = response.json()
    for interface in response_dict["ietf-interfaces:interfaces"]["interface"]:
        pprint(interface)