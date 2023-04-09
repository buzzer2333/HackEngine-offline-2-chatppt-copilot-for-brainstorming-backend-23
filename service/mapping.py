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
from module.conservation import START_CONVERSATION
from module.node import NodeData

COLOR = "cyan"
FOCUS_COLOR = "red"


def ask_chatgpt(conversation: List[Message]) -> Tuple[str, List[Message]]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # asdict comes from `from dataclasses import asdict`
        messages=[asdict(c) for c in conversation]
    )

    print("response:", response)
    # turn into a Message object
    msg = Message(**response["choices"][0]["message"])
    # return the text output and the new conversation
    print("msg:%s, conversation:%s", msg, conversation)

    return msg.content, conversation + [msg]


class MindMap:
    """A class that represents a mind map as a graph.
    """

    def __init__(self, nodeData=None) -> None:
        self.root = nodeData
        self.conversation = []
        self.map = dict()
        if nodeData is not None:
            self.map[nodeData.label] = nodeData
        # self.save()

    @classmethod
    def load(cls) -> MindMap:
        """Load mindmap from session state if it exists
        
        Returns: Mindmap
        """
        if "mindmap" in st.session_state:
            return st.session_state["mindmap"]
        return cls()

    def save(self) -> None:
        pass
        # save to session state
        # st.session_state["mindmap"] = self

    def is_empty(self) -> bool:
        return self.root is None

    def ask_for_initial_graph(self, query: str) -> None:
        """Ask GPT-3 to construct a graph from scrach.

        Args:
            query (str): The query to ask GPT-3 about.

        Returns:
            str: The output from GPT-3.
        """

        conversation = START_CONVERSATION + [
            Message(f"""
                Great, now ignore all previous nodes and restart from scratch. I now want you do the following:    

                {query}
            """, role="user")
        ]

        output, self.conversation = ask_chatgpt(conversation)
        # replace=True to restart
        self.parse_and_include_edges(output)

    def ask_for_extended_graph(self, selected_node: Optional[str] = None, text: Optional[str] = None,
                               manual=False) -> None:
        """Cached helper function to ask GPT-3 to extend the graph.

        Args:
            query (str): query to ask GPT-3 abouty
            edges_as_text (str): edges formatted as text

        Returns:
            str: GPT-3 output
        """
        Log.infof("selected_node: %s, text: %s, manual: %s", selected_node, text, manual)

        if selected_node not in self.map and text is None and not manual:
            Log.errorf("params error")
            return

        if manual:
            if selected_node not in self.map or text is None:
                Log.errorf("params error")
                return
            output = f"""
                add("{selected_node}","{text}")
            """
            self.conversation.append(Message(
                output,
                role="user"
            ))
            self.parse_and_include_edges(output)
            # self.save()
            return

        # change description depending on if a node.py
        # was selected or a text description was given
        #
        # note that the conversation is copied (shallowly) instead
        # of modified in place. The reason for this is that if
        # the chatgpt call fails self.conversation will not
        # be updated
        if selected_node in self.map:
            # prepend a description that this node.py
            # should be extended
            conversation = self.conversation + [
                Message(f"""
                    add new edges to the node "{selected_node}"
                """, role="user")
            ]
            st.session_state.last_expanded = selected_node
        else:
            # just provide the description
            conversation = self.conversation + [Message(text, role="user")]

        Log.infof("conversation: %s", conversation)

        # now self.conversation is updated
        output, self.conversation = ask_chatgpt(conversation)
        self.parse_and_include_edges(output)

    def parse_and_include_edges(self, output: str) -> None:
        """Parse output from LLM (GPT-3) and include the edges in the graph.

        Args:
            output (str): output from LLM (GPT-3) to be parsed
            replace (bool, optional): if True, replace all edges with the new ones, 
                otherwise add to existing edges. Defaults to True.
        """
        print(output)
        # Regex patterns
        pattern1 = r'(add|delete)\("([^()"]+)",\s*"([^()"]+)"\)'
        pattern2 = r'(delete)\("([^()"]+)"\)'

        # Find all matches in the text
        matches = re.findall(pattern1, output) + re.findall(pattern2, output)

        for match in matches:
            op, *args = match
            add = op == "add"
            if add or (op == "delete" and len(args) == 2):
                a, b = args
                if a == b:
                    continue
                if add:
                    if a not in self.map:
                        self.root = NodeData(label=a, id="0")
                        self.map[a] = self.root
                    father = self.map[a]
                    self.map[b] = NodeData(label=b, id=father.id + "-" + str((len(father.children) + 1)))
                    father.children.append(self.map[b])
                else:
                    pass
            else:
                pass

        print(self.root)
        # self.save()

    # def _delete_node(self, node) -> None:
    #     """Delete a node.py and all edges connected to it.
    #
    #     Args:
    #         node (str): The node.py to delete.
    #     """
    #     # self.edges = [e for e in self.edges if node not in frozenset(e)]
    #     # self.nodes = list(set([n for e in self.edges for n in e]))
    #     # print(self.edges)
    #     # print(self.nodes)
    #     self.conversation.append(Message(
    #         f'delete("{node}")',
    #         role="user"
    #     ))
    #     self.save()

    # def _add_expand_delete_buttons(self, node) -> None:
    #     st.sidebar.subheader(node)
    #     cols = st.sidebar.columns(2)
    #     cols[0].button(
    #         label="Expand",
    #         on_click=self.ask_for_extended_graph,
    #         key=f"expand_{node}",
    #         # pass to on_click (self.ask_for_extended_graph)
    #         kwargs={"selected_node": node}
    #     )
    #     cols[1].button(
    #         label="Delete",
    #         on_click=self._delete_node,
    #         type="primary",
    #         key=f"delete_{node}",
    #         # pass on to _delete_node
    #         args=(node,)
    #     )

    # def visualize(self, graph_type: Literal["agraph", "networkx", "graphviz"]) -> None:
    #     """Visualize the mindmap as a graph a certain way depending on the `graph_type`.
    #
    #     Args:
    #         graph_type (Literal["agraph", "networkx", "graphviz"]): The graph type to visualize the mindmap as.
    #     Returns:
    #         Union[str, None]: Any output from the clicking the graph or
    #             if selecting a node.py in the sidebar.
    #     """
    #
    #     selected = st.session_state.get("last_expanded")
    #     if graph_type == "agraph":
    #         vis_nodes = [
    #             Node(
    #                 id=n,
    #                 label=n,
    #                 # a little bit bigger if selected
    #                 size=10 + 10 * (n == selected),
    #                 # a different color if selected
    #                 color=COLOR if n != selected else FOCUS_COLOR
    #             )
    #             for n in self.nodes
    #         ]
    #         vis_edges = [Edge(source=a, target=b) for a, b in self.edges]
    #         config = Config(width="100%",
    #                         height=600,
    #                         directed=False,
    #                         physics=True,
    #                         hierarchical=False,
    #                         )
    #         # returns a node.py if clicked, otherwise None
    #         clicked_node = agraph(nodes=vis_nodes,
    #                               edges=vis_edges,
    #                               config=config)
    #         # if clicked, update the sidebar with a button to create it
    #         if clicked_node is not None:
    #             self._add_expand_delete_buttons(clicked_node)
    #         return
    #     if graph_type == "networkx":
    #         graph = nx.Graph()
    #         for a, b in self.edges:
    #             graph.add_edge(a, b)
    #         colors = [FOCUS_COLOR if node == selected else COLOR for node in graph]
    #         fig, _ = plt.subplots(figsize=(16, 16))
    #         pos = nx.spring_layout(graph, seed=123)
    #         nx.draw(graph, pos=pos, node_color=colors, with_labels=True)
    #         st.pyplot(fig)
    #     else:  # graph_type == "graphviz":
    #         graph = graphviz.Graph()
    #         graph.attr(rankdir='LR')
    #         for a, b in self.edges:
    #             graph.edge(a, b, dir="both")
    #         for n in self.nodes:
    #             graph.node(n, style="filled", fillcolor=FOCUS_COLOR if n == selected else COLOR)
    #         # st.graphviz_chart(graph, use_container_width=True)
    #         b64 = base64.b64encode(graph.pipe(format='svg')).decode("utf-8")
    #         html = f"<img style='width: 100%' src='data:image/svg+xml;base64,{b64}'/>"
    #         st.write(html, unsafe_allow_html=True)
    #     # sort alphabetically
    #     for node in sorted(self.nodes):
    #         self._add_expand_delete_buttons(node)


def default(o):
    if isinstance(o, NodeData):
        return o.to_json()
    if isinstance(o, MindMap):
        return ""
