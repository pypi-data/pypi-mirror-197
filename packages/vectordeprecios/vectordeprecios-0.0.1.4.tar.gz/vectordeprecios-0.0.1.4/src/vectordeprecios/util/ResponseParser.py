"""Copyright © 2022 Burrus Financial Intelligence, Ltda. (hereafter, BFI) Permission to include in application
software or to make digital or hard copies of part or all of this work is subject to the following licensing
agreement.
BFI Software License Agreement: Any User wishing to make a commercial use of the Software must contact BFI
at jacques.burrus@bfi.lat to arrange an appropriate license. Commercial use includes (1) integrating or incorporating
all or part of the source code into a product for sale or license by, or on behalf of, User to third parties,
or (2) distribution of the binary or source code to third parties for use with a commercial product sold or licensed
by, or on behalf of, User. """

import time
import os

def getResponse(filename, timeOut=300, timeFrecuency=0.5):
    startTime = time.time()
    responsePath = '/opt/datawarehouse/responses/'
    if responsePath in filename:
        filepath = filename
    else:
        filepath = f'{responsePath}{filename}'
    while time.time() - startTime < timeOut:
        fileExists = os.path.exists(filepath)
        if fileExists:
            with open(filepath, "r") as f:
                response = f.read()
            return response
        else:
            time.sleep(timeFrecuency)
            if time.time() - startTime > timeOut:
                raise TimeoutError("The time out limit (" + str(timeOut) + " seconds) has been exceeded.")
