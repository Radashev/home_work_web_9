import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "http://quotes.toscrape.com"
AUTHOR_URL = "http://quotes.toscrape.com{}"
quotes = []
authors = []

def scrape_quotes(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    quote_elements = soup.select('.quote')

    for quote_element in quote_elements:
        quote_text = quote_element.select_one('.text').get_text()
        author_name = quote_element.select_one('.author').get_text()
        author_url = quote_element.select_one('span a')['href']
        tags = [tag.get_text() for tag in quote_element.select('.tag')]

        quotes.append({
            "quote": quote_text,
            "author": author_name,
            "tags": tags
        })

        if not any(author['fullname'] == author_name for author in authors):
            scrape_author(author_url)

    next_button = soup.select_one('.next a')
    if next_button:
        next_page = BASE_URL + next_button['href']
        scrape_quotes(next_page)

def scrape_author(author_url):
    response = requests.get(AUTHOR_URL.format(author_url))
    if response.status_code != 200:
        print(f"Failed to retrieve author page {author_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    author_name = soup.select_one('.author-title').get_text().strip()
    born_date = soup.select_one('.author-born-date').get_text().strip()
    born_location = soup.select_one('.author-born-location').get_text().strip()
    description = soup.select_one('.author-description').get_text().strip()

    authors.append({
        "fullname": author_name,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    })


if __name__ == "__main__":
    start_time = time.time()
    scrape_quotes(BASE_URL)
    print(f"Scraping finished in {time.time() - start_time:.2f} seconds")

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print("Data saved to quotes.json and authors.json")
