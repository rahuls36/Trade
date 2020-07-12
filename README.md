# Steps for the getting the Django App Up and Running
1. Install Docker on local.
2. run docker-compose build
3. run docker-compose up

# Endpoints Available
1. GET /Trades/currency/{symbol}/ - For Getting the Trade Data according to the symbol provided
2. GET /Trades/currency/all/ - For Getting the Trade Data for all the preconfigured Symbols.
3. POST /Trades/currency/symbol/ - For Adding new Symbol Data on Local Db

