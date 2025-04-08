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
    with open(".env", "w") as f:
        f.write(f"REFRESH_TOKEN={creds.refresh_token}\n")
        f.write(f"CLIENT_ID={creds.client_id}\n")
        f.write(f"CLIENT_SECRET={creds.client_secret}\n")
