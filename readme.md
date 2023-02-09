## Siwa Oracle 
*prototype 1 // January 25, 2023*

## OVERVIEW:
    This code base provides a CLI for running and interacting various data production algorithms which are then collected by another service and saved to the blockchain. 

## Setup:
    You should run `pip install -r requirements.txt`

    Each feed may itself require separate setup. 
    See the /feeds directory and the readme.md files therein

## Files:
* `siwa.py` - provides CLI interface / thread handling
* `endpoint.py` http/json endpoint, run automatically via siwa CLI, or standalone
* `all_feeds.py` - all enabled datafeeds from `feeds/`
* `feeds/data_feed.py` - defines class structure shared by all datafeeds
* `feeds/*.py` - e.g. `gauss.py` - defines an individual datafeed

## Examples:
    endpoint example: http://127.0.0.1:16556/datafeed/gauss
    (you may need to pre-populate by running gauss for a second)

## Notes:
    The JSON endpoint has a debugging mode, which can among other things display errors via HTTP.
    To run in debug mode, endpoint must be run standalone.
    To do that, you would have to disable it from autostarting in its own thread in siwa.py, and then run `python endpoint.py`

    `status` from CLI now shows thread counts for datafeeds (as well as other threads, i.e. main thread, endpoint thread(s))

    the debug endpoint would uses 1 thread
    the non-debug endpoint uses 5 



## TODOs:
* [done] add http endpoint to expose newest datapoint per feed in JSON format
* [done] disallow starting more than 1 thread per datafeed via CLI
