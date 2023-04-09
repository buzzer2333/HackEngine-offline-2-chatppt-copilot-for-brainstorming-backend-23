import uuid
import logging

from flask import Flask, request, jsonify, session
from controller.map import map_blue
from log import Log

# 初始化flask app
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.secret_key = "hackthon-20230408"
app.register_blueprint(blueprint=map_blue)


# return index.html
@app.route("/666", methods=["GET", "POST"])
def index():
    if session.get("user_id") is None:
        # 这里是假设用户只会从/路由进入应用
        # 生成随机数标识用户
        user_id = uuid.uuid4().hex
        print(user_id)
        Log.infof("get user_id as %s", user_id)
        session["user_id"] = user_id
        # todo:: session model
        # session["map"] =
    user_id = session["user_id"]
    Log.infof("already has user_id as %s", user_id)
    return app.send_static_file("mind_map_test.html")
