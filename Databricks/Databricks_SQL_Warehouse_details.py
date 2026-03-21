import requests
import json
import datetime
import os
import pandas as pd
from datetime import date
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
# Replace these variables with your Databricks workspace details
databricks_url = [ '' ]
databricks_name = [ '' ]
databricks_token = ''
TENANT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
subscriptionId = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
envt = ''   #QA/DEV/PROD
dirpath = r"C:\New_tech\\" + envt + "\\DBRK_ALL_WKSP_DETAILS\\" + envt + "_"
file1 = open(""+dirpath+"SQL_WAREHOUSE_ID_LIST.csv" ,'w')
file2 = open(""+dirpath+"SQL_WAREHOUSE_INFO_DETAILS.csv", 'w')
file3 = open(""+dirpath+"SQL_WAREHOUSE_ALL_DETAILS_"+todate+".csv" ,'w')
input_csv_file = ""+dirpath+"SQL_WAREHOUSE_INFO_DETAILS.csv"
output_csv_file = ""+dirpath+"SQL_WAREHOUSE_ALL_DETAILS_"+todate+".csv"
print(f"Databricks_Name, Warehouse_ID, Warehouse_Name", file=file1)
print(f"Databricks_Name, Warehouse_ID, Warehouse_Name, Warehouse_State, Cluster_size, Max_Num_Clusters, Num_Active_sess, Num_Run_Queries, Num_Queue_Queries, Num_Fail_Queries", file=file2)

def warehouse_id_det():
    headers = {
        "Authorization": f"Bearer {databricks_token}",
        'Content-Type': 'application/json'
    }
    url_count = len(databricks_url)
    count = 0
    while count < url_count:   
        sql_url = f"{databricks_url[count]}/api/2.0/sql/warehouses"
        dbrk_nm = f"{databricks_name[count]}"
        print(sql_url,dbrk_nm)
        response = requests.get(sql_url, headers=headers)
        if response.status_code == 200:
        # Parse the JSON response
            warehouses_info = response.json()
    
        # Print the warehouse IDs and their names
            print("SQL Warehouses:")
            for warehouse in warehouses_info['warehouses']:
                print(f"{dbrk_nm}, {warehouse['id']}, {warehouse['name']}", file=file1)
                WAREHOUSEID = warehouse['id']
                print(WAREHOUSEID)
                endpoint = f"{databricks_url[count]}/api/2.0/sql/warehouses/{WAREHOUSEID}"
                #print(endpoint)
                headers1 = {
                    'Authorization': f'Bearer {databricks_token}',
                    'Content-Type': 'application/json'
                }
                response1 = requests.get(endpoint, headers=headers1)
                if response1.status_code == 200:
                    # Parse the JSON response
                    sql_ware_info = response.json()
                    #print(sql_ware_info)
                    for wareho in sql_ware_info['warehouses']:
                        W_ID = wareho['id']
                        print(W_ID)
                        W_NAME = wareho['name']
                        W_STATE = wareho['state']
                        try:
                            C_SIZE = wareho['cluster_size']
                        except KeyError:
                            C_SIZE = None
                        try:
                            CLUS_NUM = wareho['max_num_clusters']
                        except KeyError:
                            CLUS_NUM = None
                        try:
                            ACT_SESS = wareho['num_active_sessions']
                        except KeyError:
                            ACT_SESS = None
                        try:
                            RUN_QUE = wareho['num_running_queries']
                        except KeyError:
                            RUN_QUE = None
                        try:
                            QUE_QUE = wareho['num_queued_queries']
                        except KeyError:
                            QUE_QUE = None
                        try:
                            FAI_QUE = wareho['num_failed_queries']
                        except KeyError:
                            FAI_QUE = None
                        print(f"{dbrk_nm},{W_ID}, {W_NAME}, {W_STATE},{C_SIZE}, {CLUS_NUM}, {ACT_SESS}, {RUN_QUE}, {QUE_QUE}, {FAI_QUE}", file=file2)
                else:
                    print(f"Failed to retrieve all warehouse information from {dbrk_nm}. Status code: {response.status_code}")
                    #print(f"Response: {response.text}")
        else:
            print(f"Failed to retrieve SQL warehouse ID information from {dbrk_nm}. Status code: {response.status_code}")
            #print(f"Response: {response.text}")
        count += 1
        
def unique_lines():
    file1.close()
    file2.close()
    file3.close()
    # 1. Read CSV
    df = pd.read_csv(input_csv_file)

    # 2(a). For complete row duplicate
    df_cleaned = df.drop_duplicates()
    #pd.drop_duplicates(inplace=True)

# 3. Save then
    df_cleaned.to_csv(output_csv_file, index=False)

warehouse_id_det()
unique_lines()