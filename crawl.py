import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse


# r = "https://en.wikipedia.org/wiki/Router_(computing)"
#r = "https://en.wikipedia.org/wiki/Terminalia_ferdinandiana"
domain = "https://www.geeksforgeeks.com"
r  ="https://www.geeksforgeeks.org/reading-writing-text-files-python/"
queue_links = deque()
links_processed = set()
max_level = 2
counter2 = 1
file1 = open("links_connection.txt","w")

queue_links.append((r,1))

def crawl():
    counter = 0
    counter2 = 0
    while len(queue_links) > 0:
        link_from_queue = queue_links.popleft()
        # print(link_request1)
        link_request = link_from_queue[0]
        current_level = link_from_queue[1]
        links_processed.add(link_request)
        print("links requested: ",len(links_processed))
        print("links added to queue: ",len(queue_links))
        print(queue_links)
        links_added_level = 0
        if link_check (link_request):
            link_response = requests.get(link_request)
            src = link_response.content
            soup = BeautifulSoup(src, "html.parser")
            links = soup.find_all('a')
            for i in links:
                link = i.get('href')
                # print("link:",link)
                # print (type(link))
                # print (link)
                link = str(link)
                if link == 'None' or link.startswith('#') or link.startswith("javascript"):
                    continue
                else:
                    updated_link = whole_link(link)
                    new_link = no_fragment(updated_link)
                    # print(f"whole link: {updated_link} \n no fragment link: {new_link}")
                    counter += 1
                    print("iterated through:",counter)
                    file1.write (f"({link_request},{new_link}),\n")
                    if current_level <= max_level and links_added_level<10:
                        # if new_link not in queue_links:
                        queue_links.append((new_link, current_level + 1))
                        counter2 = counter2 + 1
                        links_added_level +=1
                        print("added link:",counter2,"\n")
                        print("links added at the level:", links_added_level)
    file1.close()
    return links_processed

def whole_link(a):
    return_link = ""
    if a.startswith ("/"):
        return_link = domain + a
    elif a.startswith("//"):
        return_link = "https:" + a
    else:
        return_link = a
    return return_link

def no_fragment(link):
    return_link = urlparse(link)
    return_link = return_link._replace(fragment='')
    return_link = return_link.geturl()
    return return_link


def link_check(link):
    """cheking if link is not broken and is not image and is not in processed links"""
    try:
        r = requests.get(link)
        if r.status_code >=200 and r.status_code <=300 and (r.headers["Content-Type"]) is not "image/jpeg" and r not in links_processed:
            return True
        else:
            return False
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectionError,requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
        return False

crawl()
print(queue_links)
print(links_processed)