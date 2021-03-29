
import reverb_price_finder.db_mod as db
import reverb_price_finder.notify as notify
import reverb_price_finder.manual_search as manual
import reverb_price_finder.auto_search as auto
import reverb_price_finder.reverb_scraper as scrape
import sys

#APP INFO
app_name = 'Reverb Price Finder'
version = '0.1.0'
author = 'Jonathan Fielder'

#VARS
prompt = 'Enter a command and optional arguements seperated by spaces: '
commands = [
    'help', 'quick_search', 'auto_search', 'exit', 'email_toggle', 'email_sender', 'email_reciever', 
    'email_test', 'search_items', 'add', 'delete_selected', 'delete_all', 'auto_frequency', 'menu'
    ]

help_text ='''
Help:
Enter a command along with optional arguements seperated by a space between each value. 
Format should be as follows: command arg arg (if there are any args to use with the command)

Possible Commands: 

"help" - Prints out this help diolog
    -No arguements

"quick_search" - Runs the quick search function. Can be run with optional arguments.
    -arg 1: item to search reverb.com for
    -arg 2: the number for how many results you would like returned. Must be a whole number
    -arg 3: "lp" to sort by lowest price or "mr" for most recent or "d" for default

"auto_search" - Runs the auto search function based off the saved search items
    -No arguments

"exit" - Exits the program
    -No arguments

"email_toggle" - Turns off or on email notifications for the auto search.
    -arg 1: "on" to set the email toggle to on or "off to set it to off

"email_sender" - Change email address to send the auto search notifications.
    -arg 1: email address
    -arg 2: password for the email

"email_reciever" - Change email address to recieve the auto search notifications.
    -arg 1: email address

"email_test" - Sends a test email so the user can check that their email settings are correct.
    -No arguements

"search_items" - Prints out the saved search items from the user's data base.
    -No arguments

"add" - Adds an item to saved search items in the user's data base.
    -arg 1: name of item to add (Cannot contain spaces in name! Use underscores instead i.e. korg_ms20_mini)
    -arg 2: price floor (Lowest price yu would like totification for. Sorts out items that are 
            too cheap to be the product i.e. cables and stands. Must be a whole number.)
    -arg 3: price ceiling (Highest price you would like to be notified for. Must be a whole number.)

"delete_selected" - Delete selected items from the user's auto search data base.
    -args: can take multiple integer arguements, each integer arg will delete the item that coresponds to 
           that number in the saved list

"delete_all" - Deletes all saved search items from user's data base.
    -No arguments

"auto_frequency" - Sets the frequency the auto search will run in the background while scheduler.py or 
                   scheduler.exe is running.
    -arg 1: an integer for how many hours should pass between each background search

"menu" - Brings up menu options to run commands by picking them from a console menu rather 
         than entering them manually. This is a slower way to use the program but may feel more user friendly.
    -No arguments
'''
def nl(): #saves some headache by adding a new line when called
    print('\n')

#command taker arg cound be set up for runtime console args but I have decided against doing this for now
#command taker takes user input and splits it into a list at each space then calls command runner with list as arg
def command_taker():
    command_str = input(prompt)
    command = command_str.split() #seperates inputs to list
    if command[0] in commands:
            command_runner(command)
    else:
        print('Not a valid command. Enter "help" for a list of possible commands and arguements.')
        command_taker()

