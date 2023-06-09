

import csv
import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar'

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the product listings on the page
products = soup.select('div[data-component-type="s-search-result"]')

# Create a CSV file to store the data
csv_file = open('amazon_products.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

# Write the header row
writer.writerow(['Product Name', 'Price', 'Rating', 'Seller Name'])

# Iterate over each product and extract the details
for product in products:
    # Extract the product name
    name = product.select_one('span.a-size-base-plus.a-color-base.a-text-normal').text.strip()

    # Extract the price
    price = product.select_one('span.a-price-whole').text.strip()

    # Extract the rating if available, otherwise set it as 'Not Rated'
    rating_element = product.select_one('span.a-icon-alt')
    rating = rating_element.text.strip() if rating_element else 'Not Rated'

    # Check if the product is out of stock
    out_of_stock = product.select('span.a-size-small.a-color-price')

    # Extract the seller name if the product is not out of stock, otherwise set it as 'Out of Stock'
    seller = 'Out of Stock' if out_of_stock else product.select_one('span.a-size-base.a-color-secondary').text.strip()

    # Write the data to the CSV file
    writer.writerow([name, price, rating, seller])

# Close the CSV file
csv_file.close()
