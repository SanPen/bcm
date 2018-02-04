
import json
import requests
import urllib.request
import sys
import subprocess

from api_server import PORT
from map_network import map_network, get_my_ip


def launch_api_server():
    """

    :return:
    """
    # launch the api server asynchronously
    python_exec = sys.executable
    p = subprocess.Popen([python_exec, "api_server.py"])  # something long running
    return p


def get_players():
    """
    Get the network ip's that host the GET function es_el_mercado_amigo, on the designated port
    :return: list of players
    """
    # Request to the locally launched API server

    valid_ip_list = map_network()
    players = list()
    for ip in valid_ip_list:
        url = 'http://' + ip + ':' + str(PORT) + '/es_el_mercado_amigo'

        # data = '''{}'''
        # response = requests.post(url, data=data)
        try:
            response = urllib.request.urlopen(url).read()
            players.append(ip)
            print(ip, json.loads(response))
        except:
            pass

    return players


def register_players(players_lst):
    """
    Register the detected players into the block chain
    :param players_lst:
    :return:
    """
    my_ip = get_my_ip()

    url = 'http://' + my_ip + ':' + str(PORT) + '/nodes/register'

    data = dict()
    data['nodes'] = players_lst
    response = requests.post(url, json=data)

    print(response.json())


if __name__ == '__main__':

    p = launch_api_server()

    players_list = get_players()

    register_players(players_lst=players_list)

    p.terminate()
