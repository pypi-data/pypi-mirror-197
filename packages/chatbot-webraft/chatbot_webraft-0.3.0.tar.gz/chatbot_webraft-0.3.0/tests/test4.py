from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Define custom user agent and search filter
headers = '"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"'
search_filter = " -site:youtube.com -site:google.com -site:googleusercontent.com -site:twitter.com -site:facebook.com -site:instagram.com -site:pinterest.com -site:wikipedia.org -site:wikimedia.org -site:webmd.com -site:linkedin.com -site:slideshare.net -site:amazon.com"

# Take input from user
query = input("Enter your query: ")

# Search for the query on Google and get the first website
search_results = search(query + search_filter)
first_website = next(iter(search_results), None)
print(search_results)
print("\n",first_website)
# If no results found on Google, print error message and exit
if not first_website:
    print("Could not find any results on Google for that query.")
    exit()

# Request the first website's content and parse it using BeautifulSoup
response = requests.get(first_website)
soup = BeautifulSoup(response.content, "html.parser")

# Extract the first four lines of text from the website's content (only <p> tags)
text_lines = []
for p in soup.find_all('\n'):
    stripped_line = p.get_text().strip()
    if stripped_line:
        text_lines.append(stripped_line)
        if len(text_lines) == 4:
            break

# If no text found in <p> tags, print error message and exit
if not text_lines:
    print("Could not find any text in <p> tags on the first website.")
    exit()

# Print the first four lines of text
print('\n'.join(text_lines))
