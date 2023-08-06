from typing import List
from devcloud.project import *
from devcloud.container import *
from devcloud.edgenode import *
import getpass
from devcloud.result import *


def connect(token: str = ""):
    if len(token) == 0:
        token=os.getenv('DEVCLOUD_TOKEN')
        if token == None:
            token = getpass.getpass("Token:")
    login(token, "PROD")
    print("LoggedIn")
    updateEdgeId()
    print("Overview - Project")
    getProject()
    print("Overview - Dashboard")
    getStatus(output="wide")

def transfer(region: str, bucketName: str, path: List, accessKey: str="", secretKey: str=""):
    if len(accessKey) == 0:
        accessKey = getpass.getpass("Access Key:")
    if len(secretKey) == 0:
        secretKey = getpass.getpass("Secret Key:")
    mount(accessKey, secretKey, region, bucketName)
    cloudImport(path, bucketName)

def createContainer(projectName: str, containerName: str, url: str):
    createproject(projectName, "")
    createcontainer(containerName, projectName, url)
    #containers.assigncontainer(containerName, projectName)


def configureContainer(projectName: str, containerName: str, port: list, label: list, entryScript: str, output: str, mountPoint: list, environment: str):
    createConfiguration(projectName, containerName, port, label, entryScript, output, mountPoint, environment)

def availableHardware():
    getNodeDetail()

def launch(projectName: str, edgeNode: int):
    deployProject(projectName, edgeNode)

def getDashboardStatus():
    getStatus()

def getProjects():
    getProject()

def previewOutput(path: str, type: str = "jpeg"):
    return getFilePreview(path=path, type=type)
    
def getFilePreview(projectName: str, path: str, edgeNode: str = "", createTime: str = "", type: str = "jpeg"):
    getFilesPreview(projectName, path, edgeNode, createTime, type)

