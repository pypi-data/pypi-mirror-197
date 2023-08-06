from scinode.core.node import Node


class TestSqrtAdd(Node):

    identifier: str = "TestSqrtAdd"
    name = "TestSqrtAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_group_properties(self):
        group_properties = [
            ["sqrt1", "t", "t1"],
            ["add1", "t", "t2"],
        ]
        return group_properties

    def get_group_inputs(self):
        group_inputs = [
            ["sqrt1", "x", "x"],
            ["sqrt2", "x", "y"],
        ]
        return group_inputs

    def get_group_outputs(self):
        group_outputs = [["add1", "Result", "Result"]]
        return group_outputs

    def get_node_group(self):
        ntdata = {
            "metadata": {
                "platform": "scinode",
            },
            "nodes": {
                "sqrt1": {
                    "metadata": {
                        "identifier": "TestSqrt",
                    },
                    "properties": {},
                },
                "sqrt2": {
                    "metadata": {
                        "identifier": "TestSqrt",
                    },
                    "properties": {},
                },
                "add1": {
                    "metadata": {
                        "identifier": "TestAdd",
                    },
                    "properties": {},
                },
            },
            "links": [
                {
                    "from_node": "sqrt1",
                    "from_socket": "Result",
                    "to_node": "add1",
                    "to_socket": "x",
                },
                {
                    "from_node": "sqrt2",
                    "from_socket": "Result",
                    "to_node": "add1",
                    "to_socket": "y",
                },
            ],
        }
        return ntdata


class TestNestedSqrtAdd(Node):

    identifier: str = "TestNestedSqrtAdd"
    name = "TestNestedSqrtAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_group_inputs(self):
        group_inputs = [
            ["sqrt_add1", "x", "x"],
            ["sqrt_add2", "x", "y"],
        ]
        return group_inputs

    def get_group_outputs(self):
        group_outputs = [["add1", "Result", "Result"]]
        return group_outputs

    def get_node_group(self):
        ntdata = {
            "metadata": {
                "platform": "scinode",
            },
            "nodes": {
                "sqrt_add1": {
                    "metadata": {
                        "identifier": "TestSqrtAdd",
                    },
                    "properties": {},
                },
                "sqrt_add2": {
                    "metadata": {
                        "identifier": "TestSqrtAdd",
                    },
                    "properties": {},
                },
                "add1": {
                    "metadata": {
                        "identifier": "TestAdd",
                    },
                    "properties": {},
                },
            },
            "links": [
                {
                    "from_node": "sqrt_add1",
                    "from_socket": "Result",
                    "to_node": "add1",
                    "to_socket": "x",
                },
                {
                    "from_node": "sqrt_add2",
                    "from_socket": "Result",
                    "to_node": "add1",
                    "to_socket": "y",
                },
            ],
        }
        return ntdata


node_list = [
    TestSqrtAdd,
    TestNestedSqrtAdd,
]
