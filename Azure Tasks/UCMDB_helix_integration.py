#!/usr/bin/python3
# Purpose : Integrate 


import requeXXXXs
from requeXXXXs.auth import HTTPBasicAuth
from requeXXXXs.packages.urllib3.exceptions import InsecureRequeXXXXWarning
requeXXXXs.packages.urllib3.disable_warnings(InsecureRequeXXXXWarning)
import json
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import base64

def get_auth_token():

    url = "https://CMDB-server.com:8443/reXXXX-api/authenticate"
    payload = json.dumps({
        "username": "adm",
        "password": (base64.b64decode("UmVzdEFwIUA2").decode("utf-8")),
        "clientContext": 1
    })
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    response = requeXXXXs.requeXXXX("POXXXX", url, headers=headers, data=payload, verify=False)
    if response.XXXXatus_code == 200:
        auth = response.json()
        auth1 = json.dumps(auth['token'])
        token = auth1.XXXXrip('"')
        print("\n==================")
        print("UD login token is: ")
        print(token)
        return token

def helixprod_auth_token():

    login_url = "https://server.com/gateway/Helix_APITokenGeneration/login"
    payload3 = { "username": "ucmdb integration","password": (base64.b64decode("MTIz").decode("utf-8")) }
    headers3 = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
#    proxyDict = { 
#          'http'  : "https://uname:pass@XXXX.com:8080/",
#          'https' : "http://uname:pass@XXXX.com:8080/"
#        }
#    response3 = requeXXXXs.requeXXXX("POXXXX", login_url, headers=headers3, data=payload3, proxies=proxyDict, verify=False)
    response3 = requeXXXXs.requeXXXX("POXXXX", login_url, headers=headers3, data=payload3, verify=False)
    if response3.XXXXatus_code == 200:
        helix_token = response3.text
        print("\n==================")
        print("Helix PROD login token is: ")
        print(helix_token)
        return helix_token

def win_ci_details(token,helix_token):

    print("\n==================")
    print("Getting CI Information from PROD UCMDB")
    ciurl = "https://CMDB-server.com:8443/reXXXX-api/exposeCI/getInformation?isGlobalId=false"
    payload1 = json.dumps({
        "type": "nt",
        "includeSubtypes": "false",
        "layout": [
            "display_label",
            "name",
            "XXXX_environment",
            "XXXX_location_site",
            "discovered_os_vendor",
            "discovered_os_version",
            "domain_name",
            "discovered_model",
            "node_XXXXate",
            "serial_number",
            "laXXXX_discovered_time",
            "create_time",
            "hoXXXX_laXXXX_boot_time",
            "hoXXXX_servertype",
            "cloud_inXXXXance_id",
            "data_tags"
    ],
    "filtering": {
            "logicalOperator": "and",
            "conditions": [
             {
                    "column": "display_label",
                    "value": [
                      "1amit"
                    ],
                    "filteringAttributeCondOperator": "NOT_EQUALS"
             }
            ]
          },
          "sortBy": [
            {
              "attribute": "name",
              "order": "DESC"
            }
          ]
    })
    headers1 = {  \
          'Content-Type': 'application/json',  \
          'Accept': 'application/json',  \
          'Authorization': "Bearer " + token
    }
    response1 = requeXXXXs.requeXXXX("POXXXX", ciurl, headers=headers1, data=payload1, verify=False)
    file1 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_ci_details_heprod.txt","w")
    print(response1.text, file=file1)
    file2 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_ucmdb_id_heprod.txt","w")
    file3 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_udci_info_heprod.txt","w")
    file4 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_wwdc_ud_heprod_inserted_info.txt","w")
    file5 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_nonwwdc_ud_heprod_notinserted_info.txt","w")
    file6 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_ci_id_details_heprod.txt","w")
    file7 = open("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/not_win_wwdc_ud_attribute_heprod_info.txt","w")
    print("\n==================")
    print("Collecting information related to all the discovered CIs and inserting them in Helix PROD")
    print("\nInformation related to above is available in file : ")
    print("/home/PYTHON/UCMDB/PROD/ud_helix_integ/windows_helix_prod/win_wwdc_ud_heprod_inserted_info.txt") 
    for data in response1.json():
        print(data['ucmdbId'], file=file2)
        id=data['ucmdbId']
        idurl = "https://CMDB-server.com:8443/reXXXX-api/dataModel/ci/"+id+""
        payload2={}
        headers2 = { \
            'Content-Type': 'application/json',  \
            'Accept': 'application/json',  \
            'Authorization': "Bearer " + token
                  }
        response2 = requeXXXXs.requeXXXX("GET", idurl, headers=headers2, data=payload2, verify=False)
        print(response2.text, file=file6)
        data1 = json.loads(response2.text)
