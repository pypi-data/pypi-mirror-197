from .utilities import getRequest, getMaterialsApiTarget, getClientAliasId
from .entities import Material

import json

class MaterialCasIdInfo:
    def __init__(self, name, casId):
        self.name = name
        self.casId = casId

def getAllMaterials() -> list[Material]:

    """Gets the full detais of all available materials.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        List[Material]: The list of available materials.
    """

    url = f'{getMaterialsApiTarget()}all?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materials = list[Material]()

        for json_def in json.loads(response.text):
            material = Material()
            material.initialiseFromDictionary(json_def)
            materials.append(material)

        return materials
        
    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)
    
def getAllCasIds() -> list[MaterialCasIdInfo]():

    """Gets a list containing the names of all available materials and their CAS IDs.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
         List[MaterialCasIdInfo]: The list of available material names and their CAS IDs.
    """

    url = f'{getMaterialsApiTarget()}cas?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materials = json.loads(response.text)

        materialsInfoList = list[MaterialCasIdInfo]()

        for material in materials:
            materialsInfoList.append(MaterialCasIdInfo(material["casId"], material["name"]))

        return materialsInfoList

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)
    
def getMaterialByCasId(casId: str) -> Material:

    """Gets a material by CAS ID.

    Args:
        casId (str): The CAS ID to search for,

    Raises:
        ValueError: Any communication error with the PWS APIs or if a materoal woth the supplied CAS ID cannot be found.

    Returns:
        Material: The material which has the supplied CAS ID.
    """

    url = f'{getMaterialsApiTarget()}cas/{casId}?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materialJson = json.loads(response.text)
        material = Material()
        material.initialiseFromDictionary(materialJson)

        return material
    
    elif response.status_code == 404: 
        raise ValueError('Material with the specifid CAS ID not found.', casId)

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)
    
def getMaterialById(id: str) -> Material: 

    """Gets a material by ID.

    Args:
        id (str): The ID to search for,

    Raises:
        ValueError: Any communication error with the PWS APIs or if a materoal woth the supplied ID cannot be found.

    Returns:
        Material: The material which has the supplied ID.
    """

    url = f'{getMaterialsApiTarget()}{id}?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materialJson = json.loads(response.text)
        material = Material()
        material.initialiseFromDictionary(materialJson)

        return material
    
    elif response.status_code == 404: 
        raise ValueError('Material with the specifid ID not found.', id)

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)