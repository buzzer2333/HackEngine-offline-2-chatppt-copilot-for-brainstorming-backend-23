import json
from log import Log
from flask import request, jsonify, Blueprint, session, make_response
from service.mapping import MindMap, default

map_blue = Blueprint("map", __name__)

# uuid -> mindMap
user2map = dict()

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
    m.ask_for_initial_graph(input)

    # 存储用户mindMap
    uuid = session['user_id']
    if uuid is None:
        Log.errorf("get user id failed")
        return jsonify({"err":"get user info failed"})
    Log.infof("get user id as %s", uuid)
    user2map[uuid] = m
    Log.infof("get user2Map as %s", user2map)
    rsp = make_response(json.dumps(m.root, default=default))
    rsp.headers["Content-Type"] = "application/json; charset=utf-8"
    return rsp

@map_blue.route("/detail", methods=["POST"])
def detail():
    string = request.get_data()
    Log.infof("get input as %s", string)



