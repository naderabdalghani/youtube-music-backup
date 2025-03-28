from google_auth_oauthlib.flow import InstalledAppFlow

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        scopes=["https://www.googleapis.com/auth/youtube.readonly"]
    )
    creds = flow.run_local_server(port=0)
    return creds

if __name__ == "__main__":
    creds = get_credentials()
    print("Access Token:", creds.token)
    print("Refresh Token:", creds.refresh_token)
    print("Client ID:", creds.client_id)
    print("Client Secret:", creds.client_secret)
