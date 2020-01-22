# Yelp Scraper

## Installation
To run this script you need three main components:
- Python 3 (python.org)
- Mozilla Firefox Browser (firefox.com)
- Firefox Selenium Driver (https://github.com/mozilla/geckodriver/releases)

If you have these installed and the firefox driver (geckodriver.exe) in PATH, run `pip install -r requirements.txt` inside the scraper folder in the console.

## Running the script
After the installation you can run the script with the following command in the console
```python yelp-scraper.py keyword```
Where you replace keyword by your business of interest.
The script will open Firefox and for each city in 'cities.txt' and scrape business links first.
Then it will scrape all individual business pages for information.
(title, website, category, phone, address, description)
And save it to a folder named 'output' in JSON format using a separate file for each city.

## Disclaimer
This script was written for educational purposes only and it is not meant to be used in any harmful way.
If you want to retrieve data from Yelp use their API.