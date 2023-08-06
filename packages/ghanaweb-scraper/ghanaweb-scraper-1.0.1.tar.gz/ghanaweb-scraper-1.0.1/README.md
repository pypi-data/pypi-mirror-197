### GhanaWeb Scraper
  A simple unofficial python package to scrape data from Ghanaweb. Affiliated to [bank-of-ghana-fx-rates](https://pypi.org/project/bank-of-ghana-fx-rates/)

### How to install
```shell
pip install ghanaweb-scraper
```
### Warning: DO NOT RUN IN ONLINE JUPYTERNOTEBOOKS eg. Colabs

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
### scrape list of articles
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

BuyMeCoffee
-----------
[![Build](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/theodondrew)

Credits
-------
-  `Theophilus Siameh`
<div>
    <a href="https://twitter.com/tsiameh"><img src="https://img.shields.io/twitter/follow/tsiameh?color=blue&logo=twitter&style=flat" alt="tsiameh twitter"></a>
</div>