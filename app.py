from flask import Flask, render_template, request, jsonify
import ast
import operator

app = Flask(__name__)

# Safe eval using ast
def safe_eval(expr):
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg
    }

    def eval_node(node):
        if isinstance(node, ast.BinOp):
            return allowed_ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return allowed_ops[type(node.op)](eval_node(node.operand))
        elif isinstance(node, ast.Num):
            return node.n
        else:
            raise ValueError("Unsupported operation")

    node = ast.parse(expr, mode='eval').body
    return eval_node(node)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        result = safe_eval(data["expression"])
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": "Invalid Expression"}), 400

if __name__ == "__main__":
    app.run(debug=True)

#main file and run this file