import csv
import os
import urllib
import requests
from bs4 import BeautifulSoup
from .utils import SaveFile

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


class MyJoyOnline:
    def __init__(self, url):
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.file_name = urllib.parse.unquote(url.split("/")[-2] if url.endswith("/") else url.split("/")[-1])

    def download(self, output_dir=None):
        """scrape data"""
        with requests.Session() as session:
            response = session.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        lst_pages = [page for page in soup.find_all(['li', 'div'],
                                                     {'class': ['mostrecent_btf', 'faded-bar', 'home-section-story-list tt-center']})
                     + soup.find('ul', {'class': 'home-latest-list'}).find_all('li')]

        try:
            print("saving results to csv...")
            if output_dir is None:
                output_dir = os.getcwd()
                SaveFile.mkdir(output_dir)
            if not os.path.isdir(output_dir):
                raise ValueError(f"Invalid output directory: {output_dir} is not a directory")
            print(f"File will be saved to: {output_dir}")
            with open(os.path.join(output_dir, self.file_name + ".csv"), mode='w', newline='') as csv_file:
                fieldnames = ['title', 'content', 'page_url']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for page in lst_pages:
                    page_url = page.find("a").attrs.get('href')
                    if page_url:
                        with requests.Session() as session:
                            response_page = session.get(page_url, headers=headers)
                        soup_page = BeautifulSoup(response_page.text, 'html.parser')
                        title = soup_page.find('div', {'class': 'article-title'})
                        title = title.text.strip() if title else ""
                        content = soup_page.find('div', {'id': 'article-text'})
                        content = content.text.strip() if content else ""
                        writer.writerow({'title': title, 'content': content, 'page_url': page_url})
                print("Writing data to file...")
        except Exception as e:
            print(f"error: {e}")

        print(f"All file(s) saved to: {output_dir} successfully!")
        print("Done!")



# class MyJoyOnline:
#     def __init__(self, url):
#         self.url = url
#         self.file_name = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
#
#     def download(self, output_dir=None):
#         """scrape data"""
#         response = requests.request('GET', self.url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         lst_pages = soup.find_all('li', {'class': 'mostrecent_btf'}) \
#                     + soup.find_all('li', {'class': 'faded-bar'}) \
#                     + soup.find_all('div', {'class': 'home-section-story-list tt-center'}) \
#                     + soup.find('ul', {'class': 'home-latest-list'}).find_all('li')
#
#         try:
#             print("saving results to csv...")
#             if output_dir is None:
#                 output_dir = os.getcwd()
#                 SaveFile.mkdir(output_dir)
#             print(f"File will be saved to: {output_dir}")
#             with open(f"{output_dir}/{self.file_name}" + ".csv", mode='w', newline='') as csv_file:
#                 fieldnames = ['title', 'content', 'page_url']
#                 writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#                 print("Writing column names...")
#                 writer.writeheader()
#                 for page in lst_pages:
#                     try:
#                         page_url = page.find("a").attrs['href']
#                         response_page = requests.request('GET', page_url, headers=headers)
#                         soup_page = BeautifulSoup(response_page.text, 'html.parser')
#                         try:
#                             title = soup_page.find('div', {'class': 'article-title'}).text.strip()
#                         except Exception:
#                             title = ""
#                         try:
#                             content = soup_page.find('div', {'id': 'article-text'}).text.strip()
#                         except Exception:
#                             content = ""
#
#                         writer.writerow({'title': title, 'content': content, 'page_url': page_url})
#                     except Exception:
#                         continue
#                 print("Writing artitle titles...")
#                 print("Writing article content...")
#                 print("Writing data to file...")
#         except Exception as e:
#             print(f"error: {e}")
#
#         print(f"All file(s) saved to: {output_dir} successfully!")
#         print("Done!")
