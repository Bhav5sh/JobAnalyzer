import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_courses(skill, max_results=2):
    query = f"Learn {skill} tutorial"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={query}&key={YOUTUBE_API_KEY}&type=video"

    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        results.append({"title": title, "link": video_url})

    return results

def recommend_courses_dynamic(missing_skills):
    recommendations = {}
    for skill in missing_skills:
        videos = search_youtube_courses(skill)
        if videos:
            recommendations[skill] = videos
    return recommendations