#takes list as arg and uses first element of the list to check against possible commands
#if the command exists it runs the function with the list as an arg if there are other arguements to run with command
def command_runner(c):
    if c[0] == 'help':
        print(help_text)
    elif c[0] == 'quick_search':
        manual.man_search(c)
        nl()
    elif c[0] == 'auto_search':
        print('Searching...')
        auto.main()
        print('Search Complete!')
        print('Sending Notification')
        nl()
    elif c[0] == 'exit':
        sys.exit()
    elif c[0] == 'email_toggle':
        emailer_toggle(c)
    elif c[0] == 'email_sender':
        change_email('s', c)
    elif c[0] == 'email_reciever':
        change_email('r', c)
    elif c[0] == 'email_test':
        t = 'test'
        notify.notify_action([[t,t],[t,t],[t,t],[t,t]])
        print('Notification Sent. If no email appears check results_log.txt. If it is in results_log make sure your email settings are correct.')
    elif c[0] == 'search_items':
        print_all_items()
    elif c[0] == 'add':
        add_item(c)
    elif c[0] == 'delete_selected':
        delete_selected(c)
    elif c[0] == 'delete_all':
        delete_all_search(c)
    elif c[0] == 'auto_frequency':
        set_times(c)
    elif c[0] == 'menu':
        main_page()


    #change the stuff to try possible args 1st


#MENUS

def main_page():
    help = '\nType a number to choose one of the options on the screen.\n'
    ch_1 = '1: Email Settings'
    ch_2 = '2: Auto Search Settings'
    ch_3 = '3: Quick Search (Performs a Reverb search for one item)'
    ch_4 = '4: Auto Search (Search saved products now)'
    ch_5 = '5: Exit Program'
    ch_6 = 'Or type "help" for more information.'
    print(ch_1, '\n' + ch_2, '\n' + ch_3, '\n' + ch_4, '\n' + ch_5, '\n' + ch_6)
    
    fil = input()
    nl()

    #CHOICES
    if fil == '1':
        email_settings()
    elif fil == '2':
        auto_search_settings()
    elif fil == '3':
        manual.man_search()
        nl()
        main_page()
    elif fil == '4':
        print('Searching...')
        auto.main()
        print('Search Complete!')
        print('Sending Notification')
        nl()
        main_page()
    elif fil == '5':
        print('Are you sure you want to exit?', '\n1: Yes', '\n2: No')
        user_in = input()
        nl()
        if user_in == '1':
            nl()
            input('Goodbye! Press "Enter" to exit.')
            sys.exit()
        else:
            main_page()
    elif fil == '6' or fil == 'help':
        print(help)
        nl()
        main_page()
    else:
        print('Incorrect input! Try typing "help" to learn more.')
        nl()
        main_page()

def email_settings():
    help = '\nThis is where one can turn off or on email notifications, set a sender eamil, and set a reciever. The sender and reciever may be the same.\n'
    ch_1 = '1: Toggle Email Notifier off/on'
    ch_2 = '2: Change Sender Email'
    ch_3 = '3: Change Recipient Address'
    ch_4 = '4: Send Test Email'
    ch_5 = '5: Main Menu'
    ch_6 = 'Or type "help" for more information.'
    print(ch_1, '\n' + ch_2, '\n' + ch_3, '\n' + ch_4, '\n' + ch_5, '\n' + ch_6)
    
    fil = input()
    nl()

    #CHOICES
    if fil == '1':
        emailer_toggle()
        email_settings()
    elif fil == '2':
        change_email('s')
        email_settings()
    elif fil == '3':
        change_email('r')
        email_settings()
    elif fil == '4':
        t = 'test'
        notify.notify_action([[t,t],[t,t],[t,t],[t,t]])
        print('Notification Sent. If no email appears check results_log.txt. If it is in results_log make sure your email settings are correct.')
        email_settings()
    elif fil == '5':
        main_page()
    elif fil == '6' or fil == 'help':
        print(help)
        nl()
        email_settings()
    else:
        print('Incorrect input! Try typing "help" to learn more.')
        nl()
        email_settings()

