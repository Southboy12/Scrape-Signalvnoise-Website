#!/usr/bin/env python
# coding: utf-8

# # Web Scraping Project - Dataset of blog posts on popular blog Signalvnoise
# 
# Data Source : [Signalvnoise.com](https://m.signalvnoise.com)
# <div>
# <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbvM6BCIt13nyV4IlUYLBvY63XojMinnOCyQ&usqp=CAU" width=1000/>
# </div>

# ## Web Scraping
# 
# Web scraping is a technique used to collect data and content from the internet. An example of web scraping is 
# coping and pasting a content from a website into Excel spreadsheet, but on a very small scale.
# 
# Web scraping applications also referred to as web scrapers are programmed to visit websites, grab the relevant 
# pages and extract useful information. By automating this process, the bots can extract huge amount of data in a 
# very short time.
# 
# > ### Basic Web Scraping Principles:
# 
# - Making an HTTP request to a server
# - Extracting and parsing the website's code
# - Saving the relevant data locally
# 
# > ### Beautiful Soup
# 
# Beautiful Soup is a Python library for pulling data out of HTML and XML files. It makes it easy to scrape information from web pages. It provides Pythonic idioms for iterating, searching and modifying the parse tree.
# 
# Beautiful Soup library helps with isolating titles and links from web pages. It can extract all the text from HTML tags and alter the HTML document with which we're working.

# ### About Signalvnoise
# <div>
# <img src="https://archive.signalvnoise.com/assets/archive-v3.png" width=500>
# </div>
# 
# Signal v. Noise (to quote the blog directly) "Strong opinions and shared thoughts on design, business, and tech. By the makers (and friends) of Basecamp".
# One interesting thing about the blog is that most of the posts can be read in 5 minutes - they are concise, straight to the point.

# ### Project Idea
# 
# In this project, we will parse the signalvnoise website to get information like title, author, published date, blog url, author url and author image url from **https://m.signalvnoise.com** and collate the data into a single CSV document.

# ### Project Steps
# Here is an outline of the steps we'll follow :
# 
# 1. Download the web page using `requests`
# 2. Parse the HTML source code using `BeautifulSoup` library
# 3. Build the scraper components
# 4. Compile the extracted information into Python list and dictionaries
# 5. Write information into a CSV file
# 6. Convert the CSV file into a `Python DataFrame`
# 7. Future work and references

# ### Download the web page using `request`

# >#### **What is `request`**
# 
# >Requests is a Python HTTP library that allows us to send HTTP requests to servers of websites, instead of using browsers to communicate the web.
# 
# >We use `pip`, a package-management system, to install and manage softwares. Since the platform we selected is **Binder**, we would have to type a line of code `!pip install` to install `requests`. You will see lots codes of `!pip` when installing other packages.
# 
# >When we attempt to use some prewritten functions from a certain library, we would use the `import` statement. e.g. When we would have to type `import requests` after installation, we are able to use any function from `requests` library.

# In[150]:


# install the requests package

# In[151]:


import requests


# In[152]:


header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


# In[153]:


base_url = 'https://m.signalvnoise.com'
response = requests.get(base_url, headers=header)
if response.status_code != 200:
    print(f'Failed to fetch webpage {url} with status code {response.status_code}')
else:
    page_content = response.text
    print(len(page_content))


#  ### Parse the HTML source code using `BeautifulSoup` library

# In[154]:



# In[155]:


from bs4 import BeautifulSoup


# In[156]:


doc = BeautifulSoup(page_content, 'html.parser')


# In[157]:


type(doc)


# ### Build the scraper components

# In[158]:


# The get_page function returns the downloaded webpage as a BeautifulSoup object
def get_page(page_number=None):
    base_url = 'https://m.signalvnoise.com'
    if page_number is None:
        url = base_url
    else:
        url = base_url + '/page/' + page_number
    response = requests.get(url, headers=header)
    if response.status_code != 200:
        print(f'Failed to fetch webpage {url} with status code {response.status_code}')
    else:
        page_content = response.text
        print(len(page_content))
        doc = BeautifulSoup(page_content, 'html.parser')
        return doc


# In[159]:


doc = get_page('3')


# ### Compile the extracted information into Python list and dictionaries

# In[160]:


header_tags = doc.find_all('header', class_='entry-header grid__item grid__item--large')


# In[161]:


header_tag = header_tags[0]


# In[162]:


def parse_webpage(header_tag):
    
    # Get title
    h2_tag = header_tag.find('h2', class_='entry-title entry-title--list centered')
    title = h2_tag.text.replace(',', '')
    # Get blog url
    blog_url = h2_tag.find('a')['href'].replace(',', '')
    # Get author
    author_span_tag = header_tag.find('span', class_='byline')
    a_tag = author_span_tag.find('a')
    author = a_tag.text.replace(',', '')
    # Get author url
    author_url = a_tag['href'].replace(',', '')
    # Get published date
    published_date = header_tag.find('time', class_='entry-date published updated').text.replace(',', '')
    # Get author image
    img_div = header_tag.find('div', class_='entry-meta__avatars')
    img_url = img_div.find('img')['src'].replace(',', '')
    return {
        'author name': author,
        'title': title,
        'published_date': published_date,
        'blog url': blog_url,
        'author url': author_url,
        'author image url': img_url
    }


# In[163]:


top_webpages = [parse_webpage(tag) for tag in header_tags]


# In[164]:


def top_webpage():
  header_tags = doc.find_all('header', class_='entry-header grid__item grid__item--large')
  top_webpages = [parse_webpage(tag) for tag in header_tags]
  return top_webpages


# ### Write information into a CSV file

# In[165]:


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


# In[166]:


write_csv(top_webpages, 'three.csv')

