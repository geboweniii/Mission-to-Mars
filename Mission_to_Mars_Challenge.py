#***********************************************************
#10.3.3 - Scrape Mars Data: The News
#***********************************************************
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
 
# pandas line from 10.3.5 - Scrape Mars Data: Mars Facts
import pandas as pd

# set your executable path in the next cell,
#then set up the URL (NASA Mars News (Links to an external site.)) for scraping.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

#set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image

#***********************************************************
# 10.3.4 Scrape Mars Data: Featured Image
#***********************************************************   

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts

#***********************************************************   
# 10.3.5 - Scrape Mars Data: Mars Facts
#***********************************************************
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

#Open url in browser
browser.visit(url)

#get html from website in browser and dump in object
html = browser.html
hemi_soup = soup(html, 'html.parser')
#get div with 'item' class and dump in items object
items = hemi_soup.find_all('div', class_='item')

# 2. Create a list to hold the images and titles.
hemisphere_page_urls = []
hemisphere_image_urls = []
hemisphere_image_titles = []
mars_info = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for item in items:
    hemisphere_page_urls.append(url + item.find('a')['href'])
    #hemisphere_image_titles.append(item.find('h3').text.strip())

for page_url in hemisphere_page_urls:
    mars_hemi = {}
    
    browser.visit(page_url)
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    hemi_image = hemi_soup.find('img', class_='wide-image')
    hemisphere_image_urls.append(url + hemi_image['src'])
    

    hemi_title = hemi_soup.find('h2', class_='title')
    hemisphere_image_titles.append(hemi_title.get_text())
    
    mars_hemi = {
        'img_url': url + hemi_image['src'],
        'title': hemi_title.get_text()
    }
    mars_info.append(mars_hemi)
    
# 4. Print the list that holds the dictionary of each image url and title.
mars_info

hemisphere_image_urls

hemisphere_image_titles

# 5. Quit the browser
browser.quit()

