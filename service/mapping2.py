from __future__ import annotations
import re
from typing import Optional, Tuple, List, Union, Literal
import base64
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import os
import openai
import graphviz
from dataclasses import dataclass, asdict
from textwrap import dedent
from streamlit_agraph import agraph, Node, Edge, Config

from log import Log
from module.message import Message
from module.conservation import START_CONVERSATION, START_CONVERSATION2
from module.node import NodeData


def ask_chatgpt(conversation: str) -> Tuple[str, str]:
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

    # print("response:", response)
    # turn into a Message object
    msg = response["choices"][0]["text"]
    # return the text output and the new conversation
    # print("msg:%s, conversation:%s", msg, conversation)

    return msg, conversation + msg


def parse_and_include_edges(output: str) -> []:
    """Parse output from LLM (GPT-3) and include the edges in the graph.

    Args:
        output (str): output from LLM (GPT-3) to be parsed
        replace (bool, optional): if True, replace all edges with the new ones,
            otherwise add to existing edges. Defaults to True.
    """
    # print(output)
    # Regex patterns
    pattern = r'(add)\("([^()"]+)",\s*"([^()"]+)"\)'

    # Find all matches in the text
    matches = re.findall(pattern, output)

    result = []
    for match in matches:
        op, *args = match
        add = op == "add"
        if add:
            a, b = args
            if a == b:
                continue
            result.append(b)
        else:
            pass

    # print(result)
    return result


class MindMap2:
    """A class that represents a mind map as a graph.
    """

    def __init__(self) -> None:
        self.conversation = ""

    def ask_for_initial_graph(self, query: str) -> []:
        """Ask GPT-3 to construct a graph from scrach.

        Args:
            query (str): The query to ask GPT-3 about.

        Returns:
            str: The output from GPT-3.
        """

        conversation = START_CONVERSATION2 + f"""
                现在忽略掉之前的测试案例，我们重新开始。
                我希望你根据下面的描述创建：  

                Human: {query}
                AI:"""

        output, self.conversation = ask_chatgpt(conversation)
        # replace=True to restart
        return parse_and_include_edges(output)

    def ask_for_extended_graph(self, selected_node: Optional[str] = None, text: Optional[str] = None,
                               manual=False) -> []:
        """Cached helper function to ask GPT-3 to extend the graph.

        Args:
            query (str): query to ask GPT-3 abouty
            edges_as_text (str): edges formatted as text

        Returns:
            str: GPT-3 output
        """

        if selected_node is None and text is None and not manual:
            Log.errorf("params error")
            return

        if manual:
            if selected_node is None or text is None:
                Log.errorf("params error")
                return
            output = f"""
                add("{selected_node}","{text}")
            """
            self.conversation += f"""
                Human: add("{selected_node}","{text}")
                """
            parse_and_include_edges(output)
            # self.save()
            return

        # change description depending on if a node.py
        # was selected or a text description was given
        #
        # note that the conversation is copied (shallowly) instead
        # of modified in place. The reason for this is that if
        # the chatgpt call fails self.conversation will not
        # be updated
        if text is None:
            # prepend a description that this node.py
            # should be extended
            conversation = self.conversation + f"""
                    Human: ext("{selected_node}")
                    AI: """
            st.session_state.last_expanded = selected_node
        else:
            # just provide the description
            conversation = self.conversation + f"""
                    Human: extwith("{selected_node}", "{text}")
                    AI: """

        Log.infof("conversation: %s", conversation)

        # now self.conversation is updated
        output, self.conversation = ask_chatgpt(conversation)
        return parse_and_include_edges(output)
