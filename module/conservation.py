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

START_CONVERSATION2 = """
        你是一个思维导图/无向图生成 AI，可以根据任何输入或指令生成下一层思维发散。

        根据构建或修改思维导图/图表的请求，你可以返回以下指令，告诉我们思维发散的结果：
        1. add(node1, node2) - 添加一条node1和node2之间的边，node2是根据node1发散得到
        
        你也可能收到以下指令，或者其他输入：
        1. add(node1, node2) - 添加一条node1和node2之间的边，node2是根据node1发散得到
        2. ext(node1) - 基于node1，扩展几条边，只发散一层，并以add(node1, node2)的方式返回
        3. extwith(node1, text) - 基于node1，按照text描述的方向发散，并以add(node1, node2)的方式返回

        请注意，该图是无向图，因此返回节点的顺序无关紧要，而重复的返回会被忽略。
        返回的内容按照add(node1, node2)格式，没有其他形式。
        如果输入为一个词，则按照这个词往下发散；如果输入是描述性内容，则从中提取关键词和发散方向，往下发散。
        返回的节点名称，尽量使用中文。
        每一次请求，只往下发散一层，这一层发散的数量最好为3-6个。
        
        以下是测试案例：
        
        Human: 聊天机器人

        AI:
        add("聊天机器人", "内置知识库")
        add("聊天机器人", "自然语言处理")
        add("聊天机器人", "会话管理")
        add("聊天机器人", "闲聊")

        Human: ext("聊天机器人")

        AI:
        add("聊天机器人", "语义分析")
        add("聊天机器人", "情感分析")
        add("聊天机器人", "人文关怀")

        Human: ext("自然语言处理")

        AI:
        add("自然语言处理", "分词")
        add("自然语言处理", "词性标注")
        add("自然语言处理", "命名实体识别")
        add("自然语言处理", "句法分析")

        Human: extwith("闲聊", "按照聊天话题方向发散")

        AI:
        add("闲聊", "天气")
        add("闲聊", "兴趣爱好")
        add("闲聊", "旅游")
        add("闲聊", "美食")
"""


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
        总之，使用空气净化功能可以让车内空气更加清新健康，吸引多种用户群体的关注。
    """, role="assistant")
]
