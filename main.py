from __future__ import annotations
import os
import openai

from service.detail import EntityInfos
from service.mapping import MindMap
from app import app
from log import Log

openai.api_key = os.getenv("OPENAI_API_KEY")


def test_entity_info():
    entity = EntityInfos()
    output = entity.ask_for_more_detail("产品的商用化前景", "1")
    Log.infof("%s", output)


if __name__ == "__main__":
     app.run(debug=True, port=os.getenv("PORT", default=5001), host='0.0.0.0')
    # test_entity_info()


