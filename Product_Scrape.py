import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape the additional details from a single product URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        description = soup.find('div', {'id': 'feature-bullets'}).text.strip()
    except:
        description = ''
    
    try:
        asin = soup.find('th', text='ASIN').find_next_sibling('td').text.strip()
    except:
        asin = ''
    
    try:
        product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
    except:
        product_description = ''
    
    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    except:
        manufacturer = ''
    
    return description, asin, product_description, manufacturer

# Function to scrape the product details from a single page
def scrape_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    data = []
    for product in products:
        try:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal a-text-normal'})['href']
            product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
            product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
            
            rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            
            reviews = product.find('span', {'class': 'a-size-base'}).text.strip()
            reviews = reviews.replace(',', '')
            reviews = reviews.split()[0]
            
            description, asin, product_description, manufacturer = scrape_product_details(product_url)
            
            data.append([product_url, product_name, product_price, rating, reviews, description, asin, product_description, manufacturer])
        except:
            continue
    
    return data

# Main function to scrape multiple pages
def scrape_pages(start_page, num_pages):
    all_data = []
    for page in range(start_page, start_page + num_pages):
        page_url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
        data = scrape_page(page_url)
        all_data.extend(data)
    
    return all_data

# Scrape 200 product URLs
results = scrape_pages(1, 20)

# Save the results to a CSV file
filename = 'amazon_products.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])
    writer.writerows(results)

print(f"Scraped data from {len(results)} products. Saved to {filename}.")
