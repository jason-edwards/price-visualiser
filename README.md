#Price Visualiser

This software aims to collect stock market data and global news data. It will analyse the data and display it in various graphical representations. The idea is to create a simple to use, readable representations of stock market & global event correlations.

####FILES
Python:
- datagrabber:		Scrapes ASX sites for stock price data
- webservice: 		Responsible for serving static pages and the JSON interface
- sqladaptor:		  Manages SQL database transactions
- daemon.py:		  Handles daemonising the process

####DEPENDENCIES
pip: can be installed using pip install ...
- peewee
- beautifulsoup4
- selenium
- requests
- flask
- pymysql

other:
- phantomjs

