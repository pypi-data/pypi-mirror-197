from devcloud.common import *
from devcloud.project import *
import json
from typing import Optional


# this function will give list of edge nodes
def getNodeDetail():
    """
    give details about all edgenodes.

    EXAMPLE:devcloud getnodedetail
    """
    validateToken()
    env = data.get('ENVIRONMENT').get('env')
    header = getheader()
    resourcesUrl = geturl(json_data.get(env).get("EDGENODE_ENV"), json_data.get("endPoints").get("edgenode"))
    resoucesResponse = requests.get(resourcesUrl, headers=header)
    updateEdgeId()
    try:
        statusCode = resoucesResponse.status_code
        if statusCode == 204:
            print("No content Available")
        elif statusCode == 200:
            resourceResponseData = resoucesResponse.json()
            mydata = []
            head = ["Id", "processorName", "integratedGpuName", "memory"]
            count = 0
            for dataItems in resourceResponseData:
                integratedGpuName = dataItems.get('integratedGpuName')
                processorName = dataItems.get('processorName')
                memory = dataItems.get('memory')
                count = count + 1
                mydata.append([count, processorName, integratedGpuName, memory])
            createTable(mydata, head)
        else:
            bytesValue = resoucesResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except:
        print("Unexpected Error!\n", resoucesResponse.json)


def deployProject(projectName: str, id: int):
    """
    deploy project in devcloud container playground.

    EXAMPLE: devcloud deployproject --id "enter id number" --projectname "enter projectname"
    """
    validateToken()
    loadToken()
    env = data.get('ENVIRONMENT').get('env')
    header = getheader()
    try:
        id = int(id)
        mapIDList = [nodeID for i, nodeID in enumerate(data["MAPPING"]) if (i + 1) == int(id)]
        if len(mapIDList) == 0:
            print("ID Not found. Please use devcloud get nodedetails for help")
            return False
        mapID = mapIDList[0].get(str(id))
        projectId = getprojectID(projectName)
        payload = json_data.get("payloads").get("deployMultipleHardeware")
        payload[0].update({
            "edgeNodeId": mapID,
            "projectId": projectId
        })
        deployMultipleHardewareURL = geturl(json_data.get(env).get("BYOC_ENV"),
                                            json_data.get("endPoints").get("deployMultipleHardware"))
        deployMultipleHardewareResponse = requests.post(deployMultipleHardewareURL, headers=header, json=payload,
                                                        cookies=cookies)
        statusCode = deployMultipleHardewareResponse.status_code
        if statusCode == 202:
            print("successfully launched!!")
        else:
            bytesValue = deployMultipleHardewareResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except Exception as e:
        print("Unexpected Error!\n", e)


# show the status of launched project
def getStatus(projectName: str = None, output: str = "wide"):
    """
    give the status of deployed project.

    EXAMPLE: devcloud getstatus or devcloud getstatus --projectname "enter projectname"
    """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    podUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("pod"))
    podResponse = requests.get(podUrl, headers=header)
    try:
        podResponseData = podResponse.json()
        mydata = []
        wide = []
        head = ["project", "target", "status"]
        headForWide = ["project", "target", "status", "execution time", "create time", "fps", "Throughput"]
        targetStatus = None
        for i, dItems in enumerate(podResponseData.get('listProjects')):
            projectname = dItems.get('projectDTO').get('name')
            if projectName and projectname == projectName:
                for target in dItems.get('targets'):
                    targetStatus = target.get('targetStatus')
                    targetName = target.get('targetName')
                    if output == "wide":
                        executionTime = target.get('executionTime')
                        createTime = target.get('createTime')
                        fps = target.get('fps')
                        for data_items in target.get('deployments'):
                            throughput = data_items.get('throughput')
                            if throughput == None or fps == None:
                                throughput = "Unavailable"
                                fps = "None"
                            else:
                                throughput = data_items.get('throughput')
                            wide.append([projectname, targetName, targetStatus, executionTime, createTime, fps, throughput])
                    else:
                        mydata.append([projectname, targetName, targetStatus])
                        break
            else:
                if projectName == None:
                    for target in dItems.get('targets'):
                        targetStatus = target.get('targetStatus')
                        targetName = target.get('targetName')
                        if output == "wide":
                            createTime = target.get('createTime')
                            executionTime = target.get('executionTime')
                            fps = target.get('fps')
                            throughput = target.get('throughput')
                            if throughput == None or fps == None:
                                throughput = "Unavailable"
                                fps = "None"
                            wide.append([projectname, targetName, targetStatus, executionTime, createTime, fps, throughput])
                        else:
                            mydata.append([projectname, targetName, targetStatus])
                            break
                    
        if output == "wide":
            createTable(wide, headForWide)
        else:
            createTable(mydata, head)
    except:
        print("Unexpected Error!\n", podResponse.json)


# show the log
def getlog(podName: str):
    """
    give the log of given pod name.

    EXAMPLE: EXAMPLE: devcloud getlog --podname "pod name"
    """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    podUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("pod"))
    podResponse = requests.get(podUrl, headers=header)
    try:
        podResponseData = podResponse.json()
        targetName = None
        targetFound = False
        for i, pItems in enumerate(podResponseData.get('listProjects')):
            for tItems in pItems.get('targets'):
                for dItems in tItems.get('deployments'):
                    targetName = dItems.get('podName')
                    if targetName == podName:
                        targetFound = True
                        podLogUrl = geturl(json_data.get(env).get("EXECUTION_ENV"),
                                           json_data.get("endPoints").get("log"))
                        url = podLogUrl.format(podName)
                        payload = json_data.get("payloads").get("podLog")
                        payload.update({'podName': podName})
                        podLogResponse = requests.get(url, headers=header, json=payload, cookies=cookies)
                        podLogResponseData = None
                        try:
                            podLogResponseData = podLogResponse.json()
                        except ValueError:
                            print("No Content available for this pod name")
                            break
                        logs = podLogResponseData.get('logs')
                        print(*logs, sep="\n")
                        break
        if not targetFound:
            print("couldnt find podname ")

    except:
        print("Unexpected Error!\n", podResponse.json)
