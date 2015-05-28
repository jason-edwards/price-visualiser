from bs4 import BeautifulSoup
from selenium import webdriver
import requests as req
import peewee as pw
import datetime
import platform
import re
import csv
import urllib2


DATABASE_USER = 'pricevis'

try:
    f = open(DATABASE_USER + '.passwd', 'r')
    passwd = f.read()[:-1]
except IOError:
    print "Cannot open database password file. Password file should be named <db-user>.passwd"
else:
    f.close()
db = pw.MySQLDatabase('shares_db', host='127.0.0.1', user=DATABASE_USER, password=passwd)


class BaseModel(pw.Model):
    class Meta:
        database = db


class DataGrabber():

    def __init__(self):
        pass

    def data_grab(self, code):
        current_price = 0
        try:
            url_string = "http://search.asx.com.au/s/search.html?query=" + code + "&collection=asx-meta&profile=web"

            if platform.system() == "Darwin":
                browser = webdriver.PhantomJS()
            else:
                browser = webdriver.PhantomJS('/home/ubuntu/Trial/price-visualiser/phantomjs')
            browser.get(url_string)
            browser.execute_script("return document.cookie")
            browser.execute_script("return navigator.userAgent")
            html_source = browser.page_source
            browser.close()

            soup = BeautifulSoup(html_source)

            prices_table = soup.find("table").find("tbody")
            current_price = prices_table.find_all("td")[0].get_text()

        except AttributeError:
            try:
                url_string = "https://au.finance.yahoo.com/q/pr?s=" + code + ".AX"

                if platform.system() == "Darwin":
                    browser = webdriver.PhantomJS()
                else:
                    browser = webdriver.PhantomJS('/home/ubuntu/Trial/price-visualiser/phantomjs')

                browser.get(url_string)
                browser.execute_script("return document.cookie")
                browser.execute_script("return navigator.userAgent")
                html_source = browser.page_source
                browser.close()

                soup = BeautifulSoup(html_source)

                search_id_string = "yfs_l84_" + code + ".ax"
                current_price = soup.find(id=search_id_string).get_text()
            except AttributeError:
                print "Attribute Error: bs4.find() could not retrieve text for %s." % asx_codes_array[i]
                print "Check the status of the webpage."
                pass

        print(code, current_price)

        price_log = PriceLog(
            asx_code=code,
            price=current_price,
            timestamp=datetime.datetime.now()
        )

        price_log.save()
        return 0

    def historic_data_grab(self, code):
        url_string = "https://au.finance.yahoo.com/q/hp?s=" + code + ".AX"

        page = req.get(url_string)
        html_source = page.text

        soup = BeautifulSoup(html_source)
        search_id_string = 'rightcol'
        try:
            file_url = (soup.find(id=search_id_string)
                        .find_all('a', href=re.compile('^http://real-chart.finance'))[0].get('href'))
        except AttributeError:
            print "Attribute Error: bs4.find() could not retrieve text for %s." % code
            print "Check the status of the webpage."
            return 404

        csv_file = urllib2.urlopen(file_url)
        reader = csv.reader(csv_file)

        print "%s history read." % code
        row_number = 0
        data_array = []

        # Construct data_array to contain dictionary of price_log data.
        for row in reader:
            if row_number != 0:
                # Columns are - Date, Open, High, Low, Close, Volume, Adjusted Close

                # Add in database for the price at open. The time is 10:00:00 AEST -> 00:00:00 UTC
                date_string = row[0] + " 00:00:00"
                time = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

                data = {'asx_code': code, 'price': row[1], 'timestamp': time}
                data_array.append(data)

                # Add in database for the price at open. The time is 10:00:00 AEST -> 00:00:00 UTC
                date_string = row[0] + " 06:00:00"
                time = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

                data = {'asx_code': code, 'price': row[4], 'timestamp': time}
                data_array.append(data)
            row_number += 1

        db_instance = DBConnector()
        insert_array = []
        skipped_array = []
        for element in data_array:
            query = db_instance.get_records_by_date(code=element['asx_code'], date=element['timestamp'])
            if query.count() == 0:
                insert_array.append(element)
            else:
                skipped_array.append(element)

        PriceLog.insert_many(insert_array).execute()

        print len(insert_array), "items inserted"
        print len(skipped_array), "items skipped for", code
        return 0


class DBConnector():

    def get_current_record(self, code):
        query = (PriceLog
                 .select()
                 .where(PriceLog.asx_code == code)
                 .order_by(PriceLog.timestamp.desc())
                 .get())

        return query.asx_code, query.price, query.timestamp

    def get_records_by_timeframe(self, code, start_time=(datetime.datetime.now() - datetime.timedelta(days=14)),
                                 end_time=datetime.datetime.now()):

        query = (PriceLog
                 .select()
                 .where((PriceLog.asx_code == code) & (PriceLog.timestamp > start_time) &
                        (PriceLog.timestamp < end_time))
                 .order_by(PriceLog.timestamp.desc()))
        return query

    def get_records_by_date(self, code, date):

        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        except TypeError:
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        start_time = date
        end_time = date + datetime.timedelta(days=1)

        query = (PriceLog
                 .select()
                 .where((PriceLog.asx_code == code) & (PriceLog.timestamp > start_time) &
                        (PriceLog.timestamp < end_time))
                 .order_by(PriceLog.timestamp.desc()))
        return query



class PriceLog(BaseModel):
    id = pw.PrimaryKeyField()
    asx_code = pw.CharField()
    price = pw.DecimalField()
    timestamp = pw.DateTimeField()

"""
def clean_up():
    db.close()
"""
