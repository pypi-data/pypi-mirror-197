import textwrap
from devcloud.common import *
import json
import requests
import jwt


# with the help of login function, user can login to the devcloud container playground.
def login(token: str, environment: str = "PROD"):
    """
    login to devcloud container playground.

    EXAMPLE: devcloud login --token "enter jwt token"
    """
    if os.path.exists('token.json'):
        try:
            with open("token.json", 'r') as json_file:
                data = json.load(json_file)
                data['TOKEN']['jwt'] = token
                data['ENVIRONMENT']['env'] = environment
                data['MAPPING'] = []
                parse_data = jwt.decode(token, options={"verify_signature": False})
                data['USERID']['userId'] = parse_data['userId']
                data['NAMESPACE'] = parse_data['serviceName']
            with open("token.json", 'w') as json_file:
                json.dump(data, json_file)
            loadToken()
        except:
            print("Invalid Token")
    else:
        try:
            parse_data = jwt.decode(token, options={"verify_signature": False})
            data = {"TOKEN": {"jwt": token}, "USERID": {"userId": parse_data['userId']},
                    "ENVIRONMENT": {"env": environment},"NAMESPACE": parse_data['serviceName'],"MAPPING":[]}
            with open("token.json", 'w+') as json_file:
                json.dump(data, json_file)
            loadToken()
        except:
            print("Unexpected error!")

        # with the use of getproject. user will get the list of projects having on devcloud container playground.


def getProject(output: str = None):
    """
    give project list existing in devcloud container playground.

    EXAMPLE: devcloud getproject
    """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    projectDetailsUrl = geturl(json_data.get(env).get("BYOC_ENV"),
                                     json_data.get("endPoints").get("projectDetails"))
    projectDetailsResponse = requests.get(projectDetailsUrl, headers=header)
    try:
        projectDetailsResponseData = projectDetailsResponse.json()
        mydata = []
        wide = []
        head = ["Sr.No.", "project_id", "Name", "Description"]
        headForWide = ["Sr.No.", "project_id", "Name", "Description", "Create Time"]
        count = 0
        statusCode = projectDetailsResponse.status_code
        if statusCode == 200:
            for data_items in projectDetailsResponseData.get('projectContainerDTOs'):
                projectId = data_items.get('projectId')
                name = data_items.get('name')
                desc = data_items.get('description')
                if desc == None:
                    desc = ""
                Description = textwrap.fill(desc, 50)
                count = count + 1
                if output == "wide":
                    createTime = data_items.get('createTime')
                    wide.append([count, projectId, name, Description, createTime])
                mydata.append([count, projectId, name, Description])
            if output == "wide":
                createTable(wide, headForWide)
            else:
                createTable(mydata, head)
        else:
            print("Unexpected Error!\n", print(projectDetailsResponse.json))
    except:
        print("Unexpected Error!!\n", projectDetailsResponse.json)

    # with the help of createproject, user will be able to create a new project on devcloud container playground


def createproject(projectName: str, description: str):
    """
        create new project.

        EXAMPLE:  devcloud createproject --name "your project name" --description "your project description"
        """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')

    projectUrl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projects"))
    payload = {"name": projectName, "description": description}
    projectResponse = requests.post(projectUrl, headers=header, json=payload, cookies=cookies)
    try:
        statusCode = projectResponse.status_code
        if statusCode == 201:
            print("Project {} created!.".format(projectName))
        else:
            bytesValue = projectResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except:
        print("Unexpected Error!\n", projectResponse.json)


# with the help of deleteproject, user will be ableto delete existing project on devcloud container playground.
def deleteProject(projectName: str):
    """
        delete the existing project.

        EXAMPLE:  devcloud deleteproject --name "project name you want to delete"
        """
    validateToken()
    header = getheader()
    env = data.get('ENVIRONMENT').get('env')
    projectDetailsUrl = geturl(json_data.get(env).get("BYOC_ENV"),
                                     json_data.get("endPoints").get("projectDetails"))
    projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
    try:
        projectDetailsResponseData = projectDetailsResponse.json()
        projectId = getprojectID(projectName)
        projecturl = geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projects"))
        projectUrl = projecturl + "/{}".format(projectId)
        projectDetailsResponse = requests.delete(projectUrl, headers=header, cookies=cookies)
        statusCode = projectDetailsResponse.status_code
        if statusCode == 200:
            print("project {} deleted!.".format(projectName))
        else:
            bytesValue = projectDetailsResponse.content
            myJson = json.loads(bytesValue.decode())
            print(myJson.get('message'))
    except:
        print("Unexpected error!\n", projectDetailsResponse.json)