def auto_search_settings():
    help = '\nThis is where you can set automatic search parameters.\n'
    ch_1 = '1: View Search Items'
    ch_2 = '2: Add New Search Item'
    ch_3 = '3: Edit Existing Search Items'
    ch_4 = '4: Delete Select Search Items'
    ch_5 = '5: Delete All Search Items'
    ch_6 = '6: Set How Often to Run Autosearch in the Background'
    ch_7 = '7: Main Menu'
    ch_8 = 'Or type "help" for more information.'
    print('Auto Search Settings:')
    print(ch_1, '\n' + ch_2, '\n' + ch_3, '\n' + ch_4, '\n' + ch_5, '\n' + ch_6, '\n' + ch_7)
    
    fil = input()
    nl()
    if fil == '1':
        print_all_items()
        nl()
        auto_search_settings()
    if fil == '2':
        add_item()
        nl()
        auto_search_settings()
    if fil == '3':
        edit_search_item()
        nl()
        auto_search_settings()
    if fil == '4':
        delete_selected()
        nl()
        auto_search_settings()
    if fil == '5':
        delete_all_search()
        nl()
        auto_search_settings()
    if fil == '6':
        set_times()
        nl()
        auto_search_settings()
    if fil == '7':
        main_page()
    if fil == 'help':
        print(help)
        nl()
        auto_search_settings()
    else:
        print('Incorrect Input.')
        auto_search_settings()

#EMAIL SETTINGS

def emailer_toggle(c = []):
    data = db.Data_Base('data')
    fil = ''
    if len(c) >= 2:
        if c[1] == 'on':
            fil = '1'
        elif c[1] == 'off':
            fil = '2'
        else:
            emailer_toggle()
            return
    else:
        ch_1 = '1: Email Notifier On'
        ch_2 = '2: Email Notifier Off'
        print(ch_1, '\n' + ch_2)
        fil = input()
        nl()
    if fil == '1' or fil == '2':
        results = data.query("""SELECT * from email_toggle limit 1""")
        if results: #if anything in table delete
            data.c_ex('DELETE FROM email_toggle')
        s_email = data.query_all('email_s')
        r_email = data.query_all('email_r')
        if s_email and r_email: #checks if email exists in db before able to turn on
            data.c_ex_it(' INSERT INTO email_toggle VALUES(?)', (fil,))
            if fil == '1':
                print('Email sender set to On.')
            elif fil == '2':
                print('Email sender set to Off.')
        else:
            print('Cannot turn on Email Notifier without first entering email addresses for sender and reciever.')
    else:
        print('Invalid Input.')
    data.close()

def change_email(arg, info = []):
    if arg == 's':
        if len(info) >= 3:
            email = info[1]
            password = info[2]
            data = db.Data_Base('data')
            results = data.query("""SELECT * from email_s limit 1""")
            if results:
                data.c_ex('DELETE FROM email_s')
            data.c_ex_it(' INSERT INTO email_s VALUES(?,?)', (email, password))
            data.close()
            print('Email sender set to {}'.format(email))
        else:
            data = db.Data_Base('data')
            results = data.query("""SELECT * from email_s limit 1""")
            data.close()
            if results:
                print('Current email set to {}. Would you like to change this?'.format(results[0][0]))
                print('1: Yes \n2: No')
                choice = input()
                nl()
                if choice == '2':
                    print('No changes made to Sender Email.')
                    return
                elif choice == '1':
                    pass
                else:
                    print('Invalid Input.')
                    change_email('s')
            print('Enter sender email address.')
            email = input()
            nl()
            print('Enter email password.')
            password = input()
            nl()
            print('Set email sender to {} and password to {}?'.format(email, password))
            print('1: Yes \n2: No')
            fil = input()
            nl()
            if fil == '1':
                data = db.Data_Base('data')
                results = data.query("""SELECT * from email_s limit 1""")
                if results:
                    data.c_ex('DELETE FROM email_s')
                data.c_ex_it(' INSERT INTO email_s VALUES(?,?)', (email, password))
                data.close()
            elif fil =='2':
                print('No changes made to Sender Email.')
            else:
                print('Error: Incorrect Input')
                change_email('s')
    elif arg == 'r':
        if len(info) >= 2:
            email_r = info[1]
            data = db.Data_Base('data')
            results = data.query("""SELECT * from email_r limit 1""")
            if results:
                data.c_ex('DELETE FROM email_r')
            data.c_ex_it(' INSERT INTO email_r VALUES(?)', (email_r,))
            data.close()
            print('Email receiver is set to {}'.format(email_r))
        else:
            print('Enter receiver email address.')
            email_r = input()
            nl()
            print('Set email receiver to {}?'.format(email_r))
            print('1: Yes \n2: No')
            fil = input()
            nl()
            if fil == '1':
                data = db.Data_Base('data')
                results = data.query("""SELECT * from email_r limit 1""")
                if results:
                    data.c_ex('DELETE FROM email_r')
                data.c_ex_it(' INSERT INTO email_r VALUES(?)', (email_r,))
                data.close()
            elif fil == '2':
                print('Email receiver not changed.')
            else:
                print('Error: Incorrect Input')
                change_email('r')


