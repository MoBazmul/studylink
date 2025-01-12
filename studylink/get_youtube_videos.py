#!/usr/bin/python3
"""
Script to retrieve details of a YouTube video using the YouTube Data API.
"""

from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_video_details(video_url, api_key=API_KEY):
  """
  Fetches details of a YouTube video given its URL using the YouTube Data API.

  Args:
  - video_url (str): URL of the YouTube video.
  - api_key (str, optional): API key for accessing the YouTube Data API.

  Returns:
  - dict or None: Dictionary containing video details (title, thumbnail URL, video URL),
    or None if video details cannot be retrieved.
  """
  youtube = build('youtube', 'v3', developerKey=api_key)

  # Parse video ID from URL
  query = urlparse(video_url)
  if query.hostname == 'youtu.be':
    video_id = query.path[1:]
  elif query.hostname in ('www.youtube.com', 'youtube.com'):
    video_id = parse_qs(query.query)['v'][0]
  else:
    raise ValueError('Invalid YouTube URL')

  try:
    # Call the API to fetch video details
    response = youtube.videos().list(
      part='snippet',
      id=video_id
    ).execute()

    # Extract video details
    video = response['items'][0]
    video_details = {
      'title': video['snippet']['title'],
      'thumbnail': video['snippet']['thumbnails']['default']['url'],
      'video_url': f'https://www.youtube.com/watch?v={video_id}'
    }

    return video_details

  except Exception as e:
    print(f'Error fetching video details: {str(e)}')
    return None


if __name__ == '__main__':
  # Example usage
  url = "https://www.youtube.com/watch?v=nLRL_NcnK-4&t=50s&pp=ygUGcHl0aG9u"
  video = get_video_details(url)
  if video:
    print(video['title'])
    print(video['thumbnail'])
