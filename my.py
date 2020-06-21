import sys
import os
import requests
from re import sub, finditer
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import ntpath 

def get_board_threads(url):

    thread_ids = []
    # Get URLs of all active threads of a board
    # I understand that this code is very hacked together
    # the while loop reads from an identifiable section of
    # the HTML backwards to the end of each thread ID.
    # BeautifulSoup cannot work with this because the respose
    # is actually a JSON object (I belive)
    html = requests.get(url).text
    #print("mah html" + str(html.encode()))

    # '":{"date"' is the only unique pattern found near each thread ID
    indicies = [x.start() for x in finditer('":{"date"', html)]
    for indice in indicies:
        thread_id = ""
        counter = 1
        while html[indice-counter] != '"':
            thread_id = html[indice-counter] + thread_id
            counter += 1
        thread_ids.append(thread_id)
    print(thread_ids)
    for thread in thread_ids:
        print("thread: " + str(thread))

    # Omit the first post, because it's always a
    # mod's sticky for the board
    return thread_ids[1:]

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def download_file(url, dest_dir, filename=None):
    print("download_file():")
    print("url: " + str(url))
    print("dest_dir: " + str(dest_dir))
    print("filename: " + str(filename))

    # If no specific filename is provided, use the filename as
    # exists on the URL path
    if(filename is None):
        #filename = urlsplit(url).path.split("/")[-1]
        print("mah url: " + str(url))
        filename = path_leaf(url)

    _, ext = os.path.splitext(filename)
    if ext == ".webm":
        return
        

    request = requests.get(url)
    image = Image.open(BytesIO(request.content))
    image.save(os.path.join(dest_dir, filename))

def main():
    print("Tharp 4chan image scraper")

    if len(sys.argv) != 4:
        print("Usage: my.py board <board_letter> <dest_dir>")
        return 0

    if(sys.argv[1] == "board"):
        board = sys.argv[2]
        print("Checking board catalog @: " + "http://boards.4chan.org/" + board)
        board_url = "http://boards.4chan.org/" + board
        dest_dir = sys.argv[3]
        
        url = "http://boards.4chan.org/" + board
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        #print(soup.prettify().encode())

        for link in soup.find_all('a'):
            #print(link.get('href'))
            href = link.get('href')
            if '//i.4cdn.org/' in href:
                print("img: " + href)
                url = "https:" + href
                download_file(url, dest_dir)
        
        url = "https://boards.4chan.org/" + board + "/catalog"
        print("new board url: " + url)
        threads = get_board_threads(url) 
        
        for thread in threads:
            url = "https://boards.4chan.org/s/thread/" + thread
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")

            for img in soup.find_all('img'):
                print("img: " + str(img.encode()))
                src = img.get('src')
                url = "http:" + src
                url = url.replace("s.jpg", ".jpg")
                url = url.replace("s.png", ".png")               
                try: 
                    download_file(url, dest_dir)
                except: 
                    print("Error: while downloading " + url + " skipping.")

if __name__ == '__main__':
    main()
