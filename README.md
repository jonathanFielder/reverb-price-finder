Reverb Price Finder
=============

Reverb Price Finder is a tool that scrapes Reverb.com so users don't miss the best deals.



Installation
---------------

Requirements:
* Windows
* [Additional Requirements](requirements.txt)


Usage
--------------

This tool can be used to manually search the website for specific products or to automatically search in the 
background based off of products and price ranges the user can specify ahead of time.

The exe versions of reverb-price-finder and scheduler work as stand alone apps without installing any of the python dependencies or running a vertual environment. The .py versions require the dependencies and should be run in a vertual environment. 

When using the auto search functionality the program will notify the user when products are in their price range
by writing to a log file named results_log.txt. It is also possible to add email information so that the user will 
recieve an email notification when a product meets the price window. 
results_log.txt should be periodically cleaned out by the user to keep it easy to read.

Suggested use for optimal Auto Search functionality:
I built the Auto Search to be run in the background so the user can set gear and price points they 
would like to by the gear at. This is to help the user catch deals quickly on gear they want without constantly
looking at Reverb.com. I suggest adding gear to the Auto Search Settings menu with a price floor that 
filters out items that are too cheap to be the actual gear (i.e. cables and stands) and setting the price 
ceiling to a level that filters out the items priced above how much you would like to pay. This will help you to 
only recieve notifications for the deals you want to find.

In order to run the auto search periodically in the background the user can either start auto_schedule.py
manually or [add it to their start up programs](https://stackoverflow.com/questions/4438020/how-to-start-a-python-file-while-windows-starts).

auto_schedule.py runs the auto_search module periodically based on how often you set it to run in choice 6
of the Auto Search Settings menu (set to every 4 hours by default).

In order for the email notifications to work with gmail,
the user must first set [Allow Less Secure Apps](https://myaccount.google.com/lesssecureapps) to on.

I recommend setting up a new gmail account as your sender account as this can be a security risk.

When using the test email option check the results_log.txt to see that the test went through.
If the test is in results_log.txt but the email notification did not work: 
First check that your sender email and password are correct.
Check that your receiving email address is correct.
Check the 'Allow less secure apps' setting is set to on for your sending email account.
Be sure that 'Toggle Email Notifier off/on' is set to on in email settings menu un Reverb Price Finder.



Contributing
---------------
This is a project I made to practice my webscraping. If any of this code is helpful to your project 
you are welcome to use it however you please. I have no plans to add to this code in the future. 

License
---------------
MIT <https://www.mit.edu/~amini/LICENSE.md>