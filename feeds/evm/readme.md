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
You would need API keys for Pokt and/or Infura and/or Alchemy. 

For running the "unrealised OVL supply" feed, you would also need a subgraph API key.

Add the required keys to your environment variables:
```
export POKT_API_KEY=<your pokt api key>
export GRAPH_API_KEY=<your graph api key>
```


# Run
To run the feeds together:
```
python siwa.py --datafeeds unr_ovl_supply eth_burn_rate
```
Or run individually in separate terminals:
```
python siwa.py --datafeeds unr_ovl_supply
```
```
python siwa.py --datafeeds eth_burn_rate
```

