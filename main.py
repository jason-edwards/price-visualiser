from trial import DBConnector, DataGrabber
from flask import Flask, render_template
from daemon import Daemon

import threading
import platform
import time
import sys

app = Flask(__name__)
datagrab_thread = None

@app.route("/table")
@app.route("/table/<code>")
def table(code=None):
    if code is None:
        return "usage: ip_address/table/asx code"

    data = DBConnector()
    code, price, timestamp = data.get_current_record(code)
    return render_template('price.html', code=code, price=price, timestamp=timestamp)


@app.route("/graph")
@app.route("/graph/<code>")
def graph(code=None):
    if code is None:
        return "usage: ip_address/graph/asx code"

    data = DBConnector()
    query = data.get_records_by_timeframe(code)

    prices = []
    timestamps = []
    for rows in query:
        prices.append(float(rows.price))
        timestamps.append(str(rows.timestamp))
    prices.insert(0, "price")
    timestamps.insert(0, "timestamps")

    return render_template('graph.html', prices=str(prices), timestamps=str(timestamps))


class DataGrabThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keep_running = True


    def run(self):
        asx_codes_array = ["anz", "cba", "wbc", "cim"]
#        asx_codes_array = ["cba"]
        data_grabber = DataGrabber()
        while self.keep_running:
            for asx_code in asx_codes_array:
                data_grabber.data_grab(asx_code)
            time.sleep(5)


def web_service():
    port = 80
    if platform.system() == "Darwin":
        port = 5000

    app.run(host='0.0.0.0', port=port)


class MyDaemon(Daemon):
    def run(self):
        datagrab_thread = DataGrabThread()
        datagrab_thread.start()
        web_service()

if __name__ == "__main__":

    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "Not running as daemon!"
        print "usage: %s start|stop|restart" % sys.argv[0]
        print '\n'

        datagrab_thread = DataGrabThread()
        datagrab_thread.start()
        web_service()

    if datagrab_thread is not None:
        print "Waiting for datagrab thread"
        datagrab_thread.keep_running = False
        datagrab_thread.join()
    print "Exiting"
