import os
import logging
import openai
from flask import Flask, request, jsonify, session
from controller.map import map_blue

# 初始化flask app
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.register_blueprint(blueprint=map_blue)



# return index.html
@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("map") is None:
        pass
        # todo:: session model
        # session["map"] =
    return app.send_static_file("mind_map_test.html")

