
### --- v0.002a ---

* removed write-datapoint-to-csv logic and replaced with deque-based logic for passing info from datafeed to endpoint

* refactored constants.get_time (and renamed to constants.get_starttime_string) to not throw exception if START_TIME had not yet been set, as it defaults to unset and is set upon starting

* renamed data_feed functions since there were a lot of them named something close to "get_data_point, get_next_data_point, get_latest_data_point", etc, and it was confusing as to whether it was getting data from a datasource (api, blockchain, etc), creating a datapoint based on said data (this function was named get_datapoint()), or fetching (i.e. getting...) a stored-in-deque datapoint.

* converted all datetime references to unix timestamp (but we can always generate a datetime from a timestamp if needed, and are in fact now doing this in constants.get_time(), etc)

* fixed test datafeed overriding START_TIME and breaking 'status' command

* configured HTTP endpoint to return HTTP error / status code in event of error so that Chainlink can handle it

* fix siwa "quit" command (by overriding cmd2's method) to mark threads inactive; active threads are stuck in a while loop so siwa can't quit until they have been stopped.

* implemented custom logging handler to log to sqlite and removed old text file logging

* added /log route to endpoint to make recent logs accessible i.e. http://localhost:16556/logs

  * (note, we can extend the above to allow user or machine to specify a range as required)