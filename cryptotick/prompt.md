CryptoTick offers a "pay as you go" service, where customers pay for the exact usage of the service rather than a subscription. Customers can pre-purchase a certain amount of units and can use the service until their balance runs out, after which they can top up again. CryptoTick does not have an application programming interface (API), which allows applications to integrate with each other. Instead, customers can go directly to the site to get the requested information; they just need to specify what they require, and the data will then be provided to them. Therefore, CryptoTick is an ideal solution for customers needing historical data, as it is a user interface and not an application.
History data from all cryptocurrency exchanges in single place.
CryptoTick is a place where you can easily download highest quality history market data from cryptocurrency markets
Backtesting ready
We are additionally timestamping data using the same synchronized clock for all exchanges when we first receive it, which gives the possibility of significantly more accurate backtesting of algorithmic trading strategies.
Redundancy
Our geographically dispersed infrastructure eliminates data errors and increasing amount of the updates we archive. Data collected from multiple locations is consolidated into the single stream available to download on our site.
Survivorship bias-free
In early developing markets, avoiding survivorship bias is essential. To prevent the issue, you can download data from closed exchanges or delisted symbols in our platform.
Processed data
In addition to the raw exchange data, we are providing various types of processed data like OHLCV time series created from active market data (transactions).
selected exchanges: surbitcoin poloniex chbtc chilebit.net jubi.com bitstamp btcchina.com virwox bter.com btctrade.com kcoin quadrigacx gatecoin gdax huobi bitfinex bitmarket deribit kraken btcx

General
What time zone is used in the data?

All timestamps are always in the UTC (Universal Coordinated Time).
What is the minimum size of the first and next orders?

Currently we do not require minimum order size.
Flat files
How the data is stored inside a flat file?

Compressed (gzip highest available compression level) ASCII text files (CSV format).
How to authorize CryptoTick to the Amazon S3 bucket for the upload delivery option?

Please disable the ACL in the object ownership section and attach this bucket policy.
How to authorize CryptoTick to the Google GCP bucket for the upload delivery option?

You need to add our Service Account flat-files@coinapi.iam.gserviceaccount.com in the bucket with Storage Admin access.
What are the configuration parameters for the CSV format?

; - is used as columns delimiter
\r\n (CR + LF) - is used as a new line marker
. (dot) - is used as the decimal mark
UTC - Timezone used for all time values
yyyy-MM-ddTHH:mm:ss.fffffff - is used as a date time format
yyyy-MM-dd - is used as a date format
HH:mm:ss.fffffff - is used as a time format
Can you provide description of the data types?

Data type	Description
quotes	Quote represent top of the book and contain best bid and ask prices with cumulative size of resting orders. This type is double timestamped by the exchange (if available) and at the moment of the first receive before any processing and marked by the server site identifier which received this data point.
trades	Trade represents a match between passive and active market participants. Each trade contains id, price, size, and aggressor of the trade (if available). This type is double timestamped by the exchange (if available) and at the moment of the first receive before any processing.
limitbook_snapshot_X	Snapshot of the limit book represents X best levels from each side of the book. Each level contains the price and cumulative size of resting orders on this level. Snapshot recorded every second ('interval') if the order book changed in at least one level in the first X best levels at the end of the interval period. This type is double timestamped by the exchange (if available) and at the moment of the first receive before any processing.
limitbook_full	The limitbook_full represents every update in the order book delivered by the data source (in the L2 or L3 granularity); the file starts with a snapshot of the order book followed by updates to the state. Every data point in this format represents a level in the order book and using this type you can see the order book as deep as data source provides. This type is double timestamped by the exchange (if available) and at the moment of the first receive before any processing.
ohlcv_active_consolidated	The ohlcv_active_consolidated represents OHLCV data (aggregated transactions). Each data point represents OHLCV for the specific symbol on the selected aggregation period between 1 Second and 1 Month if, in the period, there is at least one transaction.
How is the data split into the files?

Data type	File split methodology
quotes	Single file per symbol & trading day (UTC).
trades	Single file per symbol & trading day (UTC).
limitbook_snapshot_X	Single file per symbol & trading day (UTC).
limitbook_full	Single file per symbol & trading day (UTC).
ohlcv_active_consolidated	Single file per time series period & trading day (UTC). The file contains data across all the symbols tracked in our system or all symbols from the specific exchange.
From where I can download the samples of the flat files?

Data type	Samples
quotes	https://s3.amazonaws.com/coinapi-samples/quotes/20181010/29168-BITMEX_PERP_BTC_USD.csv.gz
trades	https://s3.amazonaws.com/coinapi-samples/trades/20180926/562-BITSTAMP_SPOT_BTC_USD.csv.gz
limitbook_snapshot_50	https://s3.amazonaws.com/coinapi-samples/limitbook_snapshot_50/20170601/98003-COINBASE_SPOT_ETH_EUR.csv.gz
limitbook_full	https://s3.amazonaws.com/coinapi-samples/limitbook_full/20171229/27606-BITSTAMP_SPOT_BTC_EUR.csv.gz
ohlcv_active_consolidated	https://s3.amazonaws.com/coinapi-samples/ohlcv_active_consolidated/20171203/1HRS.csv.gz
Can you provide documentation for the values in the CSV file?

