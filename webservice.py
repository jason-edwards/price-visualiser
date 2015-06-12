__author__ = 'jason'

from flask import Flask, request, redirect
from daemon import Daemon
import platform
import sys
import platform
import datetime

from sqladaptor import DBConnector


WEB_PORT = 5000 if platform.system() == "Darwin" else 8000
app = Flask(__name__)
#app.debug = True

db = DBConnector()


@app.route("/json/", methods=['POST'])
def route_json():
    json_request = request.get_json(force=True)
    if json_request is None or len(json_request) == 0:
        return "JSON request was empty."
    if 'asx_code' not in json_request:
        return "Request must contain 'asx_code'."
    if 'values' in json_request:
        values = json_request['values']
        if type(values) is not list:
            return "'values' should be an array."
        start_date = json_request.get('start_date')
        end_date = json_request.get('end_date')
        print "Parse start"
        if start_date is not None:
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            except TypeError:
                return "Unable to parse 'start_date' : %s" % str(json_request['start_date'])
        print "Parse end"
        if end_date is not None:
            try:
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            except TypeError:
                return "Unable to parse 'end_date' : %s" % str(json_request['end_date'])
        print "Getting database stuff"
        db_result = db.get_pricelog_record(json_request['asx_code'], start_time=start_date, end_time=end_date)
        print "Got database stuff"
        return str([(x.asx_code,x.timestamp) for x in db_result])
    return "Success"


class MyDaemon(Daemon):
    def run(self):
        app.run(host='0.0.0.0', port=WEB_PORT)


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc == 2:
        daemon = MyDaemon('/tmp/webservices.pid')
        if 'start' == sys.argv[1]:
            print "Starting as daemon."
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print "Restarting as daemon."
            daemon.restart()
        else:
            print "usage: %s start|stop|restart\n" % sys.argv[0]
            sys.exit(2)
    else:
        print "Not running as daemon!"
        app.run(host='0.0.0.0', port=WEB_PORT)

print "Exiting"
