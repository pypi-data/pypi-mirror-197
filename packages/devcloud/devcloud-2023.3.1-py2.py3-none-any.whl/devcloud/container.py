import re
from devcloud.project import *
import json, os
import typer
from devcloud.common import *


# with the help of createcontainer function, user can create container to the devcloud container playground.
def createcontainer(containerName: str = typer.Option(..., "-cn", "--containername", help="enter container name"),
                    projectName: str = typer.Option(..., "-pn", "--projectname",
                                                    help="enter project name you want to assign container"),
                    url: str = typer.Option(..., "-u", "--url", help="enter url")):
    """
    create a new container for project.

    EXAMPLE:devcloud createcontainer --containername "your container name" --projectname "project name you want to assign container" --url "enter URL"
    """
    validateToken()
    env = data.get('ENVIRONMENT').get('env')
    header = getheader()
    Containersurl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("containers"))
    projectId = getprojectID(projectName)
    userId = userId = getuserID()
    payload = json_data.get("payloads").get("createcontainer")
    payload.update({'containerName': containerName,
                    'projectId': projectId,
                    'projectName': projectName,
                    'url': url,
                    'userId': userId
                    })
    validateURL = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("validateimage"))
    validateURLResponse = requests.post(validateURL, headers=header, json=payload, cookies=cookies)
    try:
        statusCode = validateURLResponse.status_code
        if statusCode == 502:
            print("Invalid url or the repository is private.Please check and import again.")
            return False
        containerResponse = requests.post(Containersurl, headers=header, json=payload, cookies=cookies)
        status_code = containerResponse.status_code
        if status_code == 201:
            print("container {} created!.".format(containerName))
        else:
            bytesValue = containerResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except Exception as e:
        print("Exception occurred while creating container {}".format(e))


# with the help of getcontainer function, user can get the list of containers  that available on the devcloud container playground.
def getcontainer(output: str):
    """
    give a list of containers exists in devcloud container playground.

    EXAMPLE: devcloud getcontainer
    """

    validateToken()
    env = data.get('ENVIRONMENT').get('env')
    header = getheader()
    resourcesUrl = geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
    resoucesResponse = requests.get(resourcesUrl, headers=header)
    projectDetailsUrl = geturl(json_data.get(env).get("BYOC_ENV"),
                                     json_data.get("endPoints").get("projectDetails"))
    projectDetailsResponse = requests.get(projectDetailsUrl, headers=header)

    try:
        projectDetailsResponseData = projectDetailsResponse.json()
        statusCode = resoucesResponse.status_code
        if statusCode == 204:
            print("No content Available")
        elif statusCode == 200:
            resourceResponseData = resoucesResponse.json()
            mydata = []
            wide = []
            head = ["Sr.No.", "Container Id ", "Container Name"]
            headOfWide = ["Sr.No.", "Container Id ", "Container Name", "Project Name"]
            count = 0
            for dataItems in resourceResponseData.get('response'):
                ContainerId = dataItems.get('containerId')
                ContainerName = dataItems.get('resourceName')
                count = count + 1
                if output == "wide":
                    projectID = dataItems.get('projectIds')
                    if projectID == None:
                        name = "None"
                        wide.append([count, ContainerId, ContainerName, name])
                    else:
                        projectID = dataItems.get('projectIds')[0]
                    for data_items in projectDetailsResponseData.get('projectContainerDTOs'):
                        projectId = data_items.get('projectId')
                        if projectId == projectID:
                            name = data_items.get('name')
                            wide.append([count, ContainerId, ContainerName, name])
                mydata.append([count, ContainerId, ContainerName])
            if output == "wide":
                createTable(wide, headOfWide)

            else:
                createTable(mydata, head)
        else:
            print("Unexpected Error!", projectDetailsResponse.json)
    except:
        print("Unexpected Error!\n", projectDetailsResponse.json)


