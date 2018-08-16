from flask import abort

from datetime import datetime, timedelta
from model import *

def get_questions():
    """ Returns a number of questions for the users to tag.
    """
    # TODO: implement me.
    return Text.select()


def create_secret(app_uuid):
    expiration = datetime.now() + timedelta(minutes=10)  # 10 mins to validate captcha.
    secret = Secret.create(application_uuid=app_uuid, expiration=expiration)
    return str(secret.uuid)


def get_js(app_uuid):
    """ Returns the js file with the questions rendered.
    """
    questions = get_questions()
    # TODO: implement actual js.
    return "\n".join(str(text.uuid) + " - " + text.text for text in questions)


def create_tags(app_uuid, user_id, tags):
    """ Creates the tags in the database.
    """
    for tag in tags:
        Tag.create(application_uuid=app_uuid,
                   user_id=user_id,
                   text_uuid=tag["text_uuid"],
                   tag=tag["tag"])


def validate_captcha(secret, app_uuid):
    """ Validates the captcha.
    """
    Secret.validate(secret)
