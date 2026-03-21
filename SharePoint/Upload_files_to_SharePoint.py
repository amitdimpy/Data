import os
import requests
from msal import ConfidentialClientApplication

# Define global variables
http_proxy = 'XXXXXXXXXXXXXXXXXXXXXXX'
https_proxy = 'XXXXXXXXXXXXXXXXXXXXXXX'
no_proxy = 'XXXXXXXXXXXXXXXXXXXXXXX'
# Set the environment variables for proxies
os.environ['HTTP_PROXY'] = http_proxy
os.environ['HTTPS_PROXY'] = https_proxy
os.environ['NO_PROXY'] = no_proxy
# Azure AD and SharePoint configuration
TENANT_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
##################
CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
CLIENT_SECRET = "XXXXXXXXXXXXXXXXXXXXXXX"
SHAREPOINT_SITE_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
SITE_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
DRIVE_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
folder_id = "XXXXXXXXXXXXXXXXXXXXXXX"
DOCUMENT_LIBRARY_ID = "XXXXXXXXXXXXXXXXXXXXXXX"  # e.g., drive id for 'Documents'
FOLDER_PATH = "TMXXXXXXXXXXXXXXXXXXXXXXXAP"
# Path to the local folder containing files to upload
LOCAL_FILES_PATH = r"C:\Users\TEST"

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Failed to acquire token: {result.get('error_description')}")

def upload_file_to_folder(access_token, file_path, file_name):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    folder_path_encoded = FOLDER_PATH.replace(" ", "%20")
    #upload_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE_ID}/drives/{DOCUMENT_LIBRARY_ID}/root:/{file_name}:/content"
    upload_url = (
        f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{file_name}:/content"
    )
    print(upload_url)
    with open(file_path, "rb") as file_data:
        response = requests.put(upload_url, headers=headers, data=file_data)
    print(response.status_code)
    if response.status_code in [200, 201]:
        print(f"Uploaded '{file_name}' successfully.")
    else:
        print(f"Failed to upload '{file_name}': {response.status_code} - {response.text}")

def main():
    token = get_access_token()
    files = os.listdir(LOCAL_FILES_PATH)
    for file_name in files:
        file_path = os.path.join(LOCAL_FILES_PATH, file_name)
        if os.path.isfile(file_path):
            upload_file_to_folder(token, file_path, file_name)



if __name__ == "__main__":
    main()