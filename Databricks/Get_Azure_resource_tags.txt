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
import csv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Define global variables
http_proxy = 'XXXXXXXXXXXXXXXXXX'
https_proxy = 'XXXXXXXXXXXXXXXXXX'
no_proxy = 'XXXXXXXXXXXXXXXXXX'
# Set the environment variables for proxies
os.environ['HTTP_PROXY'] = http_proxy
os.environ['HTTPS_PROXY'] = https_proxy
os.environ['NO_PROXY'] = no_proxy
TENANT_ID = 'XXXXXXXXXXXXXXXXXX'
SUBSCRIPTION_ID = "XXXXXXXXXXXXXXXXXX"
envt = ""   #QA/PROD/DEV
dirpath = r"C:\New_tech\\" + envt + "\\TAGS\\" + envt + "_"
allowed_list = [ "XXXX","XXXX","XXXX","Missing Tags" ]
file1 = open(""+dirpath+"azure_all_res_tag.csv", 'w')
file2 = open(""+dirpath+"azure_check_all_tags.csv", 'w')
file3 = open(""+dirpath+"apptags.csv", "w")
file4 = open(""+dirpath+"featuretags.csv", "w")
file5 = open(""+dirpath+"layertags.csv", "w")

def list_resources_with_details(subscription_id):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Initialize the Resource Management Client
    resource_client = ResourceManagementClient(credential, subscription_id)

    #print(f"Listing resources in subscription: {subscription_id}\n")
    print(f"Resource Name, Resource Type, Location, Resource Group, App, Layer, Feature, Error Message", file=file1)

    # List all resources in the subscription
    resource_details = []
    for resource in resource_client.resources.list():
        resource_info = {
            "Resource Name": resource.name,
            "Resource Type": resource.type,
            "Location": resource.location,
            "Resource Group": resource.id.split("/")[4],  # Extract the resource group from the resource ID
            "Tags": resource.tags
        }
        resource_details.append(resource_info)

        # Print resource details
        print(f"Resource Name: {resource_info['Resource Name']}", file=file2)
        print(f"Resource Type: {resource_info['Resource Type']}", file=file2)
        print(f"Location: {resource_info['Location']}", file=file2)
        print(f"Resource Group: {resource_info['Resource Group']}", file=file2)
        print(f"Tags: {resource_info['Tags']}", file=file2)
        resname = resource_info['Resource Name']
        restype = resource_info['Resource Type']
        location = resource_info['Location']
        resgroup = resource_info['Resource Group']
        Tags = resource_info['Tags']
        print(f"{Tags}", file=file2)
        apptags = [value for key, value in Tags.items() if 'tag-app' in key.lower()] if Tags else None       
        featuretags = [value for key, value in Tags.items() if 'tag-feature' in key.lower()] if Tags else None       
        layertags = [value for key, value in Tags.items() if 'tag-layer' in key.lower()] if Tags else None
        if apptags:
            apptags = apptags[0]
            apptags_count = apptags.count("_")
            is_apptags_in_allowed = apptags in allowed_list
            errormsgapp = ""
            print(f"{apptags}", file=file3)
        else:
            apptags = "Missing Tags"
            errormsgapp = "app_is_missing"
            print(f"{apptags}", file=file3)
        if featuretags:
            featuretags = featuretags[0]
            featuretags_count = featuretags.count("_")
            is_apptags_in_featuretags = apptags in featuretags
            errormsgfeat = ""
            print(f"{featuretags}", file=file4)
        else:
            featuretags = "Missing Tags"
            errormsgfeat = "feature_is_missing"
            print(f"{featuretags}", file=file4)
        if layertags:
            layertags = layertags[0]
            layertags_count = layertags.count("_")
            is_apptags_in_layertags = apptags in layertags
            errormsglayer = ""
            print(f"{layertags}", file=file5)
        else:
            layertags = "Missing Tags"
            errormsglayer = "layer_is_missing"
            print(f"{layertags}", file=file5)
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
        print(f"{resname},{restype},{location},{resgroup},{apptags},{layertags},{featuretags},{combined_msg}", file=file1)
        #print("-" * 50)

    return resource_details

def dbrk_rm_snapshot():
    exclude_keywords = ["Microsoft.Compute/snapshots", "Microsoft.ManagedIdentity"]
# Input and output file paths
    input_csv = ""+dirpath+"azure_all_res_tag.csv"
    output_csv = ""+dirpath+"azure_resources_tagging_final.csv"

# Open the input and output files
    with open(input_csv, "r") as infile, open(output_csv, "w", newline="") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
    
    # Write the header row
        header = next(reader)
        writer.writerow(header)
    
        for row in reader:
            if not any(keyword in ",".join(row) for keyword in exclude_keywords):
                writer.writerow(row)

def export_to_csv(resource_details, filename=""+dirpath+"azure_resources_tagging_final.csv"):
    keys = resource_details[0].keys()  # Get the column names
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(resource_details)

    print(f"Resource details exported to {filename}")
    
if __name__ == "__main__":
    resources = list_resources_with_details(SUBSCRIPTION_ID)
    dbrk_rm_snapshot()
    #export_to_csv(resources)