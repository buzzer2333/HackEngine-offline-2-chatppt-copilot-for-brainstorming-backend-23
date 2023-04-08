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
from service.mapping import MindMap
from module.message import Message 

# set title of page (will be seen in tab) and the width
st.set_page_config(page_title="AI Mind Maps", layout="wide")

openai.api_key = "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"

def main():
    # will initialize the graph from session state
    # (if it exists) otherwise will create a new one
    mindmap = MindMap.load()

    st.sidebar.title("AI Mind Map Generator")

    graph_type = st.sidebar.radio("Type of graph", options=["agraph", "networkx", "graphviz"])
    
    empty = mindmap.is_empty()
    reset = empty or st.sidebar.checkbox("Reset mind map", value=False)
    query = st.sidebar.text_area(
        "Describe your mind map" if reset else "Describe how to change your mind map", 
        value=st.session_state.get("mindmap-input", ""),
        key="mindmap-input",
        height=200
    )
    submit = st.sidebar.button("Submit")

    valid_submission = submit and query != ""

    if empty and not valid_submission:
        return

    with st.spinner(text="Loading graph..."):
        # if submit and non-empty query, then update graph
        if valid_submission:
            if reset:
                # completely new mindmap
                mindmap.ask_for_initial_graph(query=query)
            else:
                # extend existing mindmap
                mindmap.ask_for_extended_graph(text=query)
            # since inputs also have to be updated, everything
            # is rerun
            st.experimental_rerun()
        else:
            mindmap.visualize(graph_type)

if __name__ == "__main__":
    main()