import csv

import requests
from bs4 import BeautifulSoup

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


class GhanaWeb:
    def __init__(self, url, home_page="https://www.ghanaweb.com"):
        self.url = url
        self.home_page = home_page
        self.file_name = url.split("/")[-2]

    def download(self):
        response = requests.request('GET', self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        lst_pages = soup.find('div', {'class': 'afcon-news list'}).find_all('a')

        try:
            with open(self.file_name + ".csv", mode='w', newline='') as csv_file:
                fieldnames = ['title', 'content', 'page_url']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                print("Writing column names...")
                writer.writeheader()
                for page in lst_pages:
                    try:
                        page_url = self.home_page + page.attrs['href']
                        response_page = requests.request('GET', page_url, headers=headers)
                        soup_page = BeautifulSoup(response_page.text, 'html.parser')
                        try:
                            title = soup_page.find('h1', {'style': 'clear: both;'}).text.strip()
                        except Exception:
                            title = ""
                        try:
                            content = soup_page.find('p', {'style': 'clear:right'}).text.strip()
                        except Exception:
                            content = ""
                        print("Writing artitle titles...")
                        print("Writing article content...")
                        print("Writing data to file...")
                        writer.writerow({'title': title, 'content': content, 'page_url': page_url})
                    except Exception:
                        continue
        except Exception as e:
            print(f"error: {e}")

        print(f"{self.file_name}: Data Saved Successfully!")
        print("Done!")
