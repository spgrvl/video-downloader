from bs4 import BeautifulSoup as soup
from datetime import datetime
import requests
import re

def platform(url):
    fb_match = re.search(r'^(?:https?:\/\/)?(?:www\.|web\.|m\.)?facebook\..*(?:\/videos.*\/|v=)(\d+).*$', url)
    ig_match = re.search(r'^(?:https?:\/\/)?(?:www\.)?(?:instagram\.com.*\/(?:p|tv|reel)\/)([\d\w\-_]+)(?:\/)?(\?.*)?$', url)
    if fb_match != None:
        return "fb", fb_match[1]
    elif ig_match != None:
        return "ig", ig_match[1]

def instagram(shortcode):
    page_html = requests.get("https://www.instagram.com/p/" + shortcode).content
    page_soup = soup(page_html, "html.parser")
    post_type = page_soup.findAll("meta", {"name" : "medium"})[0]['content']
    if post_type == "video":
        video_url = page_soup.findAll("meta", {"property" : "og:video"})[0]['content']
        response = requests.get(video_url)
        filename = datetime.strftime(datetime.now(), '%Y%m%d%H%M') + "_ig_" + shortcode
        with open(filename + ".mp4", "wb") as f:
            f.write(response.content)
        print("Download of Instagram Video {} completed.".format(shortcode))
    else:
        print("Provided Instagram URL is not a video!")

url = input("\nEnter a Video URL: ")
platform = platform(url)

try:
    if platform[0] == "ig":
        instagram(platform[1])
    elif platform[0] == "fb":
        facebook(platform[1])
except TypeError:
    print("Failed to detect platform of given URL!")
except Exception as e:
    print("Video download failed!\n" + str(e))