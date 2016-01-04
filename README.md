#Price Visualiser

This software aims to collect stock market data and global news data. It will analyse the data and display it in various graphical representations. The idea is to create a simple to use, readable representations of stock market & global event correlations.

####FILES
Python (v 3.4.4):
- no project structure has been defined.

####SUPERSEDED FILES
- datagrabber:      Scrapes ASX sites for stock price data
- webservice:       Responsible for serving static pages and the JSON interface
- sqladaptor:       Manages SQL database transactions
- daemon.py:        Handles daemonising the process

###DEPENDENCIES
pip3: should be installed using pip3 install ...
- peewee (v 2.7.4)
- beautifulsoup4 (v4.4.1)
- selenium (v 2.48.0)
- requests 
- django (v 1.9.1)
- pymysql (v 0.6.7)

other:
- phantomjs

