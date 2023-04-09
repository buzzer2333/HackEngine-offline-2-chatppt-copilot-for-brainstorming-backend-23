import json
import uuid
from log import Log
from flask import request, jsonify, Blueprint, session, make_response
from service.mapping import MindMap, default
from service.detail import EntityInfos

map_blue = Blueprint("map", __name__)

# uuid -> mindMap
user2map = dict()
# uuid -> nodeInfos
user2info = dict()


def get_user_id() -> str:
    # 存储用户mindMap
    user_id = session.get('user_id')
    if user_id is None:
        user_id = uuid.uuid4()
        session['user_id'] = user_id
        Log.errorf("get user id failed, re-generate one as %s", user_id)
        return user_id
    Log.infof("get user id as %s", user_id)
    return user_id


@map_blue.route("/expand", methods=["POST"])
def expand():
    # todo :: biz
    params = request.get_data()
    params = json.loads(params)
    Log.infof("get input as %s", json.dumps(params))
    return jsonify(params)


@map_blue.route("/init", methods=["POST"])
def init():
    inputs = request.get_data()
    Log.infof("get inputs as %s", inputs)
    m = MindMap()
    m.ask_for_initial_graph(inputs)

    # 存储用户mindMap
    userid = get_user_id()
    user2map[userid] = m
    Log.infof("get user2Map as %s", user2map)
    rsp = make_response(json.dumps(m.root, default=default))
    rsp.headers["Content-Type"] = "application/json; charset=utf-8"
    return rsp


@map_blue.route("/detail", methods=["GET"])
def detail():
    node_id = request.args.get("id")
    node_label = request.args.get("label")
    query = request.args.get("query")
    Log.infof("get id as %s, label as %s", node_id, node_label)
    user_id = get_user_id()
    if user_id not in user2info:
        entity_info = EntityInfos()
        output = entity_info.ask_for_more_detail(query, node_id)
        user2info[user_id] = entity_info
    else:
        output = user2info[user_id].ask_for_more_detail(query, node_id)
    return jsonify({"data": output})
