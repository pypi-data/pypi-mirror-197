"""Copyright © 2022 Burrus Financial Intelligence, Ltda. (hereafter, BFI) Permission to include in application
software or to make digital or hard copies of part or all of this work is subject to the following licensing
agreement.
BFI Software License Agreement: Any User wishing to make a commercial use of the Software must contact BFI
at jacques.burrus@bfi.lat to arrange an appropriate license. Commercial use includes (1) integrating or incorporating
all or part of the source code into a product for sale or license by, or on behalf of, User to third parties,
or (2) distribution of the binary or source code to third parties for use with a commercial product sold or licensed
by, or on behalf of, User. """

import json
import time
import requests
from vectordeprecios.core.Service.ServiceRequest import ServiceRequest

class ServiceRequestDownload(ServiceRequest.ServiceRequest):
    def __init__(self, path=''):
        ServiceRequest.Service.Object.__init__(self)
        ServiceRequest.ServiceRequest.__init__(self)
        self.path = path

    def getPath(self):
        return self.path

    @staticmethod
    def fromJson(jsonString):
        data = json.loads(jsonString)
        if 'path' in data.keys():
            path = data['path']
        else:
            path = ''
        serviceRequestDownload = ServiceRequestDownload(path)
        return serviceRequestDownload

    @staticmethod
    def request(token, path, timeOut=300, timeFrecuency=0.5):
        startTime = time.time()
        headers = {'x-api-key': token}
        paramsDict = {'path': path}
        response = 'Failed!'
        while time.time() - startTime < timeOut:
            response = requests.get(ServiceRequest.Service.getEndpoint(), params=paramsDict, headers=headers).text
            if 'not found!' in response:
                time.sleep(timeFrecuency)
                if time.time() - startTime > timeOut:
                    raise TimeoutError("The time out limit (" + str(timeOut) + " seconds) has been exceeded.")
            else:
                return response
        return response
