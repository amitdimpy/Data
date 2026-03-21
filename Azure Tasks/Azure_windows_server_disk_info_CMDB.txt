#!/usr/bin/python3
# Purpose : Fetch details of disks assigned on Azure Windows server from CMDB server

import requests
import re
import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import base64
from plumbum.cmd import cat, jq, grep, wc, sed, awk, paste, uniq, sort, head
from datetime import date

# To get the token from CMDB PROD server 
def get_auth_token():

    url = "https://CMDB-server.com:8443/rest-api/authenticate"
    payload = json.dumps({
        "username": "adm",
        #"password": (base64.b64decode("UmVzdEFwIU").decode("utf-8")),
        "password": "Restpass",
        "clientContext": 1
    })
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    if response.status_code == 200:
        auth = response.json()
        auth1 = json.dumps(auth['token'])
        token = auth1.strip('"')
        return token

# To get the CI details of Azure Windows server discovered in CMDB
def win_ci_details(token):

    ciurl = "https://CMDB-server.com:8443/rest-api/exposeCI/getInformation?isGlobalId=false"
    payload1 = json.dumps({
        "type": "nt",
        "includeSubtypes": "false",
        "layout": [
            "name",
            "st_location_site"
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
    response1 = requests.request("POST", ciurl, headers=headers1, data=payload1, verify=False)
    file1 = open("/home/PYTHON/AZURE/logs/azure_windows_server_disk_size_info.txt","w")
    print(response1.text, file=file1)
    file1.close()
    file3 = open("/home/PYTHON/AZURE/logs/ud_azvm.txt","w")
    file3.close()
    for data in response1.json():
      ud_id=data['CMDBId']
      try:
         ud_name=data['properties']['name']
      except KeyError:
         ud_name=None
      file2 = open("/home/PYTHON/AZURE/logs/id_name.txt","w")
      print (ud_id,ud_name, file=file2)
      file2.close()
      file2 = open("/home/PYTHON/AZURE/logs/id_name.txt","r")
      file3 = open("/home/PYTHON/AZURE/logs/ud_azvm.txt","a")
      for patrn in file2:
        if re.search ("azu", patrn):
          print(patrn, file=file3)
      file2.close()
      file3.close();

# To remove column of server name from the collected list
def spl_col():
    res=re.compile(r'\s+')
    fil=open('/home/PYTHON/AZURE/logs/ud_azvm.txt','r')
    file4 = open('/home/PYTHON/AZURE/logs/CMDB_id_list.txt','w')
    for f in fil:
      splitcomp=re.sub(res," ",f).strip().split(' ')
      file4.write(splitcomp[0].strip() + "\n")

# To remove blank lines from the list of collected CMDB ID's
def rem_blnk():
    blank=''
    file5 = open('/home/PYTHON/AZURE/logs/ud_final_id.txt' , 'w')
    with open('/home/PYTHON/AZURE/logs/CMDB_id_list.txt') as txt:
      txt=txt.read().split('\n')
      for line in txt:
        if line is not blank: print(line , file=file5)
    file5 = open('/home/PYTHON/AZURE/logs/ud_final_id.txt' , 'r')
    file5.close();

# To get token from CMDB, collect data from CMDB ID's, collect data related to disk drive, disk size, free space. To process the collected data to calculate the disk usage and free percent.
def ci_data(token):
    with open('/home/PYTHON/AZURE/logs/ud_final_id.txt', 'r') as ciid:
      for udcid in ciid:
       udcid = udcid.strip()
       idurl = "https://CMDB-server.com:8443/rest-api/dataModel/relatedCI/"+udcid+""
       payload2 = json.dumps({})
       headers2 = { \
            'Content-Type': 'application/json', \
            'Accept': 'application/json', \
            'Authorization': "Bearer " + token
               }
       file6 = open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","w")
       response2 = requests.request("GET", idurl, headers=headers2, data=payload2, verify=False)
       print (response2.text,file=file6)
       data1 = json.loads(response2.text)
       if([data1['cis'][0]['properties']['TenantsUses'][0]] == [ "WWDC - World Wide DataCenter" ]):
         try:
           line_number = 0
           with open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","r") as cidet:
             file7 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".mt_pt","w")
             file8 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".dk_sz","w")
             file9 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".fr_sp","w")
             for line in cidet:
                  line_number += 1
                  target_number = '"type" : "file_system"'
                  if target_number in line:
                       fir_num = line_number
                       last_num = fir_num + 82
                       lin1 = fir_num + 64
                       lin2 = fir_num + 66
                       lin3 = fir_num + 77
                       mt_pt = open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","r").readlines()[lin1]
                       mt_pt = mt_pt.strip('"mount_point" : "')
                       mt_pt = mt_pt.strip('",\n')
                       dk_sz = open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","r").readlines()[lin2]
                       dk_sz = dk_sz.strip('"disk_size" : "')
                       dk_sz = dk_sz.strip('",\n')
                       fr_sp = open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","r").readlines()[lin3]
                       fr_sp = fr_sp.strip('"free_space" : "')
                       fr_sp = fr_sp.strip('",\n')
                       us_pe = (float(100.00) - float(fr_sp))
                       us_pe = round(us_pe,2)
                       us_sp = ((float(dk_sz) * float(us_pe)) / 100)
                       us_sp = round(us_sp,2)
                       fr_pe = float(fr_sp)
                       fr_pe = round(fr_pe,2)
                       fr_sp = (float(dk_sz) - float(us_sp))
                       today = date.today()
                       file7 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".mt_pt","a") 
                       print(mt_pt,",", file=file7)
                       file8 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".dk_sz","a")
                       print(dk_sz,",",us_sp,",", file=file8)
                       file9 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".fr_sp","a")
                       print(fr_sp,",",us_pe,",",fr_pe,",",today,file=file9)

           with open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","r") as sudet:
             file15 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".su_nm","w")
