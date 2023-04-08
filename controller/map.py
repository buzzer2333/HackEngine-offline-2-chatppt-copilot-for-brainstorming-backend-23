import json
from log import Log
from flask import request, jsonify, Blueprint

map_blue = Blueprint("map", __name__)


@map_blue.route("/expand", methods=["POST"])
def expand():
    params = request.get_data()
    params = json.loads(params)
    Log.infof("get input as %s", json.dumps(params))
    return jsonify(params)
