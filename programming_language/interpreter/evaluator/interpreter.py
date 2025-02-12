class Interpreter:
    def __init__(self):
        self.global_env = {}

    def run(self, abstract_syntax_tree):
        for node in abstract_syntax_tree:
            self.visit(node)

    def visit(self, node):
        node_type = node.get("node_type")
        method_name = "visit_" + node_type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visitor method defined for node type: " + str(node.get("node_type")))

    # ------------------ Visitor Methods for AST Nodes ------------------

    def visit_recipe(self, node):
        print(f"Processing recipe: {node['name']}")
        print("Input materials:")
        for item in node["input"]:
            print(f"  Place {item['quantity']} of {item['material']} at position {item['position']}")
        print(f"Output: {node['output']}")
        print(f"Required tool: {node['tool_required']}")
        print(f"Quantity: {node['quantity']}")
        return None

    def visit_function_definition(self, node):
        self.global_env[node["name"]] = node
        print(f"Defined function: {node['name']}")
        return None

    def visit_assignment(self, node):
        value = self.visit(node["expression"])
        self.global_env[node["identifier"]] = value
        return value

    def visit_conditional(self, node):
        condition = self.visit(node["condition"])
        if condition:
            for stmt in node["then_branch"]:
                self.visit(stmt)
        elif node.get("else_branch") is not None:
            for stmt in node["else_branch"]:
                self.visit(stmt)
        return None

    def visit_while_loop(self, node):
        while self.visit(node["condition"]):
            for stmt in node["body"]:
                self.visit(stmt)
        return None

    def visit_for_loop(self, node):
        self.visit(node["init"])
        while self.visit(node["condition"]):
            for stmt in node["body"]:
                self.visit(stmt)
            self.visit(node["post"])
        return None

    def visit_log(self, node):
        value = self.visit(node["expression"])
        print(f"LOG: {value}")
        return value

    def visit_craft_command(self, node):
        recipe_name = node["recipe_name"]
        print(f"Craft command invoked for recipe: {recipe_name}")
        return None

    def visit_binary_expression(self, node):
        left = self.visit(node["left"])
        right = self.visit(node["right"])
        op = node["operator"]

        if op == "+":
            try:
                return float(left) + float(right)
            except ValueError:
                return str(left) + str(right)
        elif op == "-":
            return float(left) - float(right)
        elif op == "*":
            return float(left) * float(right)
        elif op == "/":
            return float(left) / float(right)
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return float(left) < float(right)
        elif op == ">":
            return float(left) > float(right)
        elif op == "<=":
            return float(left) <= float(right)
        elif op == ">=":
            return float(left) >= float(right)
        else:
            raise Exception("Unsupported operator: " + op)

    def visit_literal(self, node):
        value = node["value"]
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        try:
            return float(value)
        except ValueError:
            return value

    def visit_identifier(self, node):
        name = node["name"]
        if name in self.global_env:
            return self.global_env[name]
        else:
            raise Exception("Undefined variable: " + name)