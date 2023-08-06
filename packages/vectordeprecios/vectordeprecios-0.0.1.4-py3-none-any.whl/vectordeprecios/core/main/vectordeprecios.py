"""Copyright © 2022 Burrus Financial Intelligence, Ltda. (hereafter, BFI) Permission to include in application
software or to make digital or hard copies of part or all of this work is subject to the following licensing
agreement.
BFI Software License Agreement: Any User wishing to make a commercial use of the Software must contact BFI
at jacques.burrus@bfi.lat to arrange an appropriate license. Commercial use includes (1) integrating or incorporating
all or part of the source code into a product for sale or license by, or on behalf of, User to third parties,
or (2) distribution of the binary or source code to third parties for use with a commercial product sold or licensed
by, or on behalf of, User. """

__all__ = ['request']

# Check and install requests libraries if needed
from vectordeprecios.util import Installer, Enumerations, Arguments, Format, Output

Installer.install()

from vectordeprecios.core.Service.ServiceRequest.ServiceRequestDataPoint import ServiceRequestDataPointValue, ServiceRequestDataPointReport
from vectordeprecios.core.Service.ServiceRequest.ServiceRequestDownload import ServiceRequestDownload
import datetime
import sys

def request(token='', ticker='', family='', group='', market='', country=Enumerations.Country.Country_Unspecified,
            document='', item='', chapter='', section='', subsection='', paragraph='', path='',
            dateStart=datetime.datetime.today().date(), dateEnd=datetime.datetime.today().date(),
            fixing=Enumerations.Fixing.EOD, fieldType='', versionType=Enumerations.VersionType.Version_Unspecified,
            author='', version='', quality=Enumerations.Quality.Quality_Unspecified, timeOut=300, timeFrecuency=0.5,
            fileName='', format='dataFrame'):
    if path != '':
        return download(token, path, timeOut, timeFrecuency, format)
    elif not all(reportParameter == '' for reportParameter in [document, item, chapter, section, subsection, paragraph]):
        return requestReport(token, document, item, chapter, section, subsection, paragraph, dateStart, dateEnd, fixing,
                             fieldType, versionType, author, version, quality, timeOut, timeFrecuency, fileName, format)
    else:
        if isinstance(country, str):
            country = Enumerations.Country.fromString(country)
        return requestValue(token, ticker, family, group, market, country, dateStart, dateEnd, fixing, fieldType,
                            versionType, author, version, quality, timeOut, timeFrecuency, fileName, format)

def requestValue(token='', ticker='', family='', group='', market='', country=Enumerations.Country.Country_Unspecified,
                 dateStart=datetime.datetime.today().date(), dateEnd=datetime.datetime.today().date(), fixing=Enumerations.Fixing.EOD,
                 field='', versionType=Enumerations.VersionType.Version_Unspecified, author='',
                 version='', quality=Enumerations.Quality.Quality_Unspecified, timeOut=300, timeFrecuency=0.5, fileName='', format='dataFrame'):
    field = Enumerations.FieldType.fromString(field)
    service = ServiceRequestDataPointValue.ServiceRequestDataPointValue.create(ticker, family, group, market, country, dateStart, dateEnd, fixing, field, versionType, author, version, quality)
    token = Arguments.tokenReader(token)
    url = service.getResponse(token)
    response = download(token, url, timeOut, timeFrecuency, format)
    Output.writeFile(fileName, response)
    return response

def requestReport(token='', document='', item='', chapter='', section='', subsection='', paragraph='',
                  dateStart=datetime.datetime.today().date(), dateEnd=datetime.datetime.today().date(), fixing=Enumerations.Fixing.EOD,
                  field='', versionType=Enumerations.VersionType.Version_Unspecified, author='',
                  version='', quality=Enumerations.Quality.Quality_Unspecified, timeOut=300, timeFrecuency=0.5, fileName='', format='dataFrame'):
    field = Enumerations.FieldType.fromString(field)
    service = ServiceRequestDataPointReport.ServiceRequestDataPointReport.create(document, item, chapter, section, subsection, paragraph, dateStart, dateEnd, fixing, field, versionType, author, version, quality)
    token = Arguments.tokenReader(token)
    url = service.getResponse(token)
    response = download(token, url, timeOut, timeFrecuency, format)
    Output.writeFile(fileName, response)
    return response

def download(token='', path='', timeOut=300, timeFrecuency=0.5, format='dataFrame'):
    response = ServiceRequestDownload.ServiceRequestDownload.request(token, path, timeOut, timeFrecuency)
    try:
        format = Enumerations.Format.fromString(format)
        response = Format.jsonToFormat(format, response)
    except:
        print('Response is not values or reports, therefore it will be returned raw.')
    return response

if __name__=='__main__':
    if not len(sys.argv) > 1:
        token = Arguments.tokenReader()
        # Request Banco de Chile stock price
        response = request(token, ticker='CHILE')
    else:
        # For command line execution
        args = Arguments.parseArguments()
        country, dateStart, dateEnd, fixing, fieldType, versionType, quality = Arguments.checkArguments(args)
        # Service
        if args.service == 'r':
            request = request(args.token, args.ticker, args.family, args.group, args.market, country, dateStart, dateEnd, fixing, fieldType, versionType, args.author, args.version, quality, args.timeOut, args.timeFrecuency, args.filepath)
