
import json
import requests
import urllib.request
import sys
import subprocess

from api_server import PORT
from map_network import map_network

# launch the api server asynchronously
python_exec = sys.executable
p = subprocess.Popen([python_exec, "api_server.py"])  # something long running


# Request to the locally launched API server

valid_ip_list = map_network()

for ip in valid_ip_list:
    url = 'http://' + ip + ':' + str(PORT) + '/es_el_mercado_amigo'

    # data = '''{}'''
    # response = requests.post(url, data=data)
    try:
        response = urllib.request.urlopen(url).read()
        print(ip, json.loads(response))
    except:
        pass

p.terminate()
