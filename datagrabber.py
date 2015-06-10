__author__ = 'jason'

from selenium import webdriver
from daemon import Daemon
import platform
import datetime
import sys
from time import time
from bs4 import BeautifulSoup
from sqladaptor import PriceLog


class DataGrabber():

    def __init__(self):
        self.browser = webdriver.PhantomJS('./phantomjs') if platform.system() != "Darwin" else webdriver.PhantomJS()
        self.keep_running = True

    def cleanup(self):
        self.browser.close()

    def run(self):
        asx_codes_array = ["anz", "cba", "wbc", "cim"]
        #asx_codes_array = ["cba"]
        print "Starting datagrab thread loop. This message should only appear once."
        while self.keep_running:
            seconds = 0
            for asx_code in asx_codes_array:
                print "Executing datagrab(%s)" % asx_code
                data_grabber.data_grab(asx_code)
            print "Sleeping."
            while seconds < DATAGRAB_SLEEP_TIME and self.keep_running:
                time.sleep(1)
                seconds += 1
        data_grabber.cleanup()

    def data_grab(self, code):
        start_time = time()
        current_price = 0
        url_list = ["http://search.asx.com.au/s/search.html?query=%s&collection=asx-meta&profile=web" % code,
                    "https://au.finance.yahoo.com/q/pr?s=%s.AX" % code]
        print "\tGetting asx price."

        for url in url_list:
            try:
                self.browser.get(url)
                break
            except:
                print "Error getting URL."
        self.browser.execute_script("return document.cookie")
        self.browser.execute_script("return navigator.userAgent")
        html_source = self.browser.page_source

        request_time = time() - start_time
        print "\tTook %.2f seconds to get response." % request_time

        soup = BeautifulSoup(html_source)

        if url == url_list[0]:
            try:
                prices_table = soup.find("table").find("tbody")
                current_price = prices_table.find_all("td")[0].get_text()
            except AttributeError:
                print "\tUnable to scrape this time."
                return 1
        elif url == url_list[1]:
            search_id_string = "yfs_l84_%s.ax" % code
            current_price = soup.find(id=search_id_string).get_text()

        print "\t%s\t%s" % (code, current_price)

        price_log = PriceLog(
            asx_code=code,
            price=current_price,
            timestamp=datetime.datetime.now()
        )

        try:
            price_log.save()
        except:
            print "\tError saving to database."

        finish_time = time() - start_time
        print "\tSaved in database. Total time: %.2f" % finish_time
        return 0


class MyDaemon(Daemon):
    def run(self):
        data_grabber = DataGrabber()
        data_grabber.run()


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc == 2:
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if 'start' == sys.argv[1]:
            print "Starting as daemon."
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print "Restarting as daemon."
            daemon.restart()
        elif 'history' == sys.argv[1]:
            print "usage: %s history code" % sys.argv[0]
            sys.exit(2)
        else:
            print "usage: %s start|stop|restart\n" % sys.argv[0]
            sys.exit(2)
    elif argc == 3:
        if 'history' == sys.argv[1]:
            data_grabber = DataGrabber()
            result = data_grabber.historic_data_grab(sys.argv[2])
        else:
            print "Unknown argument %s" % sys.argv[1]
            print "usage: history <asx_code>"

        if result == 0:
            print "Database populated with historic data for %s" % sys.argv[2]
        elif result == 404:
            print "Could not find file for \'%s\'." % sys.argv[2]
            print "Check if code is valid."
    else:
        print "Not running as daemon!"
        data_grabber = DataGrabber()
        data_grabber.run()

print "Exiting"