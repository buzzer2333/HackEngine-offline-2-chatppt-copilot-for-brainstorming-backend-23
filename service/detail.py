from typing import Optional, Tuple, List, Union, Literal
import openai
from dataclasses import dataclass, asdict
from module.message import Message
from module.conservation import DETAIL_CONVERSATION


def ask_chatgpt_detail(conversation: str) -> Tuple[str, str]:
    response = openai.Completion.create(
        model="text-davinci-003",
        # asdict comes from `from dataclasses import asdict`
        prompt=conversation,
        temperature=0.9,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    # turn into a Message object
    msg = response["choices"][0]["text"]
    # return the text output and the new conversation
    # print("msg:%s, conversation:%s", msg, conversation)

    return msg, conversation + msg


class EntityInfos:
    """A class that represents entity infos
    """

    def __init__(self, nodes: dict = None) -> None:
        self.conversation = ""
        self.nodesInfo = dict() if nodes is None else nodes

    def ask_for_more_detail(self, query: str, nodeID: str, new=False) -> str:
        """Ask GPT-3 to construct a graph from scrach.

        Args:
            query (str): The query to ask GPT-3 about.

        Returns:
            str: The output from GPT-3.
        """

        if new:
            conversation = DETAIL_CONVERSATION + f"""
                不错, 我会问你些具体问题:
                    
                Human: {query}
                AI:"""
        else:
            conversation = self.conversation + f"""
            
                Human: {query}
                AI:"""

        output, self.conversation = ask_chatgpt_detail(conversation)
        self.nodesInfo[nodeID] = output
        return output
