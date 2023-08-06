# from devcloud.common import *
from devcloud.project import *
from devcloud.common import *
import urllib.request
import urllib.parse
import io


def mount(accessKey: str, secretKey: str, region: str, bucketName: str):
    header = getheader()
    payload = {"accessKey": accessKey, "secretAccessKey": secretKey, "regionName": region, "bucketName": bucketName}
    response = requests.post(getResultBaseURL() + "/results/secure/cloud/mount", headers=header, json=payload,
                             cookies=cookies)
    statusCode = response.status_code
    if statusCode == 200:
        print("Successfully connected to S3")
    else:
        print("Unable to connect to S3 with status code {}".format(statusCode))
        return False


def cloudImport(fromPath: list, bucket: str):
    header = getheader()
    payload = {"cloudPath": list(map(lambda path: "/s3/{bucket}/{path}".format(bucket=bucket, path=path), fromPath))}
    response = requests.post(getResultBaseURL() + "/results/secure/cloud/download", headers=header, json=payload,
                             cookies=cookies)
    statusCode = response.status_code
    if statusCode == 200:
        print("Successfully import from S3")
    else:
        print("Unable to import from S3 with status code {}".format(statusCode))
        return False


def getFilesPreview(projectName: str, path: str, edgeNode: str = "", createTime: str = "", type: str = "jpeg"):
    header = getheader()
    path = getFilePath(projectName, edgeNode, createTime, path)
    url = getResultBaseURL() + "/results/secure/stream?location={path}".format(path=urllib.parse.quote(path))
    req = requests.get(url, headers=header, stream=True)
    if(req.status_code == 200):
        image_bytes = io.BytesIO(req.raw.read())
        return image_bytes
    else:
        print("Unable to get file preview, please check file path. Status code {}".format(req.status_code))
