__author__ = 'jason'

from flask import Flask, request, redirect
from daemon import Daemon
import platform
import sys


WEB_PORT = 5000 if platform.system() == "Darwin" else 80
app = Flask(__name__)
#app.debug = True


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
