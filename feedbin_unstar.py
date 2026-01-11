import requests
import json
import os
import time
from datetime import datetime
from feedbin_secret import username, password, path

session = requests.Session()
session.auth = (f"{username}", f"{password}")
current_datetime = datetime.now()
date = current_datetime.strftime("%Y%m%d%H%M")
path = (f"{path}")
# ChatGPT recommended a headers variable
headers = {
    "Content-Type": "application/json; charset=utf-8"
}

def read_file(filename):
    with open(filename) as file:
        for line in file:
            if (not line.startswith("#") and line.strip()):
                fields = line.strip().split(',')
                feed_id = int(fields[0])
                title = fields[1].lstrip().strip("\"")
                start = int(fields[2])
                end = int(fields[3])
                write(feed_id, title, start, end)


def write( feed_id, title, start, end ):
    end = end + 1 # inclusive end
    print(f"Unstarring from: '{title}' (pages {start} - {end})")
    file_name = (os.path.join(path, f"{date} Feedbin {title} starred removed.json"))
    deleted = {}
    with open(file_name, "w") as f:
        for page_number in range(start, end):
            to_delete = []
            # url = f"https://api.feedbin.com/v2/saved_searches/{feed_id}.json?include_entries=true&page={start}"
            url = f"https://api.feedbin.com/v2/feeds/{feed_id}/entries.json?starred=true&page={start}"
            print("\t" + url)
            response = session.get(url)
            
            if (response.status_code != 200):
                if (response.status_code == 404):
                    break
                else:
                    print(f"Unexpected response {response.status_code}: {response.text}")
                    exit(1)
                
            # can get certain json fields though response.json.
            # Can use that to mass unstar articles.
            data = response.json()
            for item in data:
                id = item['id']
                to_delete.append(id);
            
            # Disclosure: ChatGPT was used for debugging purposes.
            # ChatGPT recommended a payload variable with json.dumps()
            payload = json.dumps({"starred_entries": to_delete})
            x = requests.delete("https://api.feedbin.com/v2/starred_entries.json", data=payload, headers=headers, auth=(f"{username}", f"{password}"))
            print("\t Page: ", page_number)
            data = x.json()
            deleted[f"starred entries {page_number}"] = data
            if (page_number % 5 == 0):
                time.sleep(5)
        json_str = json.dumps(deleted, indent=4)
        f.write(json_str)


def main():
    read_file("feedbin_feeds.txt")


main()