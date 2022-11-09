# Team-17
Team 17  Stock Market screener

## Setup
First of all, create a file named db.local.env in the root directory and fill it with database connection information and api keys shown below
```
DB_HOST=
DB_NAME=
DB_USER=
DB_PASS=
MGDB_HOST=
FMP_KEY=
APH_KEY=
```

System Requirements:
Python > 3.9.0

#### Windows
create a virtual environment inside market_screener folder: ```python -m venv venv```\
activate virtual environment: ```venv/Scripts/activate```\
deactivate virtual environment: ```deactivate```\
install packages: ```pip install -r requirements.txt```
run the application: ```python main.py```


#### Unix (Mac/Linux)
create a virtual environment inside market_screener folder: ```python3 -m venv venv```\
activate virtual environment: ```source venv/bin/activate```\
install packages: ```pip3 install -r requirements.txt```
run the application: ```python3 main.py```

## Core functionality
The main function of this application is the daily_update function found in the main.py file.

The function does the following:


*Technical*
- Load the database with updated stock data for the four major US indexes namely, NASDAQ, DOW, NYSE, S&P500.
- Computes the price moving averages (sma) and volume moving averages which are also loaded into the database.
- Computes the highs and lows of a 52 week period are also loaded into the database.
- Finally the relative strengths for each stock against it's index and each stock against the S&P500 index are loaded into the database.
- Use the price and computed technical data to prepare five datasets, one each for individual stock rankings against their index (using the relative_strength) and one for ranking all stocks against the S&P500 (using the relative_strength_sp500).
- The final datasets are then screened to return only stocks that have a rank greater than 0.7. The results are saved to a csv file.

*Fundamental*
- Using the final dataset from technical, loads the fundamental data of all stocks in the dataset into the database.
- Fetches data from professional finance API(Yahoo API / Alaph Vantage API / Financial Modeling Prep API).
- Gets updated results from database and save to a csv file.

### Usage
#### CLI
The application comes with a command line interface where commonly used functions can be triggered using commands and flags.

To get a list of commands available to you run 
```
python main.py --help
```

To get more details about a specific command, run the command below and replace "COMMAND" with the command you are interested in
Running this provides details of what the command does, the parameters required and examples of how to run them.
```
python main.py COMMAND --help
```

The available commands are:\
__update_all__: To update all stocks in the database, create a daily dataset for each index and a dataset for all stocks in the database against the S&P500\
__update__: Update prices of stocks in a specified index and calculate relative strengths for a specified date range\
__get_dataset__: Get a dataset for one index on a specified date\
__get_dataset_sp500__: Get the dataset of all stocks against the S&P500 for a specified date\
__screen_dataset__: Runs a query on a specified dataset to return stocks meeting provided screening conditions\
__screen_dataset_sp500__: Runs a query on a specified dataset of all stocks against the S&P500 to return stocks meeting provided screening conditions\
__status__: Shows details of the state of the database



## Modules

### Data Pipeline
The data_pipeline.py module is used to process data from external apis or from a database and then store results back in to the database. Functionality like updating all stock prices, moving averages and relative strengths can be found in the data pipeline. The daily update strategy of the screener also lives in this module.


```python

update_stocks():
"""
This is the daily update function.
It loops through all indexes and for each stock in each index, it does the following:
- Loads any missing prices from their price table till the most recently closed date.
- Calculates and loads all moving averages for price and volumes.
- Identifies the highs and lows for the added periods and updates them in the table.
- Finally, it computes the relative strength against the stocks index and adds that to the table.
"""


load_stock_prices(symbol, index, start_date):
"""
This fetches price data for the specified symbol from the provided start date to the most recently closed day.
"""


update_all_relative_strength(start_date, end_date):
"""
Calculates and uploads the relative strength for every stock in the database against the S&P500
"""


update_reference_relative_strength(ref_index, stocks_index, start_date, end_date):
"""
Calculates and uploads the relative strength for every stock in the database against the S&P500
Similar to the update_all_relative_strength function but this allows you choose which index to update rather than all or them.
"""


update_own_relative_strength(index, start_date, end_date):
"""
Calculates and uploads the relative strength for each stock based on it's own index
"""


load_stock_sma_volume(symbol, start):
"""
Computes and loads SMAs and Volume Averages into database tables
"""


load_stock_highs_lows(symbol, start):
"""
Loads 52 week highs and lows
"""


load_stock_relative_strength(symbol, index_cum_prod, stock_cum_prod, column = 'relative_strength'):
"""
This takes the cumulative products of a stock and an index and returns the relative strengths for dates where
both the stock and the index have a valid weighted cumulative product.
"""
```

