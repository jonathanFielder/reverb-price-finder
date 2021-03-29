
import schedule
import time
import reverb_price_finder.auto_search as auto
import reverb_price_finder.db_mod as db

x = 0
intervals = 0
def on_start():
    global x
    x = 1
    data = db.Data_Base('data')
    interval_ret = data.query_all('schedule')
    data.close()
    return interval_ret



schedule.every(intervals).hours.do(auto.main)


def main():
    global intervals
    while True:
        if x == 0:
            intervals = on_start()
            intervals = intervals[0][0]
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()

