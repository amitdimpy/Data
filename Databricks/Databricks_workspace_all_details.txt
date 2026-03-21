#!/usr/bin/python3
import requests
import re
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import json
import sys
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import base64
import plumbum
import datetime
from datetime import date

# Define global variables
http_proxy = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
https_proxy = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
no_proxy = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
# Set the environment variables for proxies
os.environ['HTTP_PROXY'] = http_proxy
os.environ['HTTPS_PROXY'] = https_proxy
os.environ['NO_PROXY'] = no_proxy
# Define global variables
TENANT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
mgmttoken = ''
dbrktoken = ''
subscriptionId = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'  
envt = 'XXXXX' #QA/PROD/DEV
dirpath = r"C:\\New_tech\\" + envt + "\\DBRK_ALL_WKSP_DETAILS\\" + envt + "_"
file6 = open(""+dirpath+"all_job_information.txt" ,'w')
file7 = open(""+dirpath+"inaccessible_URLs.txt" ,'w')
file8 = open(""+dirpath+"accessible_URLs.txt" ,'w')
file11 = open(""+dirpath+"jobid_URLs.txt" ,'w')
file12 = open(""+dirpath+"jobid_details.txt" ,'w')
file13 = open(""+dirpath+"access_job_url.txt" ,'w')
today = date.today()
todate = datetime.datetime.strftime(today, "%d-%m-%Y")

# Function to retrieve databricks workspaces   
def getwksp():
    file1 = open (""+dirpath+"workspace_list.txt", 'w')
    file9 = open (""+dirpath+"workspace_name.txt", 'w')
    file14 = open (""+dirpath+"workspace_name_url.txt", 'w')
    url = f'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Databricks/workspaces?api-version=2023-02-01'
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + mgmttoken
        }
    response = requests.get(url=url,headers = headers)
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        file1 = open (""+dirpath+"workspace_list.txt", 'a')
        file9 = open (""+dirpath+"workspace_name.txt", 'a')
        file14 = open (""+dirpath+"workspace_name_url.txt", 'a')
        # Iterate over the list of workspaces
        for wks in data.get('value', []):
            print(wks['properties']['workspaceUrl'], file = file1)
            print(wks['name'], file = file9)
            print(wks['properties']['workspaceUrl'],wks['name'], file = file14)
    else:
        print(f"Failed to retrieve workspaces: {response.status_code} - {response.text}", file= file1)   
    file2 = open(""+dirpath+"workspace_url.txt",'w')
    file3 = open(""+dirpath+"workspace_url.txt",'a')
    file11 = open(""+dirpath+"jobid_URLs.txt" ,'a')
    file13 = open(""+dirpath+"access_job_url.txt" ,'a')
    with open(""+dirpath+"workspace_list.txt", 'r') as file1:
        file_content = file1.read().splitlines()
        for line in file_content:
            line1 = line.strip("\n")
            print ("https://"+line1+"/api/2.1/jobs/list", file=file3)
            print ("https://"+line1+"/api/2.1/jobs/get", file=file11)
            print ("https://"+line1+"/jobs/", file=file13)

