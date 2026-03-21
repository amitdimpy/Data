import requests
import json

# Replace these variables with your Databricks workspace details
DATABRICKS_INSTANCE = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
API_TOKEN = ""

# Define the API endpoint to list SQL warehouses
endpoint = f'{DATABRICKS_INSTANCE}/api/2.0/sql/warehouses'

# Set up the headers with the API token for authentication
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# Make the GET request to the Databricks API
response = requests.get(endpoint, headers=headers)

# Check the response status
if response.status_code == 200:
    # Parse the JSON response
    warehouses_info = response.json()
    
    # Print the warehouse IDs and their names
    print("SQL Warehouses:")
    for warehouse in warehouses_info['warehouses']:
        print(f"Warehouse ID: {warehouse['id']}, Name: {warehouse['name']}")
else:
    print(f"Failed to retrieve warehouse information. Status code: {response.status_code}")
    print(f"Response: {response.text}")