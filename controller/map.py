import json
import uuid
from log import Log
from flask import request, jsonify, Blueprint, session, make_response
from service.mapping import MindMap, default
from service.detail import EntityInfos
from service.mapping2 import MindMap2

map_blue = Blueprint("map", __name__)

# uuid -> mindMap
user2map = dict()
# uuid -> nodeInfos
user2info = dict()


# 获取user_id
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


# 扩展头脑风暴图的某个节点
@map_blue.route("/expand", methods=["POST", "OPTIONS"])
def expand():
    if request.method == "OPTIONS":
        rsp = make_response()
        add_header(rsp)
        return rsp

    selected_node = request.json.get("selected_node")
    text = request.json.get("text")
    manual = bool(request.json.get("manual"))

    userid = get_user_id()
    if userid not in user2map:
        user2map[userid] = MindMap()

    m = user2map[userid]
    m.ask_for_extended_graph(selected_node=selected_node, text=text, manual=manual)
    Log.infof("get user2Map as %s", user2map)

    rsp = make_response(json.dumps(m.root, default=default))
    add_header(rsp)
    return rsp


def add_header(rsp):
    rsp.headers["Content-Type"] = "application/json; charset=utf-8"
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    rsp.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    rsp.headers["Access-Control-Allow-Headers"] = "X-PINGOTHER, Content-Type, withCredentials"
    rsp.headers["Access-Control-Max-Age"] = 86400
    rsp.headers["Vary"] = "Accept-Encoding, Origin"


# 扩展头脑风暴图的某个节点
@map_blue.route("/v2/expand", methods=["POST", "OPTIONS"])
def expand_v2():
    if request.method == "OPTIONS":
        rsp = make_response()
        add_header(rsp)
        return rsp

    selected_node = request.json.get("selected_node")
    text = request.json.get("text")
    manual = bool(request.json.get("manual"))

    userid = get_user_id()
    if userid not in user2map:
        user2map[userid] = MindMap2()

    m = user2map[userid]
    re = m.ask_for_extended_graph(selected_node=selected_node, text=text, manual=manual)
    Log.infof("get user2Map as %s", user2map)

    rsp = make_response(json.dumps(re))
    add_header(rsp)
    return rsp


# 初始化头脑风暴图
@map_blue.route("/init", methods=["POST", "OPTIONS"])
def init():
    if request.method == "OPTIONS":
        rsp = make_response()
        add_header(rsp)
        return rsp

    query = request.json.get("query")
    Log.infof("get query as %s", query)

    # 存储用户mindMap
    userid = get_user_id()
    if userid not in user2map:
        user2map[userid] = MindMap()

    m = user2map[userid]
    m.ask_for_initial_graph(query)
    Log.infof("get user2Map as %s", user2map)

    rsp = make_response(json.dumps({"data": m.root, "code": 0}, default=default))
    add_header(rsp)
    return rsp


# 初始化头脑风暴图2
@map_blue.route("/v2/init", methods=["POST", "OPTIONS"])
def init_v2():
    if request.method == "OPTIONS":
        rsp = make_response()
        add_header(rsp)
        return rsp

    query = request.json.get("query")
    Log.infof("get query as %s", query)

    userid = get_user_id()
    if userid not in user2map:
        user2map[userid] = MindMap2()

    m = user2map[userid]
    re = m.ask_for_initial_graph(query)
    Log.infof("get user2Map as %s", user2map)

    rsp = make_response(json.dumps(re))
    add_header(rsp)
    return rsp


# 获取某个节点的相关信息
@map_blue.route("/detail", methods=["GET", "OPTIONS", "POST"])
def detail():
    if request.method == "OPTIONS":
        rsp = make_response()
        add_header(rsp)
        return rsp
    node_id = request.json.get("id")
    node_label = request.json.get("label")
    query = request.json.get("query")
    if request.method == "GET":
        node_id = request.args.get("id")
        node_label = request.args.get("label")
        query = request.args.get("query")
    Log.infof("get id as %s, label as %s, query as %s", node_id, node_label, query)

    user_id = get_user_id()
    if user_id not in user2info:
        entity_info = EntityInfos()
        output = entity_info.ask_for_more_detail(query, node_id, new=True)
        user2info[user_id] = entity_info
    else:
        output = user2info[user_id].ask_for_more_detail(query, node_id, new=False)

    rsp = make_response(jsonify({"data": output, "code": 0}))
    add_header(rsp)
    return rsp