### Technical Analysis
The technical_analysis.py module contains functions that take historical prices or other derived values as input, 
run computations and return technical indicators.

```python
calc_price_average(prices: pd.DataFrame, windows = [50]):
"""
Calculates the price moving average of a series of dates

Parameters
----------
prices : A dataframe containing at least two columns, a date column and a close (close price) column

window : A list of numbers to be used as the number of datapoints required for each average,
defaults to a list with the number 50 as it's only element
"""


calc_volume_average(prices: pd.DataFrame, windows = [50]):
"""
Calculates the volume moving average of a series of dates

Parameters
----------
prices : A dataframe containing at least two columns, a date column and a volume column

window : A list of numbers to be used as the number of datapoints required for each average,
defaults to a list with the number 50 as it's only element
"""


calc_sma_volume(historical_prices):
"""
Calculate price moving averages and volume averages.
Return values as a tuple containing tuples which each representing a row in the database

Parameters
----------
historical_prices : Must be a 2D tupple or list containing date, close and volume in each nested array
"""


get_high_low(historical_prices):
"""
Iterate over prices and record the highest and lowest price within a 52 week period approximated as 240 days

Parameters
----------
historical_prices : Must be a 2D tupple or list containing date and close in each nested array
"""


get_dates(end_date, count):
"""
Takes a target date as parameter and gets 4 evenly distributed earlier dates.
In the case of a year, the 4 dates would be approximately 3 months of working days.
For smaller periods, the dates will be evenly split into 4 quarters

Parameters
----------
end_date : Date from which to find the start 4 previous quarters
count : maximum number of business days available to get dates from
"""


get_weighted_comp(historical_prices, start_date, min_days = 8):
"""
Calculate the cummulative product for a given symbol and a date from which the cummulative product is required.
This calculation is weighed 40% for most recent quarter and 20% for the remaining three quarters
"""


get_relative_strength(index_cum_prod, stock_cum_prod: pd.DataFrame):
"""
Takes the cummulative products of an index over a period and the cummulative products of a stock over a period
Joins the cummulative periods based on dates that match and divides the stock values by index values.
The result is converted to a list of tuples each containing date and relative strength for each date
"""
```

### Fundamental Analysis
The fundamental part mainly consists of five-part of codes, three files to fetch fundamental data from each finance API, and one file storing all the fundamental data to the MongoDB database, the rest of one file is generating one CSV file containing all the fundamental data from MongoDB database.

