from flask import Flask, render_template, request, jsonify
from peewee import *
import sys
sys.path.insert(0, "../../")
from model import Text, Tag, Application


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_start_string='%%',
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
out_fp = None


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/api/item/random", methods=["GET"])
def random_items():
    data = request.get_json()
    app_uuid = data["app_uuid"]

    if not Application.is_valid(app_uuid):
        abort(401)

    random_query = Text().select().order_by(fn.Random())
    text = random_query.get()

    item = {}
    item["id"] = text.uuid
    item["text"] = text.text

    app.logger.info("serving item {0}".format(item["id"]))
    return jsonify({"item": item})


@app.route("/api/item/validate", methods=["POST"])
def validate():
    data = request.get_json()
    app_uuid = data["app_uuid"]
    user_id = data["user_id"]

    if not Application.is_valid(app_uuid):
        abort(401)

    text_uuid, data_score = data["id"], data["score"]
    Tag.create(application_uuid=app_uuid,
               user_id=user_id,
               text_uuid=text_uuid,
               tag=data_score)
    return random_items()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)