#AUTO SEARCH SETTINGS

def print_all_items():
    data = db.Data_Base('data')
    items = data.query_all('search_items')
    x = 1
    print('{:50}|{:15}|{}'.format('Product','Price Floor','Price Ceiling'))
    for i in items:
        print('{}: {:47} {:15} {}'.format(x, i[0], i[1], i[2]))
        x += 1
    data.close()

def add_item(info = []):
    sql = "INSERT INTO search_items VALUES (?,?,?)"
    try:
        prod_name = info[1]
    except IndexError:
        print('Enter product name.')
        prod_name = input()
    try:
        low_price = info[2]
    except IndexError:
        print('Enter price floor.')
        low_price = input()
    try:
        high_price = info[3]
    except IndexError:
        print('Enter price ceiling.')
        high_price = input()
    try:
        #make sure price floor and ceiling are numbers
        test = int(low_price)
        test2 = int(high_price)
        data = db.Data_Base('data')
        data.c_ex_it(sql, (prod_name, low_price, high_price))
        data.close()
        print(f'{prod_name} | {low_price} | {high_price} added to search items.')
    except:
        print('Price floor and price ceiling must both be whole numbers.')

def edit_search_item():
    print_all_items()
    print('Enter the number for the item to edit.')
    num = input()
    nl()
    if num.isnumeric():
        num = int(num)
        num -= 1
        data = db.Data_Base('data')
        items = data.query_all('search_items')
        data.close()
        if num <= len(items):
            item_replace = items[num]
            item_name = item_replace[0]
            print(item_name)
            print('Enter product name.')
            prod_name = input()
            print('Enter price floor.')
            low_price = input()
            print('Enter price ceiling.')
            high_price = input()
            data = db.Data_Base('data')
            #data.c_ex('DELETE FROM search_items WHERE product = (?)',(item_name,))
            data.c_ex_it('UPDATE search_items SET product=?, lowest_price=?, highest_price=? WHERE product=?', [prod_name, low_price, high_price, item_name])
            data.close()
            print('Product updated.')
        else:
            print('Index out of range.')
    else:
        print('Invalid input!. Must be an integer.')
        
def delete_selected(position = []):
    if len(position) >= 2:
        position = position[1:] #removes first element of the list so all that is left is list of positions
        #this allows multiple indexes to be deleted in one line
        #running this func directly allows multiple to be deleted without confirmation needed
        for p in position:
            num = p
            if num.isnumeric():
                num = int(num)
                num -= 1
                data = db.Data_Base('data')
                items = data.query_all('search_items')
                data.close()
                if num <= len(items):
                    item_delete = items[num]
                    item_name = item_delete[0]
                    data = db.Data_Base('data')
                    data.c_ex_it('DELETE FROM search_items WHERE product = (?)',(item_name,))
                    data.close()
                    print('Product deleted.')
                else:
                    print('Index out of range.')
            else:
                print('Invalid input! Must be an integer.')
    else:
        print_all_items()
        print('Enter the number for the item to edit.')
        num = input()
        nl()
        if num.isnumeric():
            num = int(num)
            num -= 1
            data = db.Data_Base('data')
            items = data.query_all('search_items')
            data.close()
            if num <= len(items):
                item_delete = items[num]
                item_name = item_delete[0]
                print(item_name)
                print('Are you sure you would like to delete{}? \n1: Yes \n2: No')
                fil = input()
                if fil == '1':
                    data = db.Data_Base('data')
                    data.c_ex_it('DELETE FROM search_items WHERE product = (?)',(item_name,))
                    data.close()
                    print('Product deleted.')
                elif fil == '2':
                    print('Product not deleted.')
                else:
                    print('Invalid input.')
            else:
                print('Index out of range.')
        else:
            print('Invalid input!. Must be an integer.')

