from myjoyonline.scraper import MyJoyOnline

urls = [
        'https://www.myjoyonline.com/news/',
        'https://www.myjoyonline.com/entertainment/',
        'https://www.myjoyonline.com/business/',
        'https://www.myjoyonline.com/sports/',
        'https://www.myjoyonline.com/opinion/'
    ]

if __name__ == '__main__':

    for url in urls:
        print(f"Downloading data from: {url}")
        joy = MyJoyOnline(url=url)
        # download to current working directory
        # if no location is specified
        # joy.download(output_dir="/Users/tsiameh/Desktop/")
        joy.download()