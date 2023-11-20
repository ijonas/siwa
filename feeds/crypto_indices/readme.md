# Setup
You may want to set up a virtual environment for this project.
```
virtualenv venv -p python3
```
Note: It's possible that you may face issues with python versions > 3.9. In that case,
```
virtualenv venv -p python3.9
```

Then activate it:
```
source venv/bin/activate
```
Then install the requirements:
```
pip install -r requirements.txt
```
For Bitcoin Dominance, you will need the coinmarketcap API key and Pokt and/or Infura and/or Alchemy API keys.

Add the required keys to your environment variables:
```
export POKT_API_KEY=<your pokt api key>
export COINMARKETCAP_API_KEY=<your coinmarketcap api key>
```

For Memecoins and Mcap1000, you only need the coinmarketcap API key.

# Run
To run the feeds together:
```
python siwa.py --datafeeds mcap1000 memecoins btc_dominance
```
Or run individually in separate terminals:
```
python siwa.py --datafeeds btc_dominance
```