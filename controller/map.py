import json
from log import Log
from flask import request, jsonify, Blueprint, session, make_response
from service.mapping import MindMap, default

map_blue = Blueprint("map", __name__)


@map_blue.route("/expand", methods=["POST"])
def expand():
    params = request.get_data()
    params = json.loads(params)
    Log.infof("get input as %s", json.dumps(params))
    return jsonify(params)


@map_blue.route("/init", methods=["POST"])
def init():
    input = request.get_data()
    Log.infof("get input as %s", input)
    m = MindMap()
    # todo:: session里面只能放可以序列化的东西，所以很迷醉，不能直接把minMap放在session里面
    # session['map'] = m
    m.ask_for_initial_graph(input)
    rsp = make_response(json.dumps(m.root, default=default))
    rsp.headers["Content-Type"] = "application/json; charset=utf-8"
    return rsp

@map_blue.route("/detail", methods=["POST"])
def detail():
    string = request.get_data()
    Log.infof("get input as %s", string)



