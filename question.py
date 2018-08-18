from flask import abort

from datetime import datetime, timedelta
from model import *

def get_questions():
    """ Returns a number of questions for the users to tag.
    """
    # TODO: put 3 in a .yml file
    return Text.select().where(Text.completed == False).order_by(fn.Random()).limit(3)


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
        Returns true on success, false otherwise.
    """
    # Apparently peewee doesn't throw an exception when you try to create
    # a record with an invalid FK, so we have to check them manually.
    for tag in tags:
        if Text.get_or_none(Text.uuid == tag["text_uuid"]) is None:
            return False

    for tag in tags:
        Tag.create(application_uuid=app_uuid,
                   user_id=user_id,
                   text_uuid=tag["text_uuid"],
                   tag=tag["tag"])
        # TODO: if we change tagging to be continuous, the integrity
        # constraint for Text.completed should be different
        # (e.g. Text.completed iff >2 linked tags and variance is small)
        if len(list(Tag.select().where(Tag.text_uuid == tag["text_uuid"]))) > 2:
            Text.update(completed=True).where(Text.uuid == tag["text_uuid"]).execute()

    return True


def validate_captcha(secret, app_uuid):
    """ Validates the captcha.
    """
    Secret.validate(secret)