# To retrieve job execution details which are deployed in the databricks            
def getdbrkjoblist():
    file5 = open (""+dirpath+"dbrk_final_job_list.txt", 'w')
    file9 = open (""+dirpath+"workspace_name.txt", 'r')
    file10 = open (""+dirpath+"workspace_namelist.txt", 'w') 
    file_line1 = file9.read().splitlines()
    for line in file_line1:
        wksp = line.strip("\n")
        file10 = open (""+dirpath+"workspace_namelist.txt", 'a')
        print(wksp, file = file10)
    countline = 0
    cntln = 0
    cntjb = 0
    print("Job_ID",",","Workspace_Name",",","Job_Name",",","App_Tag",",","Feature_Tag",",","Layer_Tag",",","Access_URL",",","Job_Creater_Name",",","Spark_Version",",","Node_Type",",","Workers_Count",",","Sched_Status",",","Sched_Job",file=file5)
    with open(""+dirpath+"workspace_url.txt",'r') as file3:
        file4 = open(""+dirpath+"dbrk_joblist.txt", 'w')
        file6 = open(""+dirpath+"all_job_information.txt" ,'a')
        file_line = file3.read().splitlines()
        for line in file_line:
            with open(""+dirpath+"workspace_namelist.txt",'r') as wkp1:
                linecount = len(wkp1.readlines())
                linecount += 1
                ##print (linecount)
            with open(""+dirpath+"workspace_name.txt",'r') as wkp:
                Lines = wkp.read().splitlines()
                if countline <= linecount:
                    wkspnm = Lines[countline]
            params = { "expand_tasks": True }
            has_more = True
            while has_more:
                file4 = open(""+dirpath+"dbrk_joblist.txt", 'w')  ## 2-Nov-2024
                url = line.strip("\n")
                payload={}
                headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + dbrktoken
                    }
                response1 = requests.request("GET", url, headers=headers, data=payload, params=params, verify=False)
                data = json.loads(response1.text)
                json_string = json.dumps(data)
                response1_json = response1.json()
                print (response1.json(), file=file6)
                next_page_token = response1_json.get("next_page_token")
                print (wkspnm, url, next_page_token, countline, linecount)
                print ("============") 
                params['page_token'] = next_page_token
                if response1.status_code != 200:
                    file7 = open(""+dirpath+"inaccessible_URLs.txt" ,'a')
                    print(url, wkspnm, response1.status_code, todate, file = file7)
                elif response1.status_code == 200:
                    file8 = open(""+dirpath+"accessible_URLs.txt" ,'a')
                    print (response1.text, file = file4)
                    data = json.loads(response1.text)
                    file5 = open (""+dirpath+"dbrk_final_job_list.txt", 'a')
                    json_string = json.dumps(data)
                    word = "job_id"
                    su_nm = json_string.lower().count(word.lower())
                    print(url, wkspnm, response1.status_code, su_nm, todate, file= file8)
                    count=0
                    while count < int(su_nm):
                        with open(""+dirpath+"dbrk_joblist.txt", 'r') as jobid:
                            data = json.loads(response1.text)
                            json_string = json.dumps(data)
                            job_id1=data['jobs'][count]['job_id']
                            url1 = open(""+dirpath+"jobid_URLs.txt" ,'r')
                            lncnt = len(url1.readlines())
                            ##print ("lncnt:", lncnt)   ## 2-Nov-24
                            with open(""+dirpath+"jobid_URLs.txt" ,'r') as url2:
                                Llines = url2.read().splitlines()
                            cntln += 1
                            llines = Llines[countline]
                            print ("llines :", llines)   ## 2-Nov-24
                            geturl = ""+ llines +"?job_id=" + str(job_id1)
                            print ("geturl:", geturl)    ##29-Oct-2024
                            print ("============")    ##29-Oct-2024
                            url3 = open(""+dirpath+"access_job_url.txt" ,'r')
                            lncnt1 = len(url3.readlines())
                            with open(""+dirpath+"access_job_url.txt" ,'r') as url4:
                                Lljobs = url4.read().splitlines()
                            cntjb +=1
                            lljobs = Lljobs[countline]
                            print ("lljobs :", lljobs)
                            joburl = ""+ lljobs +"" + str(job_id1)
                            job_id="\'" + str(job_id1) + "\'"
                            job_name=data['jobs'][count]['settings']['name']
                            try:
                                app_tag=data['jobs'][count]['settings']['tags']['XXXX']
                            except KeyError:
                                app_tag=None
                            try:
                                app_tag1=data['jobs'][count]['settings']['tags']['XXXX']
                            except KeyError:
                                app_tag1=None
                            try:
                                feature_tag=data['jobs'][count]['settings']['tags']['XXXX']
                            except KeyError:
                                feature_tag=None
                            try:
                                feature_tag1=data['jobs'][count]['settings']['tags']['XXXX']
                            except KeyError:
                                feature_tag1=None
                            try:
                                layer_tag=data['jobs'][count]['settings']['tags']['XXXX']
                            except KeyError:
                                layer_tag=None
                            try:
                                layer_tag1=data['jobs'][count]['settings']['tags']['XXXX']
                            except KeyError:
                                layer_tag1=None
                            if app_tag == None:
                                app_tag=app_tag1
                            if feature_tag == None:
                                feature_tag=feature_tag1
                            if layer_tag == None:
                                layer_tag=layer_tag1   
                            tim=data['jobs'][count]['created_time'] 
                            tim1=str(int(tim))[:10]
                            cret_tim=datetime.datetime.fromtimestamp(int(tim1)).strftime('%d-%b-%Y')
                            try:
                                creator_name = data['jobs'][count]['creator_user_name']
                            except KeyError:
                                creator_name = None
                            try:
                                status_job = data['jobs'][count]['settings']['continuous']['pause_status']
                                sched_status = "Continuous"
                            except KeyError:
                                try:
                                    status_job = data['jobs'][count]['settings']['schedule']['pause_status']
                                    sched_status = "Schedule"
                                except KeyError:
                                    try:
                                        status_job = data['jobs'][count]['settings']['trigger']['pause_status']
                                        sched_status = "Trigger"
                                    except KeyError:
                                        status_job = None
                                        sched_status = None
                            payload2 = {}
                            headers2 = {'Authorization': 'Bearer ' + dbrktoken
                                    }
                            response2 = requests.request("GET", geturl, headers=headers2, data=payload2, verify=False)
                            file15 = open(""+dirpath+"jobid_details_info.txt" ,'w')
                            print(response2.text.encode('utf8'), file = file15)
                            data = json.loads(response2.text.encode('utf8'))
                            json_string = json.dumps(data)
                            if response2.status_code == 200:
                                try:
                                    spk_version = data['settings']['job_clusters'][0]['new_cluster']['spark_version']
                                except KeyError:
                                    spk_version = None
                                try:
                                    node_type = data['settings']['job_clusters'][0]['new_cluster']['node_type_id']
                                except KeyError:
                                    node_type = None
                                try:
                                    num_wrk = data['settings']['job_clusters'][0]['new_cluster']['num_workers']
                                except KeyError:
                                    num_wrk = None
                            elif response2.status_code != 200:
                                spk_version = "URL not accessible"
                                node_type = "URL not accessible"
                                num_wrk = "URL not accessible"
                            count+=1
                            print(job_id,",",wkspnm,",",job_name,",",app_tag,",",feature_tag,",",layer_tag,",",joburl,",",creator_name,",",spk_version,",",node_type,",",num_wrk,",",sched_status,",",status_job, file = file5)
                if not next_page_token:
                    has_more = False   
                    countline += 1                        

    with open(""+dirpath+"dbrk_final_job_list.txt",'r') as file5:
        file5_content = file5.read()

def texttocsv():           
    account = pd.read_csv(""+dirpath+"dbrk_final_job_list.txt", delimiter = ',')
# store dataframe into csv file 
    account.to_csv(""+dirpath+"dbrk_final_job_list_"+todate+".csv", index = None)
    
def main():
    getwksp()
    getdbrkjoblist()
    texttocsv()

if __name__ == "__main__":
    main()