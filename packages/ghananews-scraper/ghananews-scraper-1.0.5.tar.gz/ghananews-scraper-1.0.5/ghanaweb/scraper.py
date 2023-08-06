import csv
import os
import urllib
import requests
from bs4 import BeautifulSoup
from .utils import SaveFile, HEADERS


class GhanaWeb:
    def __init__(self, url, home_page="https://www.ghanaweb.com"):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.home_page = home_page
        self.file_name = urllib.parse.unquote(
            url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
        )
        self.response = None
        self.soup = None

    def download(self, output_dir=None):
        """scrape data"""
        self.response = self.response or requests.request(
            "GET", self.url, headers=HEADERS
        )
        self.soup = self.soup or BeautifulSoup(self.response.text, "html.parser")
        lst_pages = [
            a for a in self.soup.find("div", {"class": "afcon-news list"}).find_all("a")
        ]

        try:
            print("saving results to csv...")
            output_dir = output_dir or os.getcwd()
            SaveFile.mkdir(output_dir)
            if not os.path.isdir(output_dir):
                raise ValueError(
                    f"Invalid output directory: {output_dir} is not a directory"
                )
            print(f"File will be saved to: {output_dir}")
            with open(
                os.path.join(output_dir, self.file_name + ".csv"), mode="w", newline=""
            ) as csv_file:
                fieldnames = ["title", "content", "page_url"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for page in lst_pages:
                    try:
                        page_url = self.home_page + page.get("href", "")
                        if page_url:
                            response_page = requests.request("GET", page_url, headers=HEADERS)
                            soup_page = BeautifulSoup(response_page.text, "html.parser")
                            try:
                                title = soup_page.find("h1", {"style": "clear: both;"}).text.strip()
                            except Exception:
                                title = ""
                            try:
                                content = soup_page.find("p", {"style": "clear:right"}).text.strip()
                            except Exception:
                                content = ""
                            writer.writerow(
                                    {"title": title, "content": content, "page_url": page_url}
                            )
                    except Exception:
                        continue
                print("Writing data to file...")
        except Exception as e:
            print(f"error: {e}")

        print(f"All file(s) saved to: {output_dir} successfully!")
        print("Done!")


# class GhanaWeb:
#     def __init__(self, url, home_page="https://www.ghanaweb.com"):
#         self.url = url
#         self.home_page = home_page
#         self.file_name = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
#
#     def download(self, output_dir=None):
#         """scrape data"""
#         response = requests.request('GET', self.url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         lst_pages = soup.find('div', {'class': 'afcon-news list'}).find_all('a')
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
#                         page_url = self.home_page + page.attrs['href']
#                         response_page = requests.request('GET', page_url, headers=headers)
#                         soup_page = BeautifulSoup(response_page.text, 'html.parser')
#                         try:
#                             title = soup_page.find('h1', {'style': 'clear: both;'}).text.strip()
#                         except Exception:
#                             title = ""
#                         try:
#                             content = soup_page.find('p', {'style': 'clear:right'}).text.strip()
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
