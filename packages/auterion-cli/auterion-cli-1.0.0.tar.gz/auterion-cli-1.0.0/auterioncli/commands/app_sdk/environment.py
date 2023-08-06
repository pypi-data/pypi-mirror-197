import subprocess
import json
import sys
import os

import requests


def error(msg, code=1):
    print(msg, file=sys.stderr)
    exit(code)


def try_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return 0, result.stdout.decode()
        else:
            return result.returncode, 'Command ' + ' '.join(command) + ' failed on this system.'
    except FileNotFoundError:
        return 2, 'Command ' + ' '.join(command) + ' not found on this system.'


def ensure_docker():

    code, result = try_command(['docker', 'version', '--format', '{{json .}}'])
    if code != 0:
        error('Docker not working on this system. Make sure docker is installed and runnable')

    res = json.loads(result)
    server_version = 'N/A'
    if 'Server' in res:
        server_version = res['Server']['Version']
    print(f'.. Found docker client {res["Client"]["Version"]}, server {server_version}')

    # Try podman-compose, fall back to docker compose
    compose_cmd = ['podman-compose']

    code, _ = try_command(compose_cmd + ['version'])
    if code != 0:
        compose_cmd = ['docker', 'compose']
        code, _ = try_command(compose_cmd + ['version'])
        if code != 0:
            error('Docker compose plugin not found on this system. Make sure you have docker compose installed. \n'
                  'E.g. on ubuntu, you can install it with \'sudo apt-get install docker-compose-plugin\'')
    print('.. Found docker compose plugin')
    return compose_cmd


MENDER_CI_TOOLS_TAG = 'mendersoftware/mender-ci-tools:1.0.0'


def _test_mender_artifact():
    code, res = try_command(['docker', 'run', '--rm', MENDER_CI_TOOLS_TAG, 'mender-artifact', '--version'])
    if code == 0:
        print('.. Found mender artifact ' + res)
        return True
    return False


def ensure_mender_artifact():

    # check if exists locally
    code, result = try_command(['docker', 'inspect', '--type=image', MENDER_CI_TOOLS_TAG])
    if code != 0:
        print('> Pulling mender ci-tools ...')
        code, result = try_command(['docker', 'pull', MENDER_CI_TOOLS_TAG])
        if code != 0:
            error(f'Could not pull {MENDER_CI_TOOLS_TAG} image from docker hub. Exiting.')

    if not _test_mender_artifact():
        error(f'Error: Failed to execute mender artifact in image {MENDER_CI_TOOLS_TAG}. Aborting.')
