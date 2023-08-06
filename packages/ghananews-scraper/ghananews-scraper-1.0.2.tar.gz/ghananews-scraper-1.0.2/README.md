### GhanaWeb Scraper
  A simple unofficial python package to scrape data from [Ghanaweb](https://www.ghanaweb.com). Affiliated to [bank-of-ghana-fx-rates](https://pypi.org/project/bank-of-ghana-fx-rates/)

### How to install
```shell
pip install ghanaweb-scraper
```
### Warning: DO NOT RUN IN ONLINE JUPYTERNOTEBOOKS eg. Colabs

### GhanaWeb Urls:
```markdown
urls = [
    "https://www.ghanaweb.com/GhanaHomePage/regional/"	
    "https://www.ghanaweb.com/GhanaHomePage/editorial/"
    "https://www.ghanaweb.com/GhanaHomePage/health/"
    "https://www.ghanaweb.com/GhanaHomePage/diaspora/"
    "https://www.ghanaweb.com/GhanaHomePage/tabloid/"
    "https://www.ghanaweb.com/GhanaHomePage/africa/"
    "https://www.ghanaweb.com/GhanaHomePage/religion/"
    "https://www.ghanaweb.com/GhanaHomePage/NewsArchive/"
    "https://www.ghanaweb.com/GhanaHomePage/business/"
    "https://www.ghanaweb.com/GhanaHomePage/SportsArchive/"
    "https://www.ghanaweb.com/GhanaHomePage/entertainment/"
    "https://www.ghanaweb.com/GhanaHomePage/africa/"
    "https://www.ghanaweb.com/GhanaHomePage/television/"
]
```
### Usage
```python
from ghanaweb.scraper import GhanaWeb

url = 'https://www.ghanaweb.com/GhanaHomePage/politics/'
# url = 'https://www.ghanaweb.com/GhanaHomePage/health/'
# url = 'https://www.ghanaweb.com/GhanaHomePage/crime/'
# url = 'https://www.ghanaweb.com/GhanaHomePage/regional/'
# url = 'https://www.ghanaweb.com/GhanaHomePage/year-in-review/'

# web = GhanaWeb(url='https://www.ghanaweb.com/GhanaHomePage/politics/')
web = GhanaWeb(url=url)
# scrape data and save to `current working dir`
web.download(output_dir=None)
```
### scrape list of articles from [GhanaWeb](https://ghanaweb.com)
```python
from ghanaweb.scraper import GhanaWeb

urls = [
        'https://www.ghanaweb.com/GhanaHomePage/politics/',
        'https://www.ghanaweb.com/GhanaHomePage/health/',
        'https://www.ghanaweb.com/GhanaHomePage/crime/',
        'https://www.ghanaweb.com/GhanaHomePage/regional/',
        'https://www.ghanaweb.com/GhanaHomePage/year-in-review/'
    ]

for url in urls:
    print(f"Downloading: {url}")
    web = GhanaWeb(url=url)
    # download to current working directory
    # if no location is specified
    # web.download(output_dir="/Users/tsiameh/Desktop/")
    web.download(output_dir=None)
```

### Scrape data from [MyJoyOnline](https://myjoyonline.com)
```python
from myjoyonline.scraper import MyJoyOnline

url = 'https://www.myjoyonline.com/news/',

print(f"Downloading data from: {url}")
joy = MyJoyOnline(url=url)
# download to current working directory
# if no location is specified
# joy.download(output_dir="/Users/tsiameh/Desktop/")
joy.download()
```
```python
from myjoyonline.scraper import MyJoyOnline

urls = [
        'https://www.myjoyonline.com/news/',
        'https://www.myjoyonline.com/entertainment/',
        'https://www.myjoyonline.com/business/',
        'https://www.myjoyonline.com/sports/',
        'https://www.myjoyonline.com/opinion/'
    ]

for url in urls:
    print(f"Downloading data from: {url}")
    joy = MyJoyOnline(url=url)
    # download to current working directory
    # if no location is specified
    # joy.download(output_dir="/Users/tsiameh/Desktop/")
    joy.download()
```

BuyMeCoffee
-----------
[![Build](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/theodondrew)

Credits
-------
-  `Theophilus Siameh`
<div>
    <a href="https://twitter.com/tsiameh"><img src="https://img.shields.io/twitter/follow/tsiameh?color=blue&logo=twitter&style=flat" alt="tsiameh twitter"></a>
</div>