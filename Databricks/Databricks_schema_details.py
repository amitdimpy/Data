import requests
import json

# Replace these variables with your Databricks workspace details
DATABRICKS_INSTANCE = 'XXXXXXXXXXXXXXXXXX'
API_TOKEN = ''

# Define the API endpoint to list schemas
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
    schemas_info = response.json()
    
    # Print the schemas
    print("Schemas:")
    for schema in schemas_info['warehouses']:
        print(f"Schema Name: {schema['name']}")
else:
    print(f"Failed to retrieve schemas information. Status code: {response.status_code}")
    print(f"Response: {response.text}")