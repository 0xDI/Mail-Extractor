import requests
import json
import random
import re
import csv
import os

API_KEY = ''  # Replace with your API key
SEARCH_ENGINE_ID = ''  # Replace with your search engine ID
niches = ["real estate", "healthcare", "fitness", "education", "food industry", "tech startups"]
email_types = ["@gmail.com", "@outlook.com", "icloud.com"]

def perform_search(niche, email_type):
    search_query = f'{niche} -intitle:"profiles" {email_type} -inurl:"dir/+" site:linkedin.com'
    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}'
    response = requests.get(url)
    return response.json()

def extract_emails(search_results):
    emails = set()
    if 'items' in search_results:
        for item in search_results['items']:
            snippet = item.get('snippet', '')
            found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', snippet)
            emails.update(found_emails)
    return list(emails)

all_emails = []

for niche in niches:
    for email_type in email_types:
        search_results = perform_search(niche, email_type)
        emails = extract_emails(search_results)
        all_emails.extend(emails)

csv_filename = "extracted_mails.csv"
file_exists = os.path.isfile(csv_filename)

with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Email"])
    for email in set(all_emails):
        writer.writerow([email])

print(f"Extracted emails have been saved to {csv_filename}.")
