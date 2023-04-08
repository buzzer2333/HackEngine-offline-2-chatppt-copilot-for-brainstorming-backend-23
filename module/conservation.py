from module.message import Message 
START_CONVERSATION = [
    Message("""
        You are a useful mind map/undirected graph-generating AI that can generate mind maps
        based on any input or instructions.
    """, role="system"),
    Message("""
        You have the ability to perform the following actions given a request
        to construct or modify a mind map/graph:

        1. add(node1, node2) - add an edge between node1 and node2
        2. delete(node1, node2) - delete the edge between node1 and node2
        3. delete(node1) - deletes every edge connected to node1

        Note that the graph is undirected and thus the order of the nodes does not matter
        and duplicates will be ignored. Another important note: the graph should be sparse,
        with many nodes and few edges from each node. Too many edges will make it difficult 
        to understand and hard to read. The answer should only include the actions to perform, 
        nothing else. If the instructions are vague or even if only a single word is provided, 
        still generate a graph of multiple nodes and edges that that could makes sense in the 
        situation. Remember to think step by step and debate pros and cons before settling on 
        an answer to accomplish the request as well as possible.

        Here is my first request: Add a mind map about machine learning.
    """, role="user"),
    Message("""
        add("Machine learning","AI")
        add("Machine learning", "Reinforcement learning")
        add("Machine learning", "Supervised learning")
        add("Machine learning", "Unsupervised learning")
        add("Supervised learning", "Regression")
        add("Supervised learning", "Classification")
        add("Unsupervised learning", "Clustering")
        add("Unsupervised learning", "Anomaly Detection")
        add("Unsupervised learning", "Dimensionality Reduction")
        add("Unsupervised learning", "Association Rule Learning")
        add("Clustering", "K-means")
        add("Classification", "Logistic Regression")
        add("Reinforcement learning", "Proximal Policy Optimization")
        add("Reinforcement learning", "Q-learning")
    """, role="assistant"),
    Message("""
        Remove the parts about reinforcement learning and K-means.
    """, role="user"),
    Message("""
        delete("Reinforcement learning")
        delete("Clustering", "K-means")
    """, role="assistant")
]