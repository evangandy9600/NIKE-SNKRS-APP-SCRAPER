import re
import requests
from bs4 import BeautifulSoup
import csv
import time
import os

t0 = time.time()

shoe_num = 0
sites = []
sku_list = []
master = []
header_row = ['SKU', 'Release Date', 'Shoe Type', 'Shoe Name', 'Price', 'Image Link']

snkrs = open('snkrs.csv', mode='w', newline="", encoding='utf_8')
csvwriter = csv.writer(snkrs)
csvwriter.writerow(header_row)

def get_url(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc

def clean(raw_html):
    cleaner = re.compile('<.*?>')
    cleantext = re.sub(cleaner, '', raw_html)
    return cleantext

def img_url(img, sku):
    new_sku = sku.split("-")
    return f'https://secure-images.nike.com/is/image/DotCom/{new_sku[0]}_{new_sku[1]}_{img}_PREM?$SNKRS_COVER_WD$&align;'


url = 'https://www.nike.com/launch?s=upcoming'
a_tags = get_url(url).find_all('a', {'data-qa': 'product-card-link'})
for tag in a_tags:
    shoe_num += 1

    href = tag['href']
    website = (f'https://nike.com{href}')
    page = get_url(website)

    sku_parent = page.find('meta', {'name' : "branch:deeplink:styleColor"})
    sku = sku_parent['content']

    if sku in sku_list:
        pass
    else:
        sku_list.append(sku)
        shoe_name = page.find('h5', class_ = "headline-1 pb3-sm").string
        shoe_type = page.find('h1', class_ = "headline-5 pb3-sm").string
        description = page.find('div', class_ = "description-text text-color-grey").string
        price = page.find('div', class_="headline-5 pb6-sm fs14-sm fs16-md").string
        date = str(page.find('div', {'class' : 'available-date-component'}))
        image_url = img_url('E', sku)
        release = 'Released'

        try:
            month_day = list(clean(date).split(" "))
            release = month_day[1]
        except:
            pass
        
        image_name = shoe_name.replace(' ', '-')
        with open(f'SNKRS/{image_name}.jpg', 'wb') as f:
            im = requests.get(image_url)
            f.write(im.content)

        SHOE = [sku, release, shoe_type, shoe_name, price, image_url]
        master.append(SHOE)

        t1 = t0-time.time()
        print(f'Shoe ({shoe_num}) Completed in {-round(t1, 4)} seconds')

for i in master:
    csvwriter.writerow(i)
print(f'\n{shoe_num} shoes exported to "snkrs.csv"')
print(f'{shoe_num} shoes exported as "jpeg"')
print(f'Completed in {-round(t0-time.time(), 2)} seconds')