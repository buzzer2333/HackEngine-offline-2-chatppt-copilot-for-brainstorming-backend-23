from typing import Optional, Tuple, List, Union, Literal
import openai
from dataclasses import dataclass, asdict
import streamlit as st
from textwrap import dedent

@dataclass
class Message:
    """A class that represents a message in a ChatGPT conversation.
    """
    content: str
    role: Literal["user", "system", "assistant"]

    # is a built-in method for dataclasses
    # called after the __init__ method
    def __post_init__(self):
        self.content = dedent(self.content).strip()


DETAIL_CONVERSATION = [
    Message("""
        你是一个行业专家你可以回答行业专业问题
    """, role="system"),
    Message("""
        如果我要做空气净化功能，我的目标用户群体可以是谁
    """, role="user"),
    Message("""
    空气净化功能可以吸引多种用户群体，例如：
对空气质量有高要求的人群：例如患有哮喘或过敏症的人，他们需要在车内呼吸到干净的空气以避免过敏反应。
车辆长时间停放在封闭环境内的用户：例如停在车库或地下停车场的车辆，车内空气可能会污染，使用空气净化功能可以有效净化空气，使车内环境更加健康。
家庭有婴幼儿的用户：对于这些用户来说，车内空气质量对婴幼儿健康至关重要，使用空气净化功能可以保证车内空气的质量。
职业司机：长时间驾驶车辆的司机需要呼吸干净的空气，以避免疲劳和健康问题。
对环保有意识的人群：这些用户关心环境保护和减少对环境的污染，使用空气净化功能可以减少车辆对环境的影响。
总之，使用空气净化功能可以让车内空气更加清新健康，吸引多种用户群体的关注。""", role="assistant")
]

def ask_chatgpt_detail(conversation: List[Message]) -> Tuple[str, List[Message]]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # asdict comes from `from dataclasses import asdict`
        messages=[asdict(c) for c in conversation]
    )

    print("response:", response)
    # turn into a Message object
    msg = Message(**response["choices"][0]["message"])
    # return the text output and the new conversation
    print("msg:%s, conversation:%s", msg,  conversation)
    
    return msg.content, conversation + [msg]

class EntityInfos:
    """A class that represents entity infos
    """

    def __init__(self, **nodes) -> None:
        self.nodesInfo = [] if nodes is None else nodes
        self.save()

    @classmethod
    def load(cls):
        """Load EntityInfo from session state if it exists
        
        Returns: entityInfos
        """
        if "entityInfos" in st.session_state:
            return st.session_state["entityInfos"]
        return cls()

    def save(self) -> None:
        # save to session state
        st.session_state["entityInfos"] = self

    def ask_for_more_detail(self, query: str) -> None:
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
        # replace=True to restart
