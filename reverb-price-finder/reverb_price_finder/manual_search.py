import reverb_price_finder.reverb_scraper as scrape


def man_search(search = 0):
    try:
        item = search[1]
    except IndexError:
        print('Enter the name of an item to search for on Reverb.com.')
        item = input()
    try:
        search_ret = search[2]
    except  IndexError:
        print('Enter a number for how many results you would like returned.')
        search_ret = input()
    try:
        sort_search = search[3]
    except IndexError:
        print('Enter "lp" to sort by lowest price or "mr" for most recent or "d" for default.')
        sort_search = input()
    print('Searching...')

    q = scrape.reverb_scrape(item, search_ret, sort_search)

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
    while True:
        man_search()

if __name__ == '__main__':
    main()