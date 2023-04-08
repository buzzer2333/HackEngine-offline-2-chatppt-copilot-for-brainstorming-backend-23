import json
from log import Log
from flask import request, jsonify, Blueprint, session
from service.mapping import MindMap

map_blue = Blueprint("map", __name__)


@map_blue.route("/expand", methods=["POST"])
def expand():
    params = request.get_data()
    params = json.loads(params)
    Log.infof("get input as %s", json.dumps(params))
    return jsonify(params)


@map_blue.route("/init", methods=["POST"])
def init():
    str = request.get_data()
    Log.infof("get input as %s", str)
    m = MindMap()
    session['map'] = m
    m.ask_for_initial_graph(str)
    Log.infof("get root as %s", m.root.label)
    Log.infof("get rsp as %s", [x.label for x in m.root])
    jsonify(m.root)

@map_blue.route("/detail", methods=["POST"])
def detail():
    string = request.get_data()
    Log.infof("get input as %s", string)