def delete_all_search(arg = None):
    sql = 'DELETE FROM search_items'
    if arg:
        data = db.Data_Base('data')
        data.c_ex(sql)
        data.close()
        print('All search items deleted')
    else:
        print_all_items()
        print('Would you like to delete all items in search database?')
        print('1: Yes \n2: No')
        fil = input()
        nl()
        if fil == '1':
            data = db.Data_Base('data')
            data.c_ex(sql)
            data.close()
            print('All search items deleted')
        elif fil == '2':
            print('Search items not deleted.')
        else:
            print('Incorrect Input.')
            delete_all_search()

def set_times(inter = []):
    try:
        new_intervals = inter[1]
        try:
            new_intervals = int(new_intervals)
            if new_intervals >= 0:
                data = db.Data_Base('data')
                data.c_ex('DELETE FROM schedule')
                data.c_ex_it(""" INSERT INTO schedule VALUES(?)""", (new_intervals,))
                data.close()
                print('Auto search will run every {} hours.'.format(new_intervals))
            else:
                print('Interval must be a whole number.')
        except:
            print('Second arguement must be a whole number.')
            set_times()
    except IndexError:
        data = db.Data_Base('data')
        intervals = data.query_all('schedule')
        data.close()
        if intervals[0][0] > 1:
            plur = 's'
        else:
            plur = ''
        print('Reverb Auto Searcher currently runs every {} hour{}. Would you like to change this?'.format(intervals[0][0], plur))
        print('1: Yes \n2: No')
        fil = input()
        nl()
        if fil == '1':
            print('Enter a number for how many hours should pass between each search.')
            new_intervals = input()
            try:
                new_intervals = int(new_intervals)
                if new_intervals >= 0:
                    data = db.Data_Base('data')
                    data.c_ex('DELETE FROM schedule')
                    data.c_ex_it(""" INSERT INTO schedule VALUES(?)""", (new_intervals,))
                    data.close()
                    print('Auto search will run every {} hours.'.format(new_intervals))
                else:
                    print('Must enter a whole number.')
            except:
                print('Must enter a whole number.')
                set_times()
        elif fil == '2':
            print('Schedule unchanged.')
        else:
            ('Incorrect Input.')
            set_times()



#INITIALIZE DB AND TABLES
def db_init():
    data = db.Data_Base('data')
    data.c_ex("""CREATE TABLE IF NOT EXISTS email_s (
            email text,
            password text
        )""")
    data.c_ex("""CREATE TABLE IF NOT EXISTS email_r (
            email text
        )""")
    data.c_ex("""CREATE TABLE IF NOT EXISTS email_toggle (
            email_toggle_state text
        )""")
    data.c_ex("""CREATE TABLE IF NOT EXISTS schedule (
            intervals integer
        )""")


    data.c_ex("""CREATE TABLE IF NOT EXISTS search_items (
            product text,
            lowest_price text,
            highest_price text
        )""")
    
    #init email toggle to off
    results = data.query_all('email_toggle')
    if not results:
        data.c_ex_it(""" INSERT INTO email_toggle VALUES(?)""", ('2',))
        
    #init auto times
    times_a_day = data.query_all('schedule')
    if not results:
        data.c_ex_it(""" INSERT INTO schedule VALUES(?)""", (4,))

    data.close()




def main():
    #INIT
    print('{} {} by {}.'.format(app_name, version, author))
    print('Welcome to {}!'.format(app_name))
    db_init()
    while True:
        command_taker()



if __name__ == '__main__':
    main()