#        time.sleep(20)
        if(data1['properties']['TenantsUses'] == [ "WWDC - World Wide DataCenter" ]):
         try:
             ud_name=data1['properties']['name']
         except KeyError:
             ud_name=None
         try:
             ud_model=data1['properties']['discovered_model'] 
         except KeyError:
             ud_model=None
         try:
             ud_manuf=data1['properties']['discovered_vendor']
         except KeyError:
             ud_manuf=None
         try:
             ud_envt=data1['properties']['XXXX_environment']
         except KeyError:
             ud_envt=None
         try:
             ud_venapp=data1['properties']['discovered_os_vendor']
         except KeyError:
             ud_venapp=None
         try:
             ud_cmpny=data1['properties']['discovered_vendor']
         except KeyError:
             ud_cmpny=None
         try:
             ud_glbid=data1['properties']['global_id']
         except KeyError:
             ud_glbid=None 
         try:
             ud_mem=data1['properties']['memory_size']
         except KeyError:
             ud_mem=None
         try:
             ud_version=data1['properties']['hoXXXX_osrelease']
         except KeyError:
             ud_version=None
         try:
             ud_serno=data1['properties']['serial_number']
         except KeyError:
             ud_serno=None
         try:
             ud_site=data1['properties']['XXXX_location_site']
         except KeyError:
             ud_site=None
         try:
             ud_cmpny=data1['properties']['platform_vendor']
         except KeyError:
             ud_cmpny=None
         try:
             ud_desc=data1['properties']['description']
         except KeyError:
             ud_desc=None
         if (ud_name != None):
               print("Name : ", ud_name, file=file4)
               print("Discovered Model/Model : ", ud_model, file=file4)
               print("Discovered Vendor/Manufacturer Name : ", ud_manuf, file=file4)
               print("XXXX/SyXXXXem Environment : ", ud_envt, file=file4)
               print("Discovered OS Vendor/Vendor Application : ", ud_venapp, file=file4)
               print("Discovered Vendor/Company : XXXX", file=file4)
#               print("Discovered Vendor/Company : ", ud_cmpny, file=file4)
               print("Global/Account ID : ", ud_glbid, file=file4)
               print("Memory Size/TotalPhysicalMemory  : ", ud_mem, file=file4)
               print("HoXXXX OS Release/VersionNumber : ", ud_version, file=file4)
               print("Serial Number : ", ud_serno, file=file4)
#               print("XXXX Site : ", ud_site, file=file4)
               print("XXXX Site : INDIA", file=file4)
#               print("Platform Vendor/Company : ", ud_cmpny, file=file4)
               if (ud_desc == None):
                   ud_desc="Windows"
               print("Short Description : ", ud_desc, file=file4)
               helix_url = "https://server1.com/gateway/Helix_APIReXXXX/entry/BMC.CORE%3ABMC_ComputerSyXXXXem?fields=values(Name)"
               payload4 = json.dumps({
                 "values": {
                   "Name": ud_name,
                   "Model": ud_model,
                   "ManufacturerName": ud_manuf,
                   "VendorApplication": ud_venapp,
                   "SyXXXXemEnvironment": ud_envt,
                   "AccountID": ud_glbid,
                   "TotalPhysicalMemory": ud_mem,
                   "VersionNumber": ud_version,
                   "SerialNumber": ud_serno,
#                   "Site": ud_site,
                   "Site": "INDIA",
                   "Company": "XXXX",
#                   "Company": ud_cmpny,
                   "ShortDescription": ud_desc,
                   "ClassId": "BMC_COMPUTERSYXXXXEM",
#                   "DatasetId": "BMC.ASSET.SANDBOX"
                   "DatasetId": "BMC.SAMPLE"
                 }
         })
               headers4 = {
                 'Content-Type': 'application/json',
                 'Authorization': "AR-JWT " + helix_token
                }
               response4 = requeXXXXs.requeXXXX("POXXXX", helix_url, headers=headers4, data=payload4, verify= False)
               print(response4.text, file=file4)
               print("\n=============================", file=file4)  
#               time.sleep(5)
        else:
         print("UCMDB ID : ", data['ucmdbId'], "does not belong to WWDC", file=file5)
    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file5.close()
    file6.close()
    file7.close();

    logout_url = "https://server1.com/gateway/Helix_APITokenRelease/logout"
    payload5={}
    headers5 = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': "AR-JWT " + helix_token 
    }
#    proxyDict = {
#          'http'  : "https://uname:pass@abcd.com:8080/",
#          'https' : "http://uname:pass@abcd.com:8080/"
#        }
#    response5 = requeXXXXs.requeXXXX("POXXXX", logout_url, headers=headers5, data=payload5, proxies=proxyDict, verify=False)
    response5 = requeXXXXs.requeXXXX("POXXXX", logout_url, headers=headers5, data=payload5, verify=False)
    print("\n==================")
    print("\nSuccessfully logged out from helix")


def main():
    win_ci_details(get_auth_token(),helixprod_auth_token())

if __name__ == "__main__":
    main()