```python
File name: alphav.py
get_eps_info(symbol)
"""
Calculates the data related EPS and the stock price changes during a range of days based on the data fetched from Alphavantage API.
Parameters
----------
symbol : a single stock symbol name. 
"""

get_income_info(symbol)
"""
Calculates the data related stock income(Such as revenue / profit)changes based on the data fetched from Alphavantage API.
Parameters
----------
symbol : a single stock symbol name. 


"""


File name: fmp.py

get_jsonparsed_data(url):
"""
Return the data into a json format based on the data from Financialmodelingprep API.
Parameters
----------
url : specifically url assigned from the Financialmodelingprep API.
"""

def get_ratios_info(symbol):
"""
Return all the  stock ratio data from Financialmodelingprep API.
Parameters
----------
symbol : a single stock symbol name. 
"""


def get_profile_info(symbol):
"""
Return all the  stock basic stock Information from Financialmodelingprep API.
Parameters
----------
symbol : a single stock symbol name. 
"""
Return all the  stock ratio data from Financialmodelingprep API.

Parameters
----------
symbol : a single stock symbol name. 
"""

def get_score(symbol):
"""
Return all the  stock altmanZScore/piotroskiScore from Financialmodelingprep API.
Parameters
----------
symbol : a single stock symbol name. 
"""

get_cashFlowvalue(symbol):
"""
Return all the   stock dcf value /stock price from Financialmodelingprep API.
Parameters
----------
symbol : a single stock symbol name. 
"""


File name: yahoo.py

get_inst_info(symbol):
"""
Return all the  stock institutional holders data from Yahoo finance API.
Parameters
----------
symbol : a single stock symbol name. 
"""

get_major_holders(symbol):
"""
Return all the  stock major holders data from Yahoo finance API.
Parameters
----------

symbol : a single stock symbol name. 
"""


get_volume_change(symbol):
"""
Return all the  stock volume change(10-100days) data from Yahoo finance API.
Parameters
----------
symbol : a single stock symbol name. 
"""

File name: print_data.py
def print_newReq(symbol, dbname, colname):
"""
Return all the  stock Information into a list. And this list will be the input data of function of get_fundamental().
Parameters
----------
dbname:name of the MongoDB database sub-name.
colname:name of the MongoDB database colname.
symbol: a single stock symbol name.
"""

def get_screened_symbols():
"""
Read all the stock symbols in the txt file.
----------


get_fundamental():
"""
Create a CSV file for UI to present all the stock data. The source is from the function of def print_newReq(symbol, dbname, colname), and the CSV file will be saved in an assigned directory with other symbol lists for UI resources.
----------
"""

Class name: mongo.py

def __init__(self):
"""
This function is to setting up the MongoDB database for the fundamental data.

Parameters:
self: a MongoDB object.
----------
"""


def create_symbol_dbinfo(self,symbol):
"""
Create a dictionary contains all fundamental data collected by various APIs. This dictionary will be saved as a document for this stock symbol in MongoDB

Parameters:
self: this MongoDB object.
symbol: a single stock symbol name.
----------
"""

def insert_symbol(self,dbname, colname, fdDict):
"""
Import a document of a symbol into specific location of MongoDB.

Parameters:
self: this MongoDB object.
dbname: specify a database name in MongoDB.
colname: specify a collection name in the above database in MongoDB.
fdDict: the dictionary created by create_symbol_dbinfo(self,symbol).
----------
"""

def insert_multiple_symbols(self,dbname, colname, symbols):
"""
Parameters:
Import documents of a symbol list into specific location of MongoDB. The creating of documents will call create_symbol_dbinfo(self,symbol) above.

self: this MongoDB object.
dbname: specify a database name in MongoDB.
colname: specify a collection name in the above database in MongoDB.
symbols: a list of symbols that need to have fundamental data stored in MongoDB.
----------
"""

def insert_multiple_symbols(self,dbname, colname, symbols):
"""
Import documents of a symbol list into specific location of MongoDB. The creating of documents will call create_symbol_dbinfo(self,symbol) above. There is a sleep time set between the each creation of documents to avoid API limitaion.

Parameters:
self: this MongoDB object.
dbname: specify a database name in MongoDB.
colname: specify a collection name in the above database in MongoDB.
symbols: a list of symbols that need to have fundamental data stored in MongoDB.
----------
"""

def daily_update(self,dbname, colname, symbols):
"""
To make sure we have the up-to-date fundamental data for all symbols the new symbol list in MongoDB. If there are symbols in the new list but not in our database. It will
create documents for them and import to MongoDB.
The creating of documents will call insert_multiple_symbols(self,dbname, colname, symbols) above.

Parameters:
self: this MongoDB object.
dbname: specify a database name in MongoDB.
colname: specify a collection name in the above database in MongoDB.
symbols: a list of daily dataset that need to have fundamental data stored in MongoDB.
----------
"""

def get_symbol_dbinfo(self, symbol, dbname, colname):
"""
To get the fundamental data of one single stock for creating the CSV file.

Parameters:
self: this MongoDB object.
symbols: a single stock symbol that already have fundamental data stored in MongoDB.
dbname: specify a database name in MongoDB.
colname: specify a collection name in the above database in MongoDB.
----------
"""


```
