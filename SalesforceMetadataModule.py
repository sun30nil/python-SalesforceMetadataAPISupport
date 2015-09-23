from xml.etree.ElementTree import XML, fromstring, tostring
import os
import time
import base64
import csv
import zipfile
import traceback
import time
import requests
import subprocess
import getpass
import xmltodict


__author__ = "Sunil Singh"
__copyright__ = "Copyright 2015, The Metadata API Project"
__credits__ = ["Anil Kumar Ganivada"]
__version__ = "0.1"
__maintainer__ = "Sunil Singh"
__email__ = "sun30nil@gmail.com"
__status__ = "Development"

# some basic default settings for this class

# setting the xpath prefix for the xml tag
_xPathXlmns = './/{http://soap.sforce.com/2006/04/metadata}'
# current version of the api is v34.0
_salesforceURL = 'https://login.salesforce.com/services/Soap/c/34.0'
# enterprise xml name space
_enterpriseXlmns = './/{urn:enterprise.soap.sforce.com}'

# sudo easy_install requests[security] # this installs necessary
# certificates for requests


class SalesforceMetadataModule:
    sessionId = ""
    metadataServerUrl = ""
    serverUrl = ""
    userId = ""
    currencySymbol = ""
    orgAttachmentFileSizeLimit = ""
    orgDefaultCurrencyIsoCode = ""
    orgDisallowHtmlAttachments = ""
    organizationId = ""
    organizationName = ""
    profileId = ""
    sessionSecondsValid = ""
    userEmail = ""
    userFullName = ""
    userLanguage = ""
    userLocale = ""
    userName = ""
    userTimeZone = ""
    userType = ""
    userUiSkin = ""

    def __init__(self, username, password, s_token):
        # headers = {'content-type': 'application/soap+xml',  'SOAPAction': ''}
        headers = {'content-type': 'text/xml', 'SOAPAction': 'Create'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:enterprise.soap.sforce.com">
         <soapenv:Header>
            <urn:LoginScopeHeader>
            </urn:LoginScopeHeader>
         </soapenv:Header>
         <soapenv:Body>
            <urn:login>
               <urn:username>""" + username + """</urn:username>
               <urn:password>""" + password + s_token + """</urn:password>
            </urn:login>
         </soapenv:Body>
      </soapenv:Envelope>"""
        response = requests.post(_salesforceURL, data=body, headers=headers)
        loginResponseXml = fromstring(response.content)
        try:
            self.sessionId = loginResponseXml.find(
                _enterpriseXlmns + 'sessionId').text
            self.metadataServerUrl = loginResponseXml.find(
                _enterpriseXlmns + 'metadataServerUrl').text
            self.serverUrl = loginResponseXml.find(
                _enterpriseXlmns + 'serverUrl').text
            self.userId = loginResponseXml.find(
                _enterpriseXlmns + 'userId').text
            self.currencySymbol = loginResponseXml.find(
                _enterpriseXlmns + 'currencySymbol').text
            self.orgAttachmentFileSizeLimit = loginResponseXml.find(
                _enterpriseXlmns + 'orgAttachmentFileSizeLimit').text
            self.orgDefaultCurrencyIsoCode = loginResponseXml.find(
                _enterpriseXlmns + 'orgDefaultCurrencyIsoCode').text
            self.orgDisallowHtmlAttachments = loginResponseXml.find(
                _enterpriseXlmns + 'orgDisallowHtmlAttachments').text
            self.organizationId = loginResponseXml.find(
                _enterpriseXlmns + 'organizationId').text
            self.organizationName = loginResponseXml.find(
                _enterpriseXlmns + 'organizationName').text
            self.profileId = loginResponseXml.find(
                _enterpriseXlmns + 'profileId').text
            self.sessionSecondsValid = loginResponseXml.find(
                _enterpriseXlmns + 'sessionSecondsValid').text
            self.userEmail = loginResponseXml.find(
                _enterpriseXlmns + 'userEmail').text
            self.userFullName = loginResponseXml.find(
                _enterpriseXlmns + 'userFullName').text
            self.userLanguage = loginResponseXml.find(
                _enterpriseXlmns + 'userLanguage').text
            self.userLocale = loginResponseXml.find(
                _enterpriseXlmns + 'userLocale').text
            self.userName = loginResponseXml.find(
                _enterpriseXlmns + 'userName').text
            self.userTimeZone = loginResponseXml.find(
                _enterpriseXlmns + 'userTimeZone').text
            self.userType = loginResponseXml.find(
                _enterpriseXlmns + 'userType').text
            self.userUiSkin = loginResponseXml.find(
                _enterpriseXlmns + 'userUiSkin').text
            print '\nLogged In successfully!\n'
        except:
            traceback.print_exc()
            print "\nLogin Failed. Please try again.\n"
        pass

    def getSessionId(self):
        return self.sessionId

    def getMetadataServerUrl(self):
        return self.metadataServerUrl

    def getServerUrl(self):
        return self.serverUrl

    def getUserId(self):
        return self.userId

    def getCurrencySymbol(self):
        return self.currencySymbol

    def getOrgAttachmentFileSizeLimit(self):
        return self.orgAttachmentFileSizeLimit

    def getOrgDefaultCurrencyIsoCode(self):
        return self.orgDefaultCurrencyIsoCode

    def retrievePackage(self, members, name, api_version, outPutZipFileName):
        headers = {'content-type': 'text/xml', 'SOAPAction': 'retrieve'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:met="http://soap.sforce.com/2006/04/metadata">
      <soapenv:Header>
         <met:CallOptions>
         </met:CallOptions>
         <met:SessionHeader>
            <met:sessionId>""" + self.sessionId + """</met:sessionId>
         </met:SessionHeader>
      </soapenv:Header>
      <soapenv:Body>
         <met:retrieve>
            <met:retrieveRequest>
               <met:apiVersion>""" + api_version + """</met:apiVersion>
               <met:singlePackage>false</met:singlePackage>
               <met:unpackaged>
                  <met:types>
                     <!--Zero or more repetitions:-->
                     <met:members>""" + members + """</met:members>
                     <met:name>""" + name + """</met:name>
                  </met:types>
                  <!--Optional:-->
                  <met:version>""" + api_version + """</met:version>
               </met:unpackaged>
            </met:retrieveRequest>
         </met:retrieve>
      </soapenv:Body>
      </soapenv:Envelope>"""
        response = requests.post(
            self.metadataServerUrl, data=body, headers=headers)
        print "Retrieve Request Sent"
        retrieveResponse = response.content
        retrieveResponseXml = fromstring(retrieveResponse)
        jobId = retrieveResponseXml.find(
            './/{http://soap.sforce.com/2006/04/metadata}id').text
        print "Retrieving Job"
        jobResponse = self.retrieveJob(jobId)

        jobResponseXml = fromstring(jobResponse)
        statusOfJob = jobResponseXml.find(
            './/{http://soap.sforce.com/2006/04/metadata}status').text

        if statusOfJob == 'Succeeded':
            zipFileContent = jobResponseXml.find(
                './/{http://soap.sforce.com/2006/04/metadata}zipFile').text
            f = open(outPutZipFileName, 'wb')
            data = base64.b64decode(zipFileContent)
            f.write(data)
            f.close()
            print "Successfully created the zip file @ ", os.path.abspath(outPutZipFileName)
            return True
        else:
            print "Job Failed"
        return False

    def retrieveJob(self, processID):
        headers = {'content-type': 'text/xml', 'SOAPAction': 'retrieve'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:met="http://soap.sforce.com/2006/04/metadata">
      <soapenv:Header>
         <met:SessionHeader>
            <met:sessionId>""" + self.sessionId + """</met:sessionId>
         </met:SessionHeader>
      </soapenv:Header>
      <soapenv:Body>
         <met:checkRetrieveStatus>
            <met:asyncProcessId>""" + processID + """</met:asyncProcessId>
            <met:includeZip>true</met:includeZip>
         </met:checkRetrieveStatus>
      </soapenv:Body>
      </soapenv:Envelope>"""
        response = requests.post(
            self.metadataServerUrl, data=body, headers=headers)
        return response.content

    def listMetadata(self, metaType, asOfVersion):
        headers = {'content-type': 'text/xml', 'SOAPAction': 'retrieve'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:met="http://soap.sforce.com/2006/04/metadata">
         <soapenv:Header>
            <met:CallOptions>
            </met:CallOptions>
            <met:SessionHeader>
               <met:sessionId>""" + self.sessionId + """</met:sessionId>
            </met:SessionHeader>
         </soapenv:Header>
         <soapenv:Body>
            <met:listMetadata>
               <!--Zero or more repetitions:-->
               <met:queries>
                  <!--Optional:-->
                  <!--<met:folder>null</met:folder>-->
                  <met:type>""" + metaType + """</met:type>
               </met:queries>
               <met:asOfVersion>""" + asOfVersion + """</met:asOfVersion>
            </met:listMetadata>
         </soapenv:Body>
      </soapenv:Envelope>"""
        response = requests.post(
            self.metadataServerUrl, data=body, headers=headers)
        listOfResult = xmltodict.parse(response.content)
        return listOfResult['soapenv:Envelope']['soapenv:Body'][u'listMetadataResponse'][u'result']
