import requests
from bs4 import BeautifulSoup

base_url = 'https://m.signalvnoise.com'

def get_page():
  base_url = 'https://m.signalvnoise.com'
  response = requests.get(base_url)
  print('The status code is:', response.status_code)
  with open('blopost.html', 'w') as f:
    f.write(response.text)
  page_content = response.text
  print(len(page_content))
  doc = BeautifulSoup(page_content, 'html.parser')
  return doc

# Get the following information from the webpage: title, author, published date, comments, blog url,author url, author's image url

doc = get_page()

header_tags = doc.find_all('header', class_='entry-header grid__item grid__item--large')

header_tag = header_tags[0]

def parse_webpage(header_tag):
  # Get title
  h2_tag = header_tag.find('h2', class_='entry-title entry-title--list centered')
  title = h2_tag.text
  # Get blog url
  blog_url = h2_tag.find('a')['href']
  # Get author
  author_span_tag = header_tag.find('span', class_='byline')
  a_tag = author_span_tag.find('a')
  author = a_tag.text
  # Get author url
  author_url = a_tag['href']
  # Get published date
  published_date = header_tag.find('time', class_='entry-date published updated').text
  # Get author image
  img_div = header_tag.find('div', class_='entry-meta__avatars')
  img_url = img_div.find('img')['src']
  return {
    'author name': author,
    'title': title,
    'published_date': published_date,
    'blog url': blog_url,
    'author url': author_url,
    'author image url': img_url
  }

top_webpages = [parse_webpage(tag) for tag in header_tags]

def top_webpage():
  header_tags = doc.find_all('header', class_='entry-header grid__item grid__item--large')
  top_webpages = [parse_webpage(tag) for tag in header_tags]
  return top_webpages

# Put in a csv
def write_csv(items, path):
    # Open the file in write mode
    with open(path, 'w') as f:
        # Return if there's nothing to write
        if len(items) == 0:
            return
        
        # Write the headers in the first line
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        
        # Write one item per line
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            f.write(','.join(values) + "\n")

write_csv(top_webpages, 'blog.csv')