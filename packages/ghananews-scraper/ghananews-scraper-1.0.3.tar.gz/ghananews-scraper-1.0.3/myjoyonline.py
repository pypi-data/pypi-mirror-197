from myjoyonline.scraper import MyJoyOnline

# pages = 10
# for page in range(1, pages):
#
#     url = f'https://www.myjoyonline.com/opinion/page/{page}/'
#
#     print(f"Downloading data from: {url}")
#     web = MyJoyOnline(url=url)
#     web.download()

if __name__ == '__main__':
    url = 'https://www.myjoyonline.com/news/',

    print(f"Downloading data from: {url}")
    joy = MyJoyOnline(url=url)
    # download to current working directory
    # if no location is specified
    # joy.download(output_dir="/Users/tsiameh/Desktop/")
    joy.download()
