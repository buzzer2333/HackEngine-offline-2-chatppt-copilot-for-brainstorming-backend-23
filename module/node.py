import json


class NodeData:
    def __init__(self, label, id, color=""):
        self.label = label
        self.id = id
        self.color = color
        self.children = []

    def to_json(self):
        return {
            "label": self.label,
            "id": self.id,
            "color": self.color,
            "children": self.children
        }


