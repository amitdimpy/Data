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
http_proxy = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
https_proxy = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
no_proxy = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# Set the environment variables for proxies
os.environ['HTTP_PROXY'] = http_proxy
os.environ['HTTPS_PROXY'] = https_proxy
os.environ['NO_PROXY'] = no_proxy
# Replace these variables with your Databricks workspace URL and personal access token
#databricks_url = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TENANT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
subscriptionId = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
envt = ''   #QA/DEV/PROD
dirpath = r"C:\New_tech\\" + envt + "\\DBRK_USERS\\" + envt + "_"
databricks_url = [ '','','' ]
databricks_name = [ '','','' ]
databricks_token = ''
file2 = open(""+dirpath+"dbrk_users_list.txt" ,'w')
file1 = open(""+dirpath+"dbrk_users_list_"+todate+".csv", 'w')
print("Databricks_Name",",","User_ID",",","User_Name",",","Display_Name",",","Databricks_URL",file=file1)
# Function to list users in Databricks
def list_users():
    headers = {
        "Authorization": f"Bearer {databricks_token}"
    }
    url_count = len(databricks_url)
    count = 0
    while count < url_count:
        users_url = f"{databricks_url[count]}/api/2.0/preview/scim/v2/Users"
        dbrk_nm = f"{databricks_name[count]}"
        response = requests.get(users_url, headers=headers)
        if response.status_code == 200:
            users = response.json().get("Resources", [])
            for user in users:
                user_id = user.get("id")
                user_id1="\'" + str(user_id) + "\'"
                user_name = user.get("userName")
                display_name = user.get("displayName")
                print(f"{dbrk_nm},{user_id1},{user_name},{display_name},{users_url}", file=file1)
#            return users
        else:
            print(f"Failed to get users: {response.status_code}, {response.text}")
            return []
        
        count += 1

def texttocsv(): 
    account = pd.read_csv(""+dirpath+"dbrk_users_list.txt", delimiter = ',')

# store dataframe into csv file 
    account.to_csv(""+dirpath+"dbrk_users_list_"+todate+".csv", index=None)
    
def texttocsvnew():
#   header = ["Workspace_Name","Job_ID","Job_Name","Last_Run_Time","Databricks_URL"]
    # Read the existing CSV file
    with open(""+dirpath+"dbrk_users_list.txt", 'r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
        
        # Write the new CSV file with the header
    with open(""+dirpath+"dbrk_users_list_"+todate+".csv", 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header
#        writer.writerow(header)
        # Write the original rows
        writer.writerows(rows)
    
# Get the list of users and print them
list_users()
#texttocsvnew()
#texttocsv()
