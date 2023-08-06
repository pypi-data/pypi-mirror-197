import json
import os
import importlib.resources

import requests
import pandas as pd
from tabulate import tabulate

cookies = {
    'XSRF-TOKEN': 'devcloud'
}
data = {}
with importlib.resources.open_text("devcloud", "environment.json") as json_file:
    json_data = json.load(json_file)

if os.path.exists("token.json"):
    with open("token.json", 'r') as json_file:
        data=json.load(json_file)


def loadToken():
    if os.path.exists("token.json"):
        with open("token.json", 'r') as json_file:
            data.update(json.load(json_file))


loadToken()


def validateToken():
    if not os.path.exists('token.json'):
        with open("token.json", 'w+') as json_file:
            data = {"TOKEN": {"jwt": ""}, "USERID": {"userId": 0}, "ENVIRONMENT": {"env": ""},"MAPPING":[], "NAMESPACE": ""}
            json.dump(data, json_file)
    with open("token.json", 'r') as json_file:
        data = json.load(json_file)
        if data.get("TOKEN").get('jwt') == "":
            print("Error: JWT Token missing")
            return False


def geturl(host: str, endPoint: str):
    try:
        url = host + endPoint
        return url
    except:
        print("Unexpected Error!\n")
        return False


def getheader():
    with open("token.json", 'r') as json_file:
        data = json.load(json_file)
        jwt = data.get('TOKEN').get('jwt')
    header = {
        'Authorization': 'Bearer {}'.format(jwt),
        "X-XSRF-TOKEN": 'devcloud',
        "Cookie": 'token={};XSRF-TOKEN={}'.format(jwt, 'devcloud')}
    return header


def getjwt():
    return data.get("TOKEN").get('jwt')


def getuserID():
    return data.get('USERID').get('userId')


def getUserNamespace():
    return data.get("NAMESPACE")


def getRequest(host: str, endPoint: str, header: dict = {}):
    header = getheader()
    response = requests.get(geturl(host, endPoint), headers=header)
    return response


def createTable(mydata: list, head: list):
    dataframe = pd.DataFrame(mydata, columns=head)
    pd.set_option('display.colheader_justify', 'center')
    print(tabulate(dataframe, headers=head, stralign="center", tablefmt="grid", showindex="never"))


def getprojectID(project_name: str):
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    projectDetailsUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))
    projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
    try:
        response_data = projectDetailsResponse.json()
        projectExists = False
        for data_items in response_data.get('projectContainerDTOs'):
            Name = data_items.get('name')
            if project_name == Name:
                projectExists = True
                project_Id = data_items.get('projectId')
        if not projectExists:
            print("The project name does not exists")
            return False
        return project_Id
    except:
        print("Unexpected Error!\n", projectDetailsResponse.json)
        return False


def getcontainerID(containerName: str):
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    assignUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("containers"))
    containersResponse = requests.get(assignUrl, headers=header, cookies=cookies)
    try:
        responseData = containersResponse.json()
        for data_items in responseData.get('resources'):
            name = data_items.get('resourceName')
            if containerName == name:
                containerId = data_items.get('containerId')
        return containerId
    except:
        print("Unexpected Error!\n", containersResponse.json)
        return False

def updateEdgeId():
    try:
        env = data.get('ENVIRONMENT').get('env')
        header = getheader()
        resourcesUrl = geturl(json_data.get(env).get("EDGENODE_ENV"), json_data.get("endPoints").get("edgenode"))
        resoucesResponse = requests.get(resourcesUrl, headers=header)
        resourceResponseData = resoucesResponse.json()
        with open("token.json", 'r+') as json_file:
            dataJson = json.load(json_file)
            j = 0
            mapId = []
            for dataItems in resourceResponseData:
                id = dataItems.get('id')
                j = j + 1
                mapId.append({j: id})
            dataJson['MAPPING'] = mapId
            json_file.seek(0)
            json.dump(dataJson, json_file, indent=4)
    except Exception as e:
        print("Unexpected Error\n", e)
        

def updateId():
    validateToken()
    env = data.get('ENVIRONMENT').get('env')
    header = getheader()
    edgeNode = geturl(json_data.get(env).get("EDGENODE_ENV"), json_data.get("endPoints").get("edgenode"))
    edgeNodeResponse = requests.get(edgeNode, headers=header)
    try:
        resourceResponseData = edgeNodeResponse.json()
        with importlib.resources.open_text("devcloud", "environment.json") as json_file:
            dataJson = json.load(json_file)
            j = 0
            mapId = []
            for dataItems in resourceResponseData:
                id = dataItems.get('id')
                j = j + 1
                mapId.append({j: id})
            dataJson['MAPPING'] = mapId
            json_file.seek(0)
            json.dump(dataJson, json_file, indent=4)
    except Exception as e:
        print("Unexpected Error\n", e)

def getResultBaseURL() -> str:
    return "https://result-service-devcloud-{env}-{namespace}-intel.apps.cfa.devcloud.intel.com".format(env="prod",
                                                                                                        namespace= getUserNamespace())

def getFilePath(projectName: str, hardware: str = "", timestamp: str = "", filePath:str = ""):
    path = getMountPath(projectName, hardware, timestamp)
    return path + '/' + filePath

def getMountPath(projectName: str, hardware: str = "", createTime: str = ""):
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    podUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("pod"))
    podResponse = requests.get(podUrl, headers=header)
    try:
        podResponseData = podResponse.json()
        for i, dItems in enumerate(podResponseData.get('listProjects')):
            projectname = dItems.get('projectDTO').get('name')
            if projectname == projectName:
                for target in dItems.get('targets'):
                    if hardware:
                        if hardware == target.get('targetName'):
                            if createTime:
                                if createTime == target.get('createTime'):
                                    return target.get('mountSubPath')
                            else:
                                return target.get('mountSubPath')
                    else:
                        return target.get('mountSubPath')
    except:
        print("Unexpected Error!\n", podResponse.json)


def getFiles(pName: str, hardware: str = "", timeStamp: str = ""):
    header = getheader()
    path = getFilePath(pName, hardware, timeStamp)
    url = getResultBaseURL() + "/results/secure/fileExplorer?path={path}".format(path=path)
    response = requests.get(url=url, headers=header)
    if response.status_code !=200:
        print("Status code is incorrect {}".format(response.status_code))
        return False
    return [fileNames.get('fileName') for fileNames in response.json()]
