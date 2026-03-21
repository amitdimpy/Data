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
import shutil
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
TENANT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
subscriptionId = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
envt = ''
dirpath = r"C:\New_tech\\" + envt + "\\TAGS\\" + envt + "_"
databricks_url = [ 'XXXXXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXXXXX' ]
databricks_name = [ 'XXXXXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXXXXX' ]
#dbrk_token = 'az account get-access-token --resource XXXXXXXXXXXXXXXXXXXXXXXXXX --query "accessToken" -o tsv'
databricks_token = ""
file1 = open(""+dirpath+"dbrk_job_tags.csv", 'w')
file2 = open(""+dirpath+"dbrk_sqlwh_tags.csv", 'w')
file3 = open(""+dirpath+"dbrk_cluster_tags.csv", 'w')
file4 = open(""+dirpath+"databricks_tagging.csv", 'w')
file5 = open(""+dirpath+"databricks_tagging_final.csv", 'w')
print(f"Databricks_Name, Job_ID, Job_Name, Tags_Job, URL", file=file1)
print(f"Databricks_Name, Warehouse_ID, Warehouse_Name, Tags_Warehouse, URL", file=file2)
print(f"Databricks_Name, Cluster_ID, Cluster_Name, Tags_Cluster, URL", file=file3)
print(f"Workspace, Cluster_Type, Job_Cluster_Name, App, Layer, Feature, Error_Message", file=file4)
print(f"Workspace, Cluster_Type, Job_Cluster_Name, App, Layer, Feature, Error_Message", file=file5)
allowed_list = [ "XXXXX","XXXXX","XXXXX","XXXXX","Missing Tags" ]

def get_dbrks_tags():
    headers = {
        "Authorization": f"Bearer {databricks_token}"
    }
    url_count = len(databricks_url)
    count = 0
    while count < url_count:
        # Collecting Databricks Jobs information
        url = f"{databricks_url[count]}/api/2.0/jobs/list"
        #url = f"{databricks_url[count]}/api/2.2/jobs/list?expand_tasks"
        type = "Job"
        dbrk_nm = f"{databricks_name[count]}"
        response = requests.get(url, headers=headers)
        # Check the response status
        if response.status_code == 200:
            jobs = response.json().get('jobs', [])
            for job in jobs:
                job_id = job['job_id']
                job_name = job['settings']['name']
                jobtags = job['settings'].get('tags', {})
                print(f"{dbrk_nm},{job_id},{job_name},{jobtags},{databricks_url[count]}", file=file1)
                apptags = [value for key, value in jobtags.items() if 'tag-app' in key.lower()] if jobtags else None
                #apptags_count = len([value for key, value in jobtags.items() if 'tag-app' in key.lower()]) if jobtags else 0
                if apptags:
                    apptags = apptags[0]
                    apptags_count = apptags.count("_")
                    is_apptags_in_allowed = apptags in allowed_list
                    errormsgapp = ""
                else:
                    apptags = "Missing Tags"
                    errormsgapp = "app_is_missing"
                    apptags_count = "255"
                    is_apptags_in_allowed = "True"
                featuretags = [value for key, value in jobtags.items() if 'tag-feature' in key.lower()] if jobtags else None
                #featuretags_count = len([value for key, value in jobtags.items() if 'tag-feature' in key.lower()]) if jobtags else 0
                if featuretags:
                    featuretags = featuretags[0]
                    featuretags_count = featuretags.count("_")
                    is_apptags_in_featuretags = apptags in featuretags
                    errormsgfeat = ""
                else:
                    featuretags = "Missing Tags"
                    errormsgfeat = "feature_is_missing"
                    featuretags_count = "255"
                    is_apptags_in_featuretags = "True"
                layertags = [value for key, value in jobtags.items() if 'tag-layer' in key.lower()] if jobtags else None
                #layertags_count = len([value for key, value in jobtags.items() if 'tag-layer' in key.lower()]) if jobtags else 0
                if layertags:
                    layertags = layertags[0]
                    layertags_count = layertags.count("_")
                    is_apptags_in_layertags = apptags in layertags
                    errormsglayer = ""
                else:
                    layertags = "Missing Tags"
                    errormsglayer = "layer_is_missing"
                    layertags_count = "255"
                    is_apptags_in_layertags = "True"
                if apptags_count == 0:
                    apptags_valid = ""
                else:
                    apptags_valid = "Invalid_app_tags"
                if featuretags_count == 2:
                    featuretags_valid = ""
                else:
                    featuretags_valid = "Invalid_feature_tags"
                if layertags_count == 1:
                    layertags_valid = ""
                else:
                    layertags_valid = "Invalid_layer_tags"
                if is_apptags_in_allowed == False:
                    app_list_check = "apptag_not_in_list"
                else:
                    app_list_check = ""
                if is_apptags_in_featuretags == False:
                    app_feature_check = "apptag_featuretag_not_aligned"
                else:
                    app_feature_check = ""
                if is_apptags_in_layertags == False:
                    app_layer_check = "apptag_layertag_not_aligned"
                else:
                    app_layer_check = ""
                combined_msg = f"{errormsgapp} {errormsgfeat} {errormsglayer} {apptags_valid} {layertags_valid} {featuretags_valid} {app_list_check} {app_layer_check} {app_feature_check}"
                print(f"{dbrk_nm},{type},{job_name},{apptags},{layertags},{featuretags},{combined_msg}", file=file4)
                print(f"{dbrk_nm},{type},{job_name},{apptags},{layertags},{featuretags},{combined_msg}", file=file5)
        # Collect Databricks Warehouse Information
        url1 = f"{databricks_url[count]}/api/2.0/sql/warehouses"
        type = "SQL_WH"
        dbrk_nm = f"{databricks_name[count]}"
        response = requests.get(url1, headers=headers)
        # Check the response status
        if response.status_code == 200:
            warehouses = response.json().get('warehouses', [])
            for warehouse in warehouses:
                warehouse_id = warehouse['id']
                warehouse_name = warehouse['name']
                whtags = warehouse.get('tags', {})
                print(f"{dbrk_nm},{warehouse_id},{warehouse_name},{whtags},{databricks_url[count]}", file=file2)
                sqlapptags = [value for key, value in whtags.items() if 'tag-app' in key.lower()] if whtags else None
                #sqlapptags_count = len([value for key, value in whtags.items() if 'tag-layer' in key.lower()]) if whtags else 0
                if sqlapptags:
                    sqlapptags = sqlapptags[0]
                    sqlapptags_count = sqlapptags.count("_")
                    is_apptags_in_allowed = sqlapptags in allowed_list
                    print(apptags_valid)
                    errormsgapp = ""
                else:
                    sqlapptags = "Missing Tags"
                    errormsgapp = "app_is_missing"
                    sqlapptags_count = "255"
                    is_apptags_in_allowed = "True"
                sqlfeattags = [value for key, value in whtags.items() if 'tag-feature' in key.lower()] if whtags else None
                #sqlfeattags_count = len([value for key, value in whtags.items() if 'tag-feature' in key.lower()]) if whtags else 0
                if sqlfeattags:
                    sqlfeattags = sqlfeattags[0]
                    sqlfeattags_count = sqlfeattags.count("_")
                    is_apptags_in_featuretags = sqlapptags in sqlfeattags
                    errormsgfeat = ""
                else:
                    sqlfeattags = "Missing Tags"
                    errormsgfeat = "feature_is_missing"
                    sqlfeattags_count = "255"
                    is_apptags_in_featuretags = "True"
                sqllayertags = [value for key, value in whtags.items() if 'tag-layer' in key.lower()]  if whtags else None
                #sqllayertags_count = len([value for key, value in whtags.items() if 'tag-layer' in key.lower()]) if whtags else 0
                if sqllayertags:
                    sqllayertags = sqllayertags[0]
                    sqllayertags_count = sqllayertags.count("_")
                    is_apptags_in_layertags = sqlapptags in sqllayertags
                    errormsglayer = ""
                else:
                    sqllayertags = "Missing Tags"
                    errormsglayer = "layer_is_missing"
                    sqllayertags_count = "255"
                    is_apptags_in_layertags = "True"
                if sqlapptags_count == 0:
                    apptags_valid = ""
                else:
                    apptags_valid = "Invalid_app_tags"
                if sqlfeattags_count == 2:
                    featuretags_valid = ""
                else:
                    featuretags_valid = "Invalid_feature_tags"
                if sqllayertags_count == 1:
                    layertags_valid = ""
                else:
                    layertags_valid = "Invalid_layer_tags"
                if is_apptags_in_allowed == False:
                    app_list_check = "apptag_not_in_list"
                else:
                    app_list_check = ""
                if is_apptags_in_featuretags == False:
                    app_feature_check = "apptag_featuretag_not_aligned"
                else:
                    app_feature_check = ""
                if is_apptags_in_layertags == False:
                    app_layer_check = "apptag_layertag_not_aligned"
                else:
                    app_layer_check = ""
                combined_msg = f"{errormsgapp} {errormsgfeat} {errormsglayer} {apptags_valid} {layertags_valid} {featuretags_valid} {app_list_check} {app_layer_check} {app_feature_check}"
                print(f"{dbrk_nm},{type},{warehouse_name},{sqlapptags},{sqllayertags},{sqlfeattags},{combined_msg}", file=file4)
                print(f"{dbrk_nm},{type},{warehouse_name},{sqlapptags},{sqllayertags},{sqlfeattags},{combined_msg}", file=file5)
        # Collect Databricks Cluster Information
        url2 = f"{databricks_url[count]}/api/2.0/clusters/list"
        dbrk_nm = f"{databricks_name[count]}"
        type = "Cluster"
        found = False
        response = requests.get(url2, headers=headers)
        # Check the response status
        if response.status_code == 200:
            clusters = response.json().get('clusters', [])
            for cluster in clusters:
                cluster_id = cluster['cluster_id']
                cluster_name1 = cluster['cluster_name']
                if not cluster_name1.lower().startswith('job-'):
                    cluster_name = cluster_name1
                    clustags = cluster.get('custom_tags', {})
                    print(f"{dbrk_nm},{cluster_id},{cluster_name},{clustags},{databricks_url[count]}", file=file3)
                    clusapptags = [value for key, value in clustags.items() if 'tag-app' in key.lower()] if clustags else None
                    if clusapptags:
                        clusapptags = clusapptags[0]
                        clusapptags_count = clusapptags.count("_")
                        is_apptags_in_allowed = clusapptags in allowed_list
                        errormsgapp = ""
                    else:
                        clusapptags = "Missing Tags"
                        errormsgapp = "app_is_missing"
                        clusapptags_count = "255"
                        is_apptags_in_allowed = "True"
                    clusfeattags = [value for key, value in clustags.items() if 'tag-feature' in key.lower()] if clustags else None
                    if clusfeattags:
                        clusfeattags = clusfeattags[0]
                        clusfeattags_count = clusfeattags.count("_")
                        is_apptags_in_featuretags = clusapptags in clusfeattags
                        errormsgfeat = ""
                    else:
                        clusfeattags = "Missing Tags"
                        errormsgfeat = "feature_is_missing"
                        clusfeattags_count = "255"
                        is_apptags_in_featuretags = "True"
                    cluslayertags = [value for key, value in clustags.items() if 'tag-layer' in key.lower()] if clustags else None
                    if cluslayertags:
                        cluslayertags = cluslayertags[0]
                        cluslayertags_count = cluslayertags.count("_")
                        is_apptags_in_layertags = clusapptags in cluslayertags
                        errormsglayer = ""
                    else:
                        cluslayertags = "Missing Tags"
                        errormsglayer = "layer_is_missing"
                        cluslayertags_count = "255"
                        is_apptags_in_layertags = "True"
                    if clusapptags_count == 0:
                        apptags_valid = ""
                    else:
                        apptags_valid = "Invalid_app_tags"
                    if clusfeattags_count == 2:
                        featuretags_valid = ""
                    else:
                        featuretags_valid = "Invalid_feature_tags"
                    if cluslayertags_count == 1:
                        layertags_valid = ""
                    else:
                        layertags_valid = "Invalid_layer_tags"
                    if is_apptags_in_allowed == False:
                        app_list_check = "apptag_not_in_list"
                    else:
                        app_list_check = ""
                    if is_apptags_in_featuretags == False:
                        app_feature_check = "apptag_featuretag_not_aligned"
                    else:
                        app_feature_check = ""
                    if is_apptags_in_layertags == False:
                        app_layer_check = "apptag_layertag_not_aligned"
                    else:
                        app_layer_check = ""
                    combined_msg = f"{errormsgapp} {errormsgfeat} {errormsglayer} {apptags_valid} {layertags_valid} {featuretags_valid} {app_list_check} {app_layer_check} {app_feature_check}"
                    print(f"{dbrk_nm},{type},{cluster_name},{clusapptags},{cluslayertags},{clusfeattags},{combined_msg}", file=file4)
                    print(f"{dbrk_nm},{type},{cluster_name},{clusapptags},{cluslayertags},{clusfeattags},{combined_msg}", file=file5)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
        count += 1

def uniq_column():
    # Path to your CSV file
    output_file = ""+dirpath+"databricks_tagging_final.csv"
    df = pd.read_csv(output_file)
    first_three_cols = df.columns[:3]
    df_unique = df.drop_duplicates(subset=first_three_cols, keep='first', inplace=True)
    #print(df_unique)

    # Optionally, save the filtered DataFrame to a new CSV
    #output_file = ""+dirpath+"databricks_tagging_final.csv"
    #df_unique.to_csv(output_file, index=False)
    #print(df_unique.to_csv)

    #print(f"Filtered CSV saved to {output_file}")
    
get_dbrks_tags()  
uniq_column()              

