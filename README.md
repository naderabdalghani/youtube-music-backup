# YouTube Music Backup Script

This script backs up your YouTube Music playlists, including your Liked Music, into timestamped CSV files.

## Prerequisites

1. **Google Cloud Project**  
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the **YouTube Data API v3** for the project.

2. **OAuth 2.0 Credentials**  
   - Navigate to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth client ID**.
   - Set application type to **Desktop App**.
   - Download the `client_secret.json` file.
   - Note down the `client_id` and `client_secret`.

3. **Set Up a Virtual Environment**  
   - Navigate to your project directory
   - Create a virtual environment:
     ```sh
     python3 -m venv venv
     ```
   - Activate the environment:
     ```sh
     source venv/bin/activate
     ```
   - Install dependencies:
     ```sh
     pip install -r requirements.txt
     ```

4. **Get a Refresh Token**  
   - Run [get_refresh_token.py](get_refresh_token.py)
   - Copy and save the refresh token.

5. **Set Environment Variables**  
   - Open your `~/.zshrc` file:
     ```sh
     nano ~/.zshrc
     ```
   - Add the following lines:
     ```sh
     export GOOGLE_CLIENT_ID="your_client_id"
     export GOOGLE_CLIENT_SECRET="your_client_secret"
     export GOOGLE_REFRESH_TOKEN="your_refresh_token"
     ```
   - Save and exit. Apply changes:
     ```sh
     source ~/.zshrc
     ```

## Running the Script

```sh
python youtube_music_backup.py
```

This will create timestamped CSV files for each playlist, ensuring they overwrite existing ones.

## Additional Notes

- The script automatically filters out non-music videos from the Liked Music playlist.
- If running for the first time, verify OAuth authentication and grant permissions in your Google account.

## Troubleshooting

- Access blocked: “This app has not been verified”

	Go to Google Cloud Console > OAuth Consent Screen and add your Google account as a test user.

- Refresh token expired or not working

	Re-run Step 4 to generate a new refresh token.