Data type	Column name	Description
quotes	id_site_coinapi	UUID of the site which received the quote. This useful information can be used to replay markets from the perspective of the algorithmic trading strategy.
time_exchange	UTC timestamp of the trade provided by the exchange or estimation of it using the delay of the exchange API (if the time_exchange is equal to the time_coinapi, then it mean that the time_exchange is not available)
time_coinapi	UTC timestamp of the trade when we first received it from the exchange in the specific site identified by the id_site_coinapi column. This useful information can be used to replay markets from the perspective of the algorithmic trading strategy. (Our clock is synchronized across data types and exchanges)
ask_px	Best ask price
ask_sx	Total amount of volume resting on best ask level in the base asset of the symbol
bid_px	Best bid price
bid_sx	Total amount of volume resting on best bid level in the base asset of the symbol
trades	time_exchange	UTC timestamp of the trade provided by the exchange or estimation of it using the delay of the exchange API (if the time_exchange is equal to the time_coinapi, then it mean that the time_exchange is not available)
time_coinapi	UTC timestamp of the trade when we first received it from the exchange. This useful information can be used to replay markets from the perspective of the algorithmic trading strategy. (Our clock is synchronized across data types and exchanges)
guid	Unique identifier of the trade provided by the CoinAPI
price	Price of the transaction
base_amount	Amount of base asset traded in the transaction.
taker_side	Aggressor side of the transaction.
Possible values are:
BUY - Exchange has reported that transaction aggressor was buying
SELL - Exchange has reported that transaction aggressor was selling
BUY_ESTIMATED - Exchange has not reported transaction aggressor, we estimated that more likely it was buying
SELL_ESTIMATED - Exchange has not reported transaction aggressor, we estimated that more likely it was selling
UNKNOWN - Exchange has not reported transaction aggressor and we have not estimated who it was
limitbook_snapshot_X	time_exchange	UTC timestamp of the book provided by the exchange or estimation of it using the delay of the exchange API (if the time_exchange is equal to the time_coinapi, then it mean that the time_exchange is not available)
time_coinapi	UTC timestamp of the book when we first received it from the exchange. This useful information can be used to replay markets from the perspective of the algorithmic trading strategy. (Our clock is synchronized across data types and exchanges)
asks[0-X].price	Asks prices (incrementing from the spread)
asks[0-X].size	Total amount of volume resting on ask levels in the base asset of the symbol
bids[0-X].price	Bid prices (decrementing from the spread)
bids[0-X].size	Total amount of volume resting on bid levels in the base asset of the symbol
limitbook_full	time_exchange	UTC timestamp of the update provided by the exchange or estimation of it using the delay of the exchange API (if the time_exchange is equal to the time_coinapi, then it mean that the time_exchange is not available)
time_coinapi	UTC timestamp of the update when we first received it from the exchange. This useful information can be used to replay markets from the perspective of the algorithmic trading strategy. (Our clock is synchronized across data types and exchanges)
is_buy	Is the update related to the bid side of the book? Possible values are 0 (it's ask - sell) or 1 (it's bid - buy).
update_type	Type of the update.
Possible values are:
ADD - Add the order to the book with key (entry_px, order_id).
SUB - Subtract the resting entry_sx volume from the book order identified by the key (entry_px, order_id).
MATCH - Process the same as SUB, used to identify that subtraction was caused by the execution and not modification or self trade prevention algorithms.
SET - Set the new entry_sx volume on the book order identified by the key (entry_px, order_id).
DELETE - Delete the order identified by the key (entry_px, order_id) from the book.
SNAPSHOT - Process the same as ADD, but before processing the first SNAPSHOT line when the last line seen was not a SNAPSHOT, then the whole book must be discarded/cleared.
entry_px	Price identifying the book level.
entry_sx	Volume associated with the specific update item.
order_id	ID of the order if the format is Level 3 (order-by-order), empty if the format is Level 2
ohlcv_active_consolidated	symbol_id	Symbol identifier of requested time series. More information about the symbol are provided by the CoinAPI REST API at the https://docs.coinapi.io/#list-all-symbols
time_period_start	Period starting UTC time (range left inclusive)
time_period_end	Period ending UTC time (range right exclusive)
time_open	UTC Time of first trade inside a period range
time_close	UTC Time of last trade inside a period range
px_open	First trade price inside a period range
px_high	Highest traded price inside a period range
px_low	Lowest traded price inside a period range
px_close	Last trade price inside a period range
sx_sum	Cumulative base amount traded inside a period range
sx_cnt	Amount of trades executed inside a period range