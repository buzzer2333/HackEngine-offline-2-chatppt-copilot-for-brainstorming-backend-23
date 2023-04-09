from __future__ import annotations

import json
import os
import openai

import module.node as node
from service.detail import EntityInfos
from service.mapping import MindMap, default
from app import app
from log import Log
# todo:: open_api_key
openai.api_key = "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"
# openai.api_key = os.getenv("OPENAI_API_KEY")


def test_entity_info():
    entity = EntityInfos()
    output = entity.ask_for_more_detail("产品的商用化前景", "1")
    Log.infof("%s", output)


if __name__ == "__main__":
    n = node.NodeData(id="0", label="123")
    n.children.append(node.NodeData(id="0", label="123"))
    print(json.dumps(n, default=default))
    app.run()
    # test_entity_info()


