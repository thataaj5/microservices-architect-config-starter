from flask import Flask,request
from flask_cors import CORS 
import json
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

app = Flask(__name__)
CORS(app)

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))


@app.route('/', methods = ['GET'])
def hello():
   start = time.time()
   graphs['c'].inc()
   end = time.time()
   graphs['h'].observe(end - start)
   print('Getting List of WishList Items')
   x = {
    "1": "Apple Iphone",
    "2": "MacBook",
    "3": "Your Fav Something else"
   }
   y = json.dumps(x)
   return y


@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")



@app.route('/likes', methods = ['GET'])
def likes():
   print('Getting List of WishList Items')
   return 'List of WishList Items'


@app.route('/product/<product>', methods = ['GET', 'POST'])
def product(product):
   if request.method == 'POST':
      print(product)
      return product
   return 'Call from POST'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    print('Wishlist Microservice Started...')
