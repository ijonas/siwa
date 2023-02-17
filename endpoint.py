from waitress import serve
from flask import Flask, jsonify
from all_feeds import all_feeds
import constants as c

app = Flask(__name__)

@app.route("/")
def blank():
    return 'this is a siwa endpoint'

@app.route("/datafeed/<feedname>")
def json_route(feedname):
    if feedname in all_feeds.keys():
        feed = all_feeds[feedname](feedname, 1, 1, 1)
        data_point = feed.get_most_recently_stored_data_point()
        print('datapoint: ', data_point)
        if not data_point:
            data_point = {'error':'new feed / no data yet'}
    else:
        data_point = {'error':'unknown feed name'}

    return jsonify(data_point)

def run():
    serve(app,host='0.0.0.0', port=16556)

if __name__ == "__main__":
    if c.DEBUG:
        # for local debugging only:
        # note, the below cant be used if calling from siwa CLI in a thread
        # as flask assumes it will have the main thread in debug mode
        app.run(host='0.0.0.0', port=16556, debug=True)
    else:
        run()
