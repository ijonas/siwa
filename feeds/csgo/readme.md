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
You would also need the following environment variables:
```
export INFURA_API_KEY=<your infura api key>
export CSGO_API_KEY=<your csgo api key>
```
The CSGO API key can be obtained from [csgoskins.gg](https://csgoskins.gg/).


# Run
To run the csgo index feed, you can run the following command:
```
python siwa.py --datafeeds csgo_index
```
The index will appear as a `data_point` here:
```
http://127.0.0.1:16556/datafeed/csgo_index
```


# Run using docker compose
To run the csgo index feed using docker-compose, run the following commands
```
docker-compose build siwa
docker-compose up siwa
```

The index will appear as a data point hereL
```
http://127.0.0.1:81/datafeed/csgo_index
```
