import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def scrape_wikipedia_article(url, max_links=100):
    requests_result = requests.get(url)
    page_content = requests_result.text
    
    page_soup = BeautifulSoup(page_content, 'html.parser')
    
    article_title_element = page_soup.find("h1", class_="firstHeading")
    if article_title_element:
        article_title = article_title_element.text
    else:
        article_title = "Unknown"
        print("Warning: Could not find article title for URL:", url)
    
    content_div = page_soup.find("div", class_="mw-content-ltr mw-parser-output")
    if content_div:
        links = content_div.find_all("a")
    else:
        links = []
    
    links_data = []
    link_counter = 0
    for link in links:
        if link_counter >= max_links:
            break
        if 'href' in link.attrs and "/wiki/" in link['href']:
            link_text = link.get_text().strip()
            if link_text:
                links_data.append((link_text, link['href']))
                link_counter += 1
    
    return article_title, links_data

csv_file = "links_data_recursive_limited_3D100L.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Source Article", "Article Title", "Link"])
    
    initial_link = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    visited_links = set()
    
    def scrape_and_save(source_article, url, depth=0):
        if depth >= 3:
            return
        if url in visited_links:
            return
        visited_links.add(url)
        
        title, links_data = scrape_wikipedia_article(url)
        writer.writerows([(source_article, link[0], link[1]) for link in links_data])
        
        for link_title, link_url in links_data:
            next_url = urljoin("https://en.wikipedia.org/", link_url)
            scrape_and_save(source_article, next_url, depth + 1)
    
    source_article, initial_links_data = scrape_wikipedia_article(initial_link)
    writer.writerows([(source_article, link[0], link[1]) for link in initial_links_data])
    for link_title, link_url in initial_links_data:
        next_url = urljoin("https://en.wikipedia.org/", link_url)
        scrape_and_save(link_title, next_url, 1)