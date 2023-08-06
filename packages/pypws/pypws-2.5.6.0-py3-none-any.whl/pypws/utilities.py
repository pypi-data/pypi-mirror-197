import sys
import os
import json
import pathlib

import requests
from requests import Response

from .constants import REST_API_URI, PWS_CLIENT_ID, REST_API_VERSION

config = None

def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux2":
        return home / ".local/share"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


def getLicenceFolderPath():

    config = getConfigFile()
    accessTokenFileName = ''

    accessTokenFileName = config['tokenFilePath']
    if (accessTokenFileName == None):
        print("Unable to obtain the license file.")
        sys.exit()

    return accessTokenFileName

# Post json to url and time the call
def postRequest(url, json) -> Response:

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(getAccessToken())
    }

    response = requests.post(url, json=json, headers=headers, verify=True)

    return response

def getRequest(url) -> Response:

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(getAccessToken())
    }

    response = requests.get(url, headers=headers, verify=True)

    return response

def getAccessToken():

    print('Looking for access token in PYPWS_ACCESS_TOKEN environment variable')
    
    accessToken = os.getenv('PYPWS_ACCESS_TOKEN')

    if not accessToken:

        accessTokenFileName = getLicenceFolderPath()

        try:
            with open(accessTokenFileName, 'r') as file:
                print(f"Looking for access token in {accessTokenFileName}")
                accessToken = file.read().replace('\n', '')
                print(f"Access token found in {accessTokenFileName}")
        except OSError as ose:
            print('Could not read access token file (%s): %s' % (accessTokenFileName, ose.strerror))
            sys.exit()

        except:
            print('Could not read access token file (%s): %s' % (accessTokenFileName, sys.exc_info()[0]))
            sys.exit()

    else:
        print('Found access token in PYPWS_ACCESS_TOKEN environment variable.')

    return accessToken

def getConfigFile() -> dict:

    os_datadir = get_datadir() / "DNV"
    try:
        os_datadir.mkdir(parents=True)
    except FileExistsError:
        pass

    os_datadir = get_datadir() / "DNV" / "Phast Web Services"

    try:
        os_datadir.mkdir(parents=True)
    except FileExistsError:
        pass
    
    userSettingsFileName = os.path.join(os_datadir, 'UserSettings.json')

    path = pathlib.Path(userSettingsFileName)

    if not path.exists():
        print('User settings file (%s) not found' % path)

        try:
            jObject = {}
            jObject['tokenFilePath'] = '<Enter the fully qualified path to your token file here>'
            jObject['selectedAPIEndpoint'] = REST_API_URI
            jObject['selectedAPIVersion'] = REST_API_VERSION
            jObject['selectedClientAliasId'] = PWS_CLIENT_ID

            with open(path,'w') as jsonFile:
                json.dump(jObject, jsonFile)

            print('One has been created for you but you will need to update it to specify the location of your access token file')

        except OSError as ose:
            print('Tried to create a user settings file but was not able to: %s' % ose.strerror)

        except:
            print('Tried to create a user settings file but was not able to: %s' % sys.exc_info()[0])

        sys.exit()

    global config

    if config == None:
        with open(path, 'r') as f:
            config = json.load(f)

    return config

def getApiRoot() -> str:

    apiTarget = os.getenv('PYPWS_API_TARGET')

    if apiTarget:

        if not apiTarget.endswith('/'):
            apiTarget = apiTarget + '/'

        return apiTarget

    config = getConfigFile()

    try:

        apiTarget = config['selectedAPIEndpoint']

        if (apiTarget == None):
            return REST_API_URI

        if not apiTarget.endswith('/'):
            apiTarget = apiTarget + '/'

        return apiTarget

    except KeyError:
        return REST_API_URI

def getApiVersion() -> str:

    apiVersion = os.getenv('PYPWS_API_VERSION')

    if apiVersion:
        return apiVersion

    config = getConfigFile()

    try:

        apiVersion = config['selectedAPIVersion']

        print(apiVersion)

        if (apiVersion == None):
            return REST_API_VERSION
        
        return apiVersion

    except KeyError:
        return REST_API_VERSION

def getAnalyticsApiTarget() -> str:

    analyticsApiRoot = f'{getApiRoot()}analytics/v{getApiVersion()}/'
    print (f'Using Analytics API: {analyticsApiRoot}')
    return analyticsApiRoot

def getMaterialsApiTarget() -> str:

    materialsApiRoot = f'{getApiRoot()}materials/v{getApiVersion()}/'
    print (f'Using Materials API: {materialsApiRoot}')
    return materialsApiRoot

def getClientAliasId() -> str:
 
    clientAliasId = os.getenv('PYPWS_CLIENT_ALIAS_ID')

    if clientAliasId:
        return clientAliasId

    config = getConfigFile()

    try:

        clientAliasId = config['selectedClientAliasId']

        if (clientAliasId == None):
            return PWS_CLIENT_ID

        return clientAliasId

    except KeyError:
        return PWS_CLIENT_ID

    return PWS_CLIENT_ID