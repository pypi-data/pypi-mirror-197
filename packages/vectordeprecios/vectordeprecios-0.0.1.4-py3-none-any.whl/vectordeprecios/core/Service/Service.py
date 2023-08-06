"""Copyright © 2022 Burrus Financial Intelligence, Ltda. (hereafter, BFI) Permission to include in application
software or to make digital or hard copies of part or all of this work is subject to the following licensing
agreement.
BFI Software License Agreement: Any User wishing to make a commercial use of the Software must contact BFI
at jacques.burrus@bfi.lat to arrange an appropriate license. Commercial use includes (1) integrating or incorporating
all or part of the source code into a product for sale or license by, or on behalf of, User to third parties,
or (2) distribution of the binary or source code to third parties for use with a commercial product sold or licensed
by, or on behalf of, User. """

import requests
from vectordeprecios.core.Object import Object

class Service(Object):

    @staticmethod
    def getEndpoint():
        return "http://161.238.231.3:8080/"

    def getResponse(self, token):
        if not isinstance(token, str):
            raise TypeError('The token must be set to a string.')
        postData = self.getJson()
        headers = {'x-api-key': token}
        response = requests.post(self.getEndpoint(), data=postData, headers=headers)
        return response.text

