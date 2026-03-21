#!/usr/bin/python3
import requests
import re
import os
import csv
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
from datetime import date, UTC
today = date.today()
todate = datetime.datetime.strftime(today, "%d-%m-%Y")

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
subscriptionId = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
envt = ''   #QA/DEV/PROD
dirpath = r"C:\New_tech\\" + envt + "\\DBRK_JOB_RUN_TIME\\" + envt + "_"
dirpath1 = r"C:\New_tech\\" + envt + "\\DBRK_ALL_WKSP_DETAILS\\" + envt + "_"
file2 = open(""+dirpath+"databricks_all_job_details.csv", 'w')
print(f"Workspace_Name, Job_ID, Job_Name, Job_ID1, Run_ID, Lifecycle_State, Result_State, Job_Start_Time, Job_End_Time, Last_Run_Time, Databricks_URL", file=file2)
#print("Workspace_Name",",","Job_ID",",","Job_Name",",","Last_Run_Time",",","Databricks_URL",file=file2)

# Replace these variables with your Databricks workspace URL and personal access token

databricks_token = ''
# Function to get job details
def get_job_details():
    with open(""+dirpath1+"workspace_name_url.txt" ,'r') as file1:
        file_content = file1.read().splitlines()
        for line in file_content:
            databricks_url = line.strip("\n").split()
            jobs_url = f"https://{databricks_url[0]}/api/2.1/jobs/list"
            workspace_name = {databricks_url[1]}
            print(f"{jobs_url}")
            headers = { 'Content-Type': 'application/json',
                "Authorization": f"Bearer {databricks_token}"
                }
            payload = {}
            response = requests.get(jobs_url, headers=headers, data=payload, verify=False)
            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                print(f"{jobs}")
                job_details = []
                for job in jobs:
                    job_id = job.get("job_id")
                    job_name = job.get("settings", {}).get("name")
                    job_runs_url = f"https://{databricks_url[0]}/api/2.1/jobs/runs/list?job_id={job_id}&limit=1"
                    print(f"{job_runs_url}")
                    headers1 = { 'Content-Type': 'application/json',
                        "Authorization": f"Bearer {databricks_token}"
                    }
                    payload1 = {}
                    runs_response = requests.get(job_runs_url, headers=headers1, data=payload1, verify=False)

                    if runs_response.status_code == 200:
                        runs = runs_response.json().get("runs", [])
                        print(f"{runs}")
                        if runs:
                            last_run_time = runs[0].get("start_time")
                            run_id = runs[0].get('run_id')
                            job_details.append({
                                "job_id": job_id,
                                "job_name": job_name,
                                "run_id": run_id,
                                "last_run_time": last_run_time
#                               "Databricks_URL": databricks_url[0]
                            })
                            print(f"{job_id}, {job_name}, {run_id}")
                            for job in job_details:
                                #job_id = job["job_id"]
                                if job["job_id"] is None:
                                    job_id = None
                                else:
                                    job_id = job["job_id"]
                                    headers1 = {
                                        "Authorization": f"Bearer {databricks_token}"
                                    }
                                    print(f"https://{databricks_url[0]}/api/2.1/jobs/runs/get?run_id={run_id}")
                                    status_url = f"https://{databricks_url[0]}/api/2.1/jobs/runs/get?run_id={run_id}"
                                    response1 = requests.get(status_url, headers=headers1)

                                    if response1.status_code == 200:
                                        job_status = response1.json()
                                        if job_status:
                                            print("Job Status:")
                                            #job_id = "\'" + str(job_id) + "\'"
                                            job_id1 = job_status['job_id']
                                            #job_id1 = "\'" + str(job_id1) + "\'"
                                            run_id = job_status['run_id']
                                            #run_id = "\'" + str(run_id) + "\'"
                                            lifecycle_state = job_status['state']['life_cycle_state']
                                            result_state = job_status['state'].get('result_state', 'N/A')
                                            start_time = job_status['start_time']
                                            #start_time = "\'" + str(start_time) + "\'"
                                            end_time = job_status.get('end_time', 'N/A')
                                            #end_time = "\'" + str(end_time) + "\'"
                                    else:
                                        print(f"Failed to get job status: {response1.status_code}, {response1.text}")
                                        job["job_name"] = None  ##New line
                                        ##return None
                                #job_name = job["job_name"]
                                if job["job_name"] is None:
                                    job_name = None
                                    last_run_time = None
                                    job_id = None
                                    job_id1 = None
                                    run_id = None
                                    start_time = None
                                    end_time = None                                    
                                else:
                                    job_name = job["job_name"]
                                #last_run_time = convert_timestamp(job["last_run_time"])
                                if job["last_run_time"] is None:
                                    last_run_time = None
                                    job_id = "\'" + str(job_id) + "\'"
                                    job_id1 = "\'" + str(job_id1) + "\'"
                                    run_id = "\'" + str(run_id) + "\'"
                                    start_time = "\'" + str(start_time) + "\'"
                                    end_time = "\'" + str(end_time) + "\'"
                                else:
                                    last_run_time = convert_timestamp(job["last_run_time"])
                                    job_id = "\'" + str(job_id) + "\'"
                                    job_id1 = "\'" + str(job_id1) + "\'"
                                    run_id = "\'" + str(run_id) + "\'"
                                    start_time = "\'" + str(start_time) + "\'"
                                    end_time = "\'" + str(end_time) + "\'"
                                print(f"{databricks_url[1]}, {job_id}, {job_name}, {job_id1}, {run_id}, {lifecycle_state}, {result_state}, {start_time}, {end_time}, {last_run_time}, {databricks_url[0]}", file=file2)
                                #print(f"Job ID: {job_id}, Job Name: {job_name}, Last Run Time: {last_run_time}")
                                
                    #return job_details
            else:
                print(f"Failed to get job list: {response.status_code}, {response.text}")
                return []

# Function to convert timestamp to readable format
def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000, UTC).strftime('%Y-%m-%d %H:%M:%S')
            
def texttocsv():           
#    account = pd.read_csv(""+dirpath+"databricks_sort_run_job_details.txt", delimiter = ',')
    account = pd.read_csv(""+dirpath+"databricks_running_job_details.txt", delimiter = ',')
# store dataframe into csv file 
    account.to_csv(""+dirpath+"dbrk_run_job_details.csv", index = None)

def insert_header_in_csv():
    header = ["Workspace_Name","Job_ID","Job_Name","Last_Run_Time","Databricks_URL"]
    # Read the existing CSV file
    with open(""+dirpath+"dbrk_run_job_details.csv", 'r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
        
        # Write the new CSV file with the header
    with open(""+dirpath+"dbrk_header_run_job_details.csv", 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header
        writer.writerow(header)
        # Write the original rows
        writer.writerows(rows)

def sort_unique_file():
    with open(""+dirpath+"databricks_all_job_details.csv", 'r') as file:
        lines = file.readlines()

    # Remove duplicates and sort the lines
    unique_sorted_lines = sorted(set(line.strip() for line in lines))

    # Write the sorted unique lines to the output file
    with open(""+dirpath+"dbrk_final_all_job_details_"+todate+".csv", 'w') as file:
        for line in unique_sorted_lines:
            file.write(line + '\n')

def main():
    get_job_details()
    file2.close()
#    texttocsv()
#    insert_header_in_csv()
    sort_unique_file() ##This function is not running correctly
    
if __name__ == "__main__":
    main()