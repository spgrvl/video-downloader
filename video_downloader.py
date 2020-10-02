import re

def platform(url):
    fb_match = re.search(r'^(?:https?:\/\/)?(?:www\.|web\.|m\.)?facebook\..*(?:\/videos.*\/|v=)(\d+).*$', url)
    ig_match = re.search(r'^(?:https?:\/\/)?(?:www\.)?(?:instagram\.com.*\/(?:p|tv|reel)\/)([\d\w\-_]+)(?:\/)?(\?.*)?$', url)
    if fb_match != None:
        return "fb", fb_match[1]
    elif ig_match != None:
        return "ig", ig_match[1]

url = input("\nEnter a Video URL: ")
platform = platform(url)
print(platform[0], platform[1])