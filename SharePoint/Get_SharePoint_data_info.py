import msal
import requests
import os

# Azure AD and Graph API configuration
# Define global variables
http_proxy = 'XXXXXXXXXX'
https_proxy = 'XXXXXXXXXX'
no_proxy = 'XXXXXXXXXX'
# Set the environment variables for proxies
os.environ['HTTP_PROXY'] = http_proxy
os.environ['HTTPS_PROXY'] = https_proxy
os.environ['NO_PROXY'] = no_proxy
# Azure AD and Graph API configuration

TENANT_ID = "XXXXXXXXXX"
CLIENT_ID = "XXXXXXXXXX"
CLIENT_SECRET = "XXXXXXXXXX"
SHAREPOINT_SITE_ID = "XXXXXXXXXX"
SITE_ID = "XXXXXXXXXX"
DRIVE_ID = "XXXXXXXXXX"
SCOPE = ['https://graph.microsoft.com/.default']

# SharePoint site and drive info
START_FOLDER_PATH = '/Shared Documents'  # Starting folder path

def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f'https://login.microsoftonline.com/{TENANT_ID}',
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(f"Could not obtain access token: {result.get('error_description')}")

def list_items_recursive(access_token, site_id, drive_id, folder_path, indent=0):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    folder_path_encoded = folder_path.replace(' ', '%20')
    url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:{folder_path_encoded}:/children'

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")

    items = response.json().get('value', [])
    for item in items:
        prefix = ' ' * indent * 2
        if 'folder' in item:
            print(f"{prefix}📁 {item['name']}/")
            # Recursive call for subfolder
            subfolder_path = folder_path.rstrip('/') + '/' + item['name']
            list_items_recursive(access_token, site_id, drive_id, subfolder_path, indent + 1)
        else:
            print(f"{prefix}📄 {item['name']}")

if __name__ == '__main__':
    token = get_access_token()
    print(f"Listing files and folders starting at: {START_FOLDER_PATH}\n")
    list_items_recursive(token, SITE_ID, DRIVE_ID, START_FOLDER_PATH)