#             su_nm = (cat ["/home/PYTHON/AZURE/logs/UDID/"+udcid+""] | grep ["data_tags"] | grep ["ST-Env-Type"] | head ["-1"] | awk ["-FST-Env-Type",'{print $2}'] | awk ["-F:", '{print $2}'] | awk ["-F,", '{print $1}'] | sed ['s#\\"##g'])()
             su_nm = (cat ["/home/PYTHON/AZURE/logs/UDID/"+udcid+""] | grep ["data_tags"] | grep ["ST-Env"] | head ["-1"] | awk ["-FST-Env-Type",'{print $2}'] | awk ["-F:", '{print $2}'] | awk ["-F,", '{print $1}'] | sed ['s#\\"##g'])()
             su_nm = su_nm.strip()
             sunm_ln = len(su_nm)
             if (sunm_ln != 0):
               su_nm = su_nm.strip(' \\')
               su_nm = su_nm.strip('\\\n')
               print(su_nm,",", file=file15)
             else:
#               su_nm = (cat ["/home/PYTHON/AZURE/logs/UDID/"+udcid+""] | grep ["data_tags"] | grep ["ST-Env-Type"] | head ["-1"] | awk ["-FST-Environment",'{print $2}'] | awk ["-F:", '{print $2}'] | awk ["-F,", '{print $1}'] | sed ['s#\\"##g'])()
               su_nm = (cat ["/home/PYTHON/AZURE/logs/UDID/"+udcid+""] | grep ["data_tags"] | grep ["ST-Env"] | head ["-1"] | awk ["-FST-Environment",'{print $2}'] | awk ["-F:", '{print $2}'] | awk ["-F,", '{print $1}'] | sed ['s#\\"##g'])()
               su_nm = su_nm.strip()
               sunm_ln = len(su_nm)
               if (sunm_ln != 0):
                 su_nm = su_nm.strip(' \\')
                 su_nm = su_nm.strip('\\\n')
                 print(su_nm,",", file=file15)
               else: 
                 su_nm = None
                 print(su_nm,",", file=file15)

           with open("/home/PYTHON/AZURE/logs/UDID/"+udcid+"","r") as rgdet:
             file10 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".rg_nm","w")
             rg_nm = (cat ["/home/PYTHON/AZURE/logs/UDID/"+udcid+""] | grep ["cloud_instance_id"] | awk ["-F/", '{print $5,$NF}'] | awk ["-F\"", '{print $1}'] | sed ['s# #,#g'])()
             rgnm_ln = len(rg_nm)
             if (rgnm_ln == 0):
               rg_nm = None
               print(rg_nm,",", file=file10)
             else:
               rg_nm = rg_nm.replace(' ',',')
               rg_nm = rg_nm.strip()
               print(rg_nm,",", file=file10)

           with open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".mt_pt","r") as cntmt,open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".rg_nm","r") as cntrg,open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".su_nm","r") as cntsu:
             cnt_mt = cntmt.readlines()
             cn_mt = len(cnt_mt)
             cnt_rg = cntrg.readlines()
             cn_rg = len(cnt_rg)
             cnt_su = cntsu.readlines()
             cn_su = len(cnt_su)
             while (cn_mt > cn_rg):
               fir_ln = cntrg.readline()
               file10 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".rg_nm","a")
               print(rg_nm,",", file=file10)
               cn_rg += 1
             while (cn_mt > cn_su):
               file15 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".su_nm","a")
               print(su_nm,",", file=file15)
               cn_su += 1

         except KeyError:
           ud_info=None
           print(ud_info)

