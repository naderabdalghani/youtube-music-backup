import os
import csv
import datetime
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def authenticate():
    """Authenticate using environment variables from Zsh."""
    creds = Credentials.from_authorized_user_info({
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    return build("youtube", "v3", credentials=creds)

def fetch_playlist_items(service, playlist_id):
    """Fetch all music-related videos from a given playlist ID."""
    videos = []
    next_page_token = None

    while True:
        request = service.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [item["contentDetails"]["videoId"] for item in response.get("items", [])]
        
        # Fetch category IDs for videos
        if video_ids:
            video_details_request = service.videos().list(
                part="snippet",
                id=",".join(video_ids)
            )
            video_details_response = video_details_request.execute()

            valid_video_ids = {
                item["id"]: item["snippet"]["categoryId"]
                for item in video_details_response.get("items", [])
                if item["snippet"]["categoryId"] == "10"  # Category 10 is Music
            }

            for item in response.get("items", []):
                snippet = item["snippet"]
                content_details = item["contentDetails"]
                video_id = content_details["videoId"]

                # Check if the video belongs to the Music category
                if video_id in valid_video_ids or " - Topic" in snippet.get("videoOwnerChannelTitle", ""):
                    videos.append({
                        "title": snippet["title"],
                        "videoId": video_id,
                        "channel": snippet.get("videoOwnerChannelTitle", "Unknown")
                    })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def fetch_all_playlists(service):
    """Fetch user's YouTube Music playlists including Liked Music."""
    playlists = []
    next_page_token = None

    while True:
        request = service.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get("items", []):
            playlists.append({
                "title": item["snippet"]["title"],
                "playlistId": item["id"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    # Manually add the Liked Music playlist
    playlists.append({"title": "Liked Music", "playlistId": "LL"})

    return playlists

def sanitize_filename(name):
    """Ensure filenames are safe by removing invalid characters."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()

def export_to_csv(data, filename):
    """Export playlist data to a CSV file with UTF-8 encoding."""
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "videoId", "channel"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    service = authenticate()

    # Fetch all playlists including "Liked Music"
    playlists = fetch_all_playlists(service)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    for playlist in playlists:
        print(f"Fetching playlist: {playlist['title']}")
        playlist_songs = fetch_playlist_items(service, playlist["playlistId"])

        # Generate a timestamped, safe filename
        safe_playlist_name = sanitize_filename(playlist["title"])
        filename = f"{safe_playlist_name}_{today}.csv"

        # Save data to CSV
        export_to_csv(playlist_songs, filename)
        print(f"✅ Saved: {filename}")

    print("Backup complete!")
