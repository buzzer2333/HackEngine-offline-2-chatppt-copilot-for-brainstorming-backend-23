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
        an answer to accomplish the request as well as possible. Also, the graph is disconnected.
        Node names should be in Chinese as much as possible.

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
