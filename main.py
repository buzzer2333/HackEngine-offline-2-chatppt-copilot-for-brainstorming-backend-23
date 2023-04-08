from __future__ import annotations
import os
import openai

from service.detail import EntityInfos
from service.mapping import MindMap
from app import app

# todo:: open_api_key
openai.api_key = os.getenv("OPENAI_API_KEY")


def test_entity_info():
    entity = EntityInfos()
    entity.ask_for_more_detail("产品的商用化前景")


if __name__ == "__main__":
    # app.run()
    test_entity_info()


