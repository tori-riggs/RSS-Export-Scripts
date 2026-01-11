import requests
import json
import os
import time
from newsblur_config import username, password, path

session = requests.Session()
login_payload = {"username": f"{username}", "password": f"{password}"}
session.post("https://newsblur.com/api/login", data=login_payload)
path = (f"{path}")
date = "2024-09-25"

def write(feed_id, title, start, end):
    end = end + 1;
    print(f"\nExporting: '{title}' (pages {start} - {end})")
    file_name = (os.path.join(path, f"{date} Newsblur {title}.json"))

    with open(file_name, "w") as f:
        """
        Find out how to make things similar with params and such
        """
        for page_number in range (start, end):
            url = f"https://newsblur.com/reader/feed/{feed_id}?page={page_number}"
            print("\t" + url)
            response = session.get(url)

            if (response.status_code != 200):
                print(f"Unexpected response {response.status_code}: {response.text}")
                exit(1)

            pretty_response = response.json()
            f.write(json.dumps(pretty_response, indent=2))
            f.write("\n")
            # Rest every 10 pages
            if (page_number % 10 == 0):
                time.sleep(5)

def main():
    write(7999688, "PCGamer", 1, 5)

main()