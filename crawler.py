import requests
import pandas as pd
from googletrans import Translator
from bs4 import BeautifulSoup

ACCESS_KEY = '' # Register to https://fixer.io/ to get the API KEY

def scrape():
    '''
    Function that scrapes the website http://books.toscrape.com/
    and gets the id, title, price, rating and picture url for
    each book
    '''
    num_pages = 1
    book_id = 0
    ids = []
    titles = []
    ratings = []
    prices = []
    picture_urls = []

    # Map dictionary for ratings
    rating_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    # Define total number of pages to scrape
    for i in range(1, num_pages+1):
        response = requests.get('http://books.toscrape.com/catalogue/page-' + str(i) + '.html')

        soup = BeautifulSoup(response.content, "html.parser")

        books = soup.find_all("article", class_="product_pod")
        
        for book in books:
            ids.append(book_id)
            titles.append(book.h3.a.get('title'))
            ratings.append(rating_dict[book.p['class'][1]])
            prices.append(book.find('p', class_="price_color").text[1:])
            picture_urls.append(book.div.a.img.get("src"))

            book_id += 1 # increment id

    return ids, titles, ratings, prices, picture_urls


def get_book_text(title):
    '''
    Generate text using the API from https://deepai.org/machine-learning-model/text-generator
    '''
    # Should implement error handling
    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            'text': f'The text of {title} is:',
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )
    return r.json()

def gbp_to_eur(amount):
    ''''
    Converts the given amount in GBP to EUR using API from https://fixer.io/
    '''
    #url = f"http://data.fixer.io/api/latest?access_key={ACCESS_KEY}&base=GBP&symbols=EUR"
    #data = requests.get(url).json()
    #rates = data["rates"] 

    initial_amount = amount
    if not isinstance(amount, float):
        amount = float(amount)
    # limiting the precision to 2 decimal places
    #return round(amount * rates['EUR'], 2)
    return round(amount * 1, 2)


def translate(text, lang_from, lang_to):
    '''
    Translate text from lang_from to lang_to
    '''
    translator = Translator()
    return translator.translate(text, src=lang_from, dest=lang_to)
     
def export(data, destination):
    '''
    Function to export given data to CSV file
    '''
    df = pd.DataFrame.from_dict(data)

    df.to_csv(destination, index=False)


if __name__ == "__main__":  
    ids, titles, ratings, prices_gbp, picture_urls = scrape()
    
    texts = [get_book_text(title) for title in titles]
    prices_eur = [gbp_to_eur(price) for price in prices_gbp]

    # Translate text into spanish and italian
    texts_es = [translate(text,'en','es') for text in texts]
    texts_it = [translate(text,'en','it') for text in texts]

    data = {
        'id': ids,
        'title': titles,
        'rating': ratings,
        'price_gbp': prices_gbp,
        'price_eur': prices_eur,
        'picture_url': picture_urls,
        'text_en': texts,
        'text_es': texts_es,
        'text_it': texts_it
    }
    export(data, 'export.csv')


