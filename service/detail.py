from typing import Optional, Tuple, List, Union, Literal
import openai
from dataclasses import dataclass, asdict
from module.message import Message
from module.conservation import DETAIL_CONVERSATION


def ask_chatgpt_detail(conversation: List[Message]) -> Tuple[str, List[Message]]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # asdict comes from `from dataclasses import asdict`
        messages=[asdict(c) for c in conversation]
    )
    # turn into a Message object
    msg = Message(**response["choices"][0]["message"])
    # return the text output and the new conversation

    return msg.content, conversation + [msg]


class EntityInfos:
    """A class that represents entity infos
    """

    def __init__(self, nodes: dict = None) -> None:
        self.conversation = ""
        self.nodesInfo = dict() if nodes is None else nodes

    def ask_for_more_detail(self, query: str, nodeID: str) -> str:
        """Ask GPT-3 to construct a graph from scrach.

        Args:
            query (str): The query to ask GPT-3 about.

        Returns:
            str: The output from GPT-3.
        """

        conversation = DETAIL_CONVERSATION + [
            Message(f"""
                Great, 我会问你些具体问题:    
                {query}
            """, role="user")
        ]

        output, self.conversation = ask_chatgpt_detail(conversation)
        self.nodesInfo[nodeID] = output
        return output
