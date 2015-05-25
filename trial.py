from bs4 import BeautifulSoup
from selenium import webdriver
#import requests as req
import peewee as pw
import datetime
import platform

db = pw.MySQLDatabase('shares_db', host='127.0.0.1', user='root', password='a113fea')


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
                browser = webdriver.PhantomJS('/home/ubuntu/Trial/phantomjs')

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
                    browser = webdriver.PhantomJS('/home/ubuntu/Trial/phantomjs')

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


class PriceLog(BaseModel):
    id = pw.PrimaryKeyField()
    asx_code = pw.CharField()
    price = pw.DecimalField()
    timestamp = pw.DateTimeField()

"""
def clean_up():
    db.close()
"""
