from bs4 import BeautifulSoup as soup
import requests
import re

def platform(url):
    fb_match = re.search(r'^(?:https?:\/\/)?(?:www\.|web\.|m\.)?facebook\..*(?:\/videos.*\/|v=)(\d+).*$', url)
    ig_match = re.search(r'^(?:https?:\/\/)?(?:www\.)?(?:instagram\.com.*\/(?:p|tv|reel)\/)([\d\w\-_]+)(?:\/)?(\?.*)?$', url)
    tt_match = re.search(r'^(?:https?:\/\/)?(?:www\.|m\.)?(?:tiktok\.com.*\/(?:@(?:[\w]+))?(?:v|video|embed|trending)?(?:\/)?(?:video)?(?:\/)?(?:\?shareId=)?)([\d]+)', url)
    if fb_match != None:
        return "fb", fb_match[1]
    elif ig_match != None:
        return "ig", ig_match[1]
    elif tt_match != None:
        return "tt", tt_match[1]

def instagram(shortcode):
    page_html = requests.get("https://www.instagram.com/p/" + shortcode).content
    page_soup = soup(page_html, "html.parser")
    post_type = page_soup.findAll("meta", {"name" : "medium"})[0]['content']
    if post_type == "video":
        video_url = page_soup.findAll("meta", {"property" : "og:video"})[0]['content']
        response = requests.get(video_url)
        filename = "ig_" + shortcode
        with open(filename + ".mp4", "wb") as f:
            f.write(response.content)
        print("Download of Instagram Video {} completed.".format(shortcode))
    else:
        print("Provided Instagram URL is not a video!")

def facebook(video_id):
    page_html = requests.get("https://www.facebook.com/watch/?v=" + video_id).content
    page_soup = soup(page_html, "html.parser")
    post_type = page_soup.findAll("meta", {"name" : "medium"})[0]['content']
    if post_type == "video":
        video_url_sd = re.search(r'sd_src:"(.+?)"', str(page_html))[1]
        video_url_hd = re.search(r'hd_src:"(.+?)"', str(page_html))[1]
        if video_url_hd != None:
            response = requests.get(video_url_hd)
        elif video_url_sd != None:
            response = requests.get(video_url_hd)
        else:
            print("Unable to download Facebook video {}.".format(video_id))
        filename = "fb_" + video_id
        with open(filename + ".mp4", "wb") as f:
            f.write(response.content)
        print("Download of Facebook Video {} completed.".format(video_id))
    else:
        print("Provided Facebook URL is not a video!")

def tiktok(video_id):
    page_html = requests.get("https://www.tiktok.com/embed/" + video_id).content
    video_url = re.search(r'urls":\["(.+?)"]', str(page_html))[1]
    if video_url != None:
        headers = {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 'Accept': '*/*', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'no-cors', 'Sec-Fetch-Dest': 'video', 'Referer': 'https://www.tiktok.com/', 'Accept-Language': 'en-US,en;q=0.9', 'Range': 'bytes=0-'}
        response = requests.get(video_url, headers=headers)
        filename = "tt_" + video_id
        with open(filename + ".mp4", "wb") as f:
            f.write(response.content)
        print("Download of TikTok Video {} completed.".format(video_id))
    else:
        print("Failed to download this TikTok video!")

url = input("\nEnter a Video URL: ")
platform = platform(url)

try:
    if platform[0] == "ig":
        instagram(platform[1])
    elif platform[0] == "fb":
        facebook(platform[1])
    elif platform[0] == "tt":
        tiktok(platform[1])
except TypeError:
    print("Failed to detect platform of given URL!")
except Exception as e:
    print("Video download failed!\n" + str(e))