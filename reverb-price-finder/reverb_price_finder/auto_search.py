import reverb_price_finder.reverb_scraper as scrape
import reverb_price_finder.notify as n
import reverb_price_finder.db_mod as db


def search_items():
    data = db.Data_Base('data')
    searches = data.query_all('search_items')
    data.close()
    return(searches)

def scrape_ret(searches):
    if searches:
        prod = []
        price = []
        link = []
        cond = []
        if isinstance(searches, list):
            for search in searches: #for each search query
                search_returns = (scrape.reverb_scrape(search[0])) #search[0] search item name
                for x in range(len(search_returns[0])): #assign each return query item to new formmatted list
                    try: #if price not float it is not included/ if price not in set range not included in results
                        if float(search_returns[1][x][1:]) >= float(search[1]) and float(search_returns[1][x][1:]) <= float(search[2]): #slice $ with [1:]
                            prod.append(search_returns[0][x])
                            price.append(search_returns[1][x])
                            link.append(search_returns[2][x])
                            cond.append(search_returns[3][x])
                    except:
                        pass
            sorted = [prod, price, link, cond] #construct proper list format with returns from price check against logic
            if len(sorted) > 0:
                n.notify_action(sorted)
    else: 
        print('No saved items to search! Be sure to add items to search in auto search settings.')





def main():
    scrape_ret(search_items())

if __name__ == '__main__':
    main()