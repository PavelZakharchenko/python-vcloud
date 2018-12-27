#!/usr/bin/env python3

import sys
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
import requests

# Collect arguments.
if len(sys.argv) != 8:
    print("Usage: python3 {0} host org user password vdc vapp cmd".format(sys.argv[0]))
    sys.exit(1)
if sys.argv[7] not in {'powerOff', 'powerOn'}:
	print ("Error. Allowed commands: powerOff / powerOn")
	sys.exit(1)

_host = sys.argv[1]
_org = sys.argv[2]
_user = sys.argv[3]
_password = sys.argv[4]
_vdc = sys.argv[5]
_vapp = sys.argv[6]
_cmd = sys.argv[7]

requests.packages.urllib3.disable_warnings()

print("Logging in: host={0}, org={1}, user={2}".format(_host, _org, _user))
client = Client(_host,
				api_version='30.0',
				verify_ssl_certs=False,
				log_file='pyvcloud.log',
				log_requests=True,
				log_headers=True,
				log_bodies=True)
client.set_credentials(BasicLoginCredentials(_user, _org, _password))

org_resource = client.get_org()
org = Org(client, resource=org_resource)

vdc_resource = org.get_vdc(_vdc)
vdc = VDC(client, resource=vdc_resource)

vapp = VApp(client, resource=vdc.get_vapp(_vapp))

if _cmd == 'powerOff':
	vapp.undeploy(action='powerOff')
elif _cmd == 'powerOn':
	vapp.power_on()
	
# Log out.
print("Logging out")
client.logout()