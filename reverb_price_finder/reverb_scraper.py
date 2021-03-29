
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup



def reverb_scrape(item, search_limit = '40', sort = 'mr'):
    #init search settings and url
    item = item
    search_lim = search_limit

    lp = '&sort=price|asc' #from lowest price
    mr = '&sort=published_at|desc' #from most recent
    
    #set search lim as type int
    if search_lim == 'd':
        search_lim = '40'
    if search_lim.isdigit():
        search_lim = int(search_lim)
    else:
        return 'Error: Search_limit must be an integer or "d".'

    url_base = 'https://reverb.com/marketplace?query='
    url = url_base+item

    if sort == 'lp':
        url += lp
    elif sort == 'mr':
        url += mr
    elif sort == 'd':
        url = url

    #open session
    try:
        session = HTMLSession()
        response = session.get(url)
        response.html.render(timeout = 10, sleep = 5)

    except requests.exceptions.RequestException as e:
        return(e)

    soup = BeautifulSoup(response.html.raw_html, 'html.parser')

    #search soup for needed items and create lists
    title_tags = soup.find_all('h4', class_ = 'grid-card__title', limit = search_lim)
    titles = [title.get_text() for title in title_tags]
    
    price_tags = soup.find_all('div', class_ = 'grid-card__price', limit = search_lim)
    prices = [price.get_text() for price in price_tags]
    
    link_tags = soup.find_all('a', class_ = 'grid-card__inner', limit = search_lim)
    links = [link['href'] for link in link_tags]
    
    condition_tags = soup.find_all('div', class_ = 'condition-display__label', limit = search_lim)
    conditions = [condition.get_text() for condition in condition_tags]


    #lists to dict
    listings = [titles, prices, links, conditions]

    return listings


#TESTING
#
#
def scrape_test():
    q = reverb_scrape('microkorg', '10', 'lp')

    if isinstance(q,list):
       formatted_print(q) 

    #if returns an error
    else:
        print(q)

def formatted_print(q):
    q = q
    for i in range(len(q[0])):
        print('product: {:65}| Price: {:15}| Condition: {}'.format(q[0][i][:55], q[1][i], q[3][i]))
        print('URL: {}\n'.format(q[2][i]))





def main():

    scrape_test()

if __name__ == '__main__':
    main()


