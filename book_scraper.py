import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

url="https://books.toscrape.com/catalogue/page-{}.html"
titles=[]
prices=[]
availability=[]
for page in range(1,51):
    main_url=url.format(page)
    response=requests.get(main_url)
    if response.status_code != 200:
        break
    soup=BeautifulSoup(response.content,"html.parser")
    books=soup.find_all('article',class_="product_pod")

    for book in books:
        title=book.h3.a['title']
        price_tag=book.find('p',class_="price_color")
        price=price_tag.text if price_tag else "N/A"
        available_tag=book.find('p',class_="instock availability")
        available=available_tag.text.strip() if available_tag else "N/A"
        titles.append(title)
        prices.append(price)
        availability.append(available)
    print(f"Scraped page {page}")
    time.sleep(1)

df=pd.DataFrame({
    'Title':titles,
    'Prices':prices,
    'Availability':availability
})

df.to_csv('all_books.csv', index=False)
print("All books scraped and saved to all_books.csv")