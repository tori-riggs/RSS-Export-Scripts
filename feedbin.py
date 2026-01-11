import requests
import sys
import argparse
import json
import os
import time
from datetime import datetime
from feedbin_secret import username, password
from feedbin_config import path, feeds

session = requests.Session()
session.auth = (f"{username}", f"{password}")
current_datetime = datetime.now()
date = current_datetime.strftime("%Y%m%d%H%M")
path = (f"{path}")

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


def write(feed_id, title, start, end):
    end = end + 1 # inclusive end
    all_data = []
    print(f"\nExporting: '{title}' (pages {start} - {end})")
    file_name = (os.path.join(path, f"{date} Feedbin {title}.json"))
    # file_name = (os.path.join(path, f"{date} Feedbin {title} starred.json"))

    with open(file_name, "w") as f:
        for page_number in range(start, end + 1):
            url = f"https://api.feedbin.com/v2/feeds/{feed_id}/entries.json?page={page_number}"
            # starred:
            # url = f"https://api.feedbin.com/v2/feeds/{feed_id}/entries.json?starred=true&page={page_number}"
            # saved search:
            # url = f"https://api.feedbin.com/v2/saved_searches/{feed_id}.json?include_entries=true&page={page_number}"
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
            all_data.append(data)
            
            # f.write("\n")
            if (page_number % 5 == 0):
                time.sleep(5)

        f.write(json.dumps(all_data, indent=4, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(prog="feedbin.py")
    parser.add_argument("-o", "--output", help="Output path directory", action='store', default=path)
    parser.add_argument("-c", "--config", help="Path to config file", default="feedbin_config.py")
    parser.add_argument("-f", "--feeds", help="Path to list of feeds", default=feeds)
    args = parser.parse_args()
    print(args.output)
    print(args.config)
    print(args.feed)
    read_file(args.config)
    read_file(args.feeds)

main()