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
from datetime import date, UTC

databricks_url = "XXXXXXXXXXXXXXXXXXXXXXX"
databricks_token = ""

# Function to get job details
def get_job_details():
    headers = {
        "Authorization": f"Bearer {databricks_token}"
    }
    jobs_url = f"{databricks_url}/api/2.1/jobs/list"
    response = requests.get(jobs_url, headers=headers)

    if response.status_code == 200:
        jobs = response.json().get("jobs", [])
        job_details = []

        for job in jobs:
            job_id = job.get("job_id")
            job_name = job.get("settings", {}).get("name")
            job_runs_url = f"{databricks_url}/api/2.1/jobs/runs/list?job_id={job_id}&limit=1"
            runs_response = requests.get(job_runs_url, headers=headers)

            if runs_response.status_code == 200:
                runs = runs_response.json().get("runs", [])
                if runs:
                    last_run_time = runs[0].get("start_time")
                    job_details.append({
                        "job_id": job_id,
                        "job_name": job_name,
                        "last_run_time": last_run_time
                    })

        return job_details
    else:
        print(f"Failed to get job list: {response.status_code}, {response.text}")
        return []

# Function to convert timestamp to readable format
def convert_timestamp(timestamp):
#    from datetime import datetime
    return datetime.datetime.fromtimestamp(timestamp / 1000, UTC).strftime('%Y-%m-%d %H:%M:%S')
#    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Get job details and print them
job_details = get_job_details()
for job in job_details:
    job_id = job["job_id"]
    job_name = job["job_name"]
    last_run_time = convert_timestamp(job["last_run_time"])
    print(f"Job ID: {job_id}, Job Name: {job_name}, Last Run Time: {last_run_time}")