# with the help of deletecontainer function, user can delete particular container from devcloud container playground.
def deletecontainer(containerName: str):
    """
    delete container of the project.

    EXAMPLE:  devcloud deletecontainer --containername "container name you want to delete"
    """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    resourcesUrl = geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
    resoucesResponse = requests.get(resourcesUrl, headers=header, cookies=cookies)
    try:
        resourceResponseData = resoucesResponse.json()
        project_id = None
        projectExists = False
        for dataItems in resourceResponseData.get('response'):
            resouceName = dataItems.get('resourceName')
            name = re.split(":", resouceName)
            if containerName == name[0]:
                projectExists = True
                resoucename = dataItems.get('resourceName')
                assignmentStatus = dataItems.get('projectAssignStatus')
                if assignmentStatus == True:
                    project_id = dataItems.get('projectIds')
                    project_Id = project_id[0]
                else:
                    project_Id = None
        if not projectExists:
            print("The container name does not exists")
            return False

        projectDetailsUrl = geturl(json_data.get(env).get("BYOC_ENV"),
                                         json_data.get("endPoints").get("projectDetails"))
        projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
        projectDetailsResponseData = projectDetailsResponse.json()
        for data_items in projectDetailsResponseData['projectContainerDTOs']:
            project_ID = data_items.get('projectId')
            if project_Id == project_ID:
                project_name = data_items.get('name')
        if assignmentStatus == True:
            print(
                "container " + containerName + " is assign to project " + project_name + ", please unassign that first")
        else:
            deleteUrl = geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("deleteBuild"))
            url = deleteUrl.format(resoucename)
            deleteResponse = requests.delete(url, headers=header, cookies=cookies)
            statusCode = deleteResponse.status_code
            if statusCode == 200:
                print("Container {} deleted!.".format(containerName))
            else:
                bytesValue = deleteResponse.content
                myJson = json.loads(bytesValue.decode())
                print(myJson.get('message'))
    except:
        print("Unexpected Error!\n", resoucesResponse.json)


# with the help of unassigncontainer function, user can unassign container on the devcloud container playground.
def unassigncontainer(containerName: str, projectName: str):
    """
        unassign container of the project.

        EXAMPLE: devcloud unassigncontainer --containername "container name "
        """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    projectDetailsUrl = geturl(json_data.get(env).get("BYOC_ENV"),
                                     json_data.get("endPoints").get("projectDetails"))
    projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)

    try:
        projectDetailsResponseResponseData = projectDetailsResponse.json()
        project_Id = getprojectID(projectName)
        count = 0
        resourcesUrl = geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
        resoucesResponse = requests.get(resourcesUrl, headers=header, cookies=cookies)
        resourceResponseData = resoucesResponse.json()
        for dataItems in resourceResponseData.get('response'):
            resouceName = dataItems.get('resourceName')
            name = re.split(":", resouceName)
            if containerName == name[0]:
                assignmentStatus = dataItems.get('projectAssignStatus')
                if assignmentStatus == False:
                    print("container is already unassigned")
                    return False

        container_name = False
        for dataItems in projectDetailsResponseResponseData.get('projectContainerDTOs'):
            name = dataItems.get('name')
            count = count + 1
            for i in range(0, count):
                if name == projectName:
                    for items in projectDetailsResponseResponseData['projectContainerDTOs'][count - 1]['containers']:
                        # for items in projectDetailsResponseResponseData.get('projectContainerDTOs')[count-1].get('containers'):
                        resourceName = items.get('containerName')
                        if resourceName == containerName:
                            container_Id = items.get('containerId')
                            container_name = True
                            break

        if container_name == False:
            print("container name not exist")
            return False
        payload = json_data.get("payloads").get("unassignContainer")
        payload.update({'containerId': container_Id,
                        'projectId': project_Id,
                        'resourceName': containerName
                        })
        unassignUrl = geturl(json_data.get(env).get("BYOC_ENV"),
                                   json_data.get("endPoints").get("unassignContainer"))
        unassignResponse = requests.post(unassignUrl, headers=header, json=payload, cookies=cookies)
        stausCode = unassignResponse.status_code
        if stausCode == 200:
            print("Container {} Unassigned!.".format(containerName))
        else:
            bytesValue = unassignResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except:
        print("Unexpected Error!\n", projectDetailsResponse.json)


# with the help of assigncontainer function, user can assign container to particular project on the devcloud container playground.
def assigncontainer(containerName: str , projectName: str):
    """
        assign container to the project.

        EXAMPLE: devcloud assigncontainer --containername "container name " --projectname "project to which you want to assign the container"
        """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    assignUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("containers"))
    containersResponse = requests.get(assignUrl, headers=header, cookies=cookies)
    try:
        responseData = containersResponse.json()
        container_name = False
        for data_items in responseData.get('resources'):
            name = data_items.get('resourceName')
            if containerName == name:
                containerId = data_items.get('containerId')
                container_name = True
                break
        if container_name == False:
            print("container name not exist")
            return False
        userId = getuserID()
        projectId = getprojectID(projectName)
        payload = json_data.get("payloads").get("assignContainer")
        payload.update(
            {'containerId': containerId, 'containerName': containerName, 'projectId': projectId, 'url': projectName,
             'userId': userId})
        assignResponse = requests.post(assignUrl, headers=header, json=payload, cookies=cookies)
        assignResponseData = assignResponse.json()
        staus_code = assignResponse.status_code
        if staus_code == 201:
            print("Container " + containerName + " assigned to project " + projectName)
        else:
            bytesValue = assignResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except:
        print("Unexpected Error!\n", containersResponse.json)


def createConfiguration(projectName: str, containerName: str, port: list = [], label: list = [], entryPoint: str = "",
                        outputPath: str = "", mountPath: list = [()], environment: str = ""):
    validateToken()
    env = data.get('ENVIRONMENT').get('env')
    header = getheader()
    containerID = getContainerId(containerName)
    projectId = getprojectID(projectName)
    payload = json_data.get("payloads").get("createContainer")
    inputPaths, containerPaths = list(map(list, zip(*mountPath)))
    payload.update({'additionalConfig': environment,
                    'containerId': containerID,
                    'containerName': "",
                    'dependentOn': [],
                    'entryPoint': entryPoint,
                    'mountPoint': outputPath,
                    'port': ','.join(port),
                    'projectId': projectId,
                    'newTags': label,
                    'cancelledTags': [],
                    'toStorage': "",
                    'routeEnabledPort': "",
                    'inputPaths': inputPaths,
                    'containerPaths': containerPaths
                    })
    configurationURL = geturl(json_data.get(env).get("CONFIG_ENV"),
                                    json_data.get("endPoints").get("configuration"))
    response = requests.post(configurationURL, headers=header, json=payload, cookies=cookies)
    status_code = response.status_code
    if status_code == 200:
        print("Updated the configuration!!")
    else:
        print("Configuration update failed")


def getContainerId(containerName: str) -> int:
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    resourcesUrl = geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
    resoucesResponse = requests.get(resourcesUrl, headers=header, cookies=cookies)
    project_id = None
    projectExists = False
    containerId = None
    try:
        resourceResponseData = resoucesResponse.json()
        for dataItems in resourceResponseData.get('response'):
            resouceName = dataItems.get('resourceName')
            name = re.split(":", resouceName)
            if containerName == name[0]:
                projectExists = True
                containerId = dataItems.get('containerId')
                assignmentStatus = dataItems.get('projectAssignStatus')
                if assignmentStatus == True:
                    project_id = dataItems.get('projectIds')
                    project_Id = project_id[0]
                else:
                    project_Id = None
                break
        if not projectExists:
            print("No container");
            return False

    except:
        print("Unexpected Error!\n")#, projectDetailsResponse.json)
        print("Failed to get container")
        return False
    return containerId