# To create a file which contains data in desired format,arrange the collected data from text file, remove the empty files. 
def ci_data_paste():
    with open('/home/PYTHON/AZURE/logs/ud_final_id.txt', 'r') as ciid:
      file17 = open("/home/PYTHON/AZURE/logs/azure_win_disk_final_info.txt","w")
      print("Envt",",","RG_Name",",","Svr_Name",",","Disk_Drive",",","Disk_Size(MB)",",","Used_Space(MB)",",","Free Space(MB)",",","Used%",",","Free%",",","Date",file=file17)
      for udcid in ciid:
       udcid = udcid.strip()
       file7 = "/home/PYTHON/AZURE/logs/DATA/"+udcid+".mt_pt"
       file8 = "/home/PYTHON/AZURE/logs/DATA/"+udcid+".dk_sz"
       file9 = "/home/PYTHON/AZURE/logs/DATA/"+udcid+".fr_sp"
       file15 = "/home/PYTHON/AZURE/logs/DATA/"+udcid+".su_nm"
       file10 = "/home/PYTHON/AZURE/logs/DATA/"+udcid+".rg_nm"
       file_size = os.path.getsize(file7)
       file_size1 = os.path.getsize(file8)
       file_size2 = os.path.getsize(file9)
       file_size3 = os.path.getsize(file15)
       file_size4 = os.path.getsize(file10)
       if (((file_size == 0) and (os.path.exists(file7))) or ((file_size1 == 0) and (os.path.exists(file8))) or ((file_size2 == 0) and (os.path.exists(file9))) or ((file_size3 == 0) and (os.path.exists(file15))) or ((file_size4 == 0) and (os.path.exists(file10)))):
         os.remove(file7)
         os.remove(file8)
         os.remove(file9)
         os.remove(file15)
         os.remove(file10)
       else:
         file7 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".mt_pt","r")
         file8 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".dk_sz","r")
         file9 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".fr_sp","r")
         file10 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".rg_nm","r")
         file15 = open("/home/PYTHON/AZURE/logs/DATA/"+udcid+".su_nm","r")
         file17 = open("/home/PYTHON/AZURE/logs/azure_win_disk_final_info.txt","a") 
         ps_fl = (paste ["/home/PYTHON/AZURE/logs/DATA/"+udcid+".su_nm","/home/PYTHON/AZURE/logs/DATA/"+udcid+".rg_nm","/home/PYTHON/AZURE/logs/DATA/"+udcid+".mt_pt","/home/PYTHON/AZURE/logs/DATA/"+udcid+".dk_sz", "/home/PYTHON/AZURE/logs/DATA/"+udcid+".fr_sp"])()
         ps_fl = ps_fl.strip()
         print(ps_fl, file=file17)

# To copt the text file to csv file and mail it to desired users
def copy_mail():
    os.chdir("/home/PYTHON/AZURE/logs/")
    today = date.today()
    sr_fl = "azure_win_disk_final_info.txt"
    ds_fl = "azure_win_vm_details."+str(today)+".csv"
    os.rename(sr_fl,ds_fl)
    subject = "Azure Windows Server Disk Storage Usage Information"
    body = "Hello All, \n\nAttached report contains the Azure Windows Server Disk Usage Details of all subscriptions.\n\nIt provides information for FINOPS. \n\nRegards, \n\nTEST"
    sender_email = "FIN@" + os.uname()[1] + ".abcd.com"
    receiver_email = "XXXXXs@abcd.com"
    cc_email = "YYYY@abcd.com"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Cc"] = cc_email
#    rcpt_email = cc_email.split(",") + [receiver_email]
    rcpt_email = receiver_email.split(",") + [cc_email]
    message.attach(MIMEText(body, "plain"))
    filename = ds_fl
    with open(filename, "rb") as attachment:
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
      "Content-Disposition",
      f"attachment; filename= {filename}",
    )
    message.attach(part)
    text = message.as_string()
    with smtplib.SMTP("localhost", 25) as server:
      server.sendmail(sender_email, rcpt_email, text)

def main():
    win_ci_details(get_auth_token())
    spl_col()
    rem_blnk()
    ci_data(get_auth_token())
    ci_data_paste()
    copy_mail()

if __name__ == "__main__":
    main()

