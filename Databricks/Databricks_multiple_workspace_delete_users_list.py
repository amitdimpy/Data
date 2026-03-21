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

# Replace these variables with your Databricks workspace URL and personal access token
databricks_url = "" 
databricks_token = ""

# List of user IDs to delete
user_ids = [ 'XXXXX', 'XXXXX', 'XXXXX', 'XXXXX' ]
    # Add more user IDs as needed

# Function to delete a user in Databricks
def delete_user(user_id):
    headers = {
        "Authorization": f"Bearer {databricks_token}"
    }
    delete_url = f"{databricks_url}/api/2.0/preview/scim/v2/Users/{user_id}"
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        print(f"Successfully deleted user with ID: {user_id}")
    else:
        print(f"Failed to delete user with ID: {user_id}, Status Code: {response.status_code}, Response: {response.text}")

# Delete users
for user_id in user_ids:
    delete_user(user_id)