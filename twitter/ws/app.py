from flask import Flask, render_template, request, jsonify
from random import randint

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__)
out_fp = None


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/api/item/random", methods=["GET"])
def random_items():

    item = {}
    item["id"] = randint(1, 100)
    item["text"] = "string for item {}".format(item["id"])

    app.logger.info("serving item {0}".format(item["id"]))
    return jsonify({"item": item})


@app.route("/api/item/validate", methods=["POST"])
def validate():
    data = request.get_json()
    app.logger.info("score for item {}: {}".format(data["id"], data["score"]))
    return random_items()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)
