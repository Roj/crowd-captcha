from flask import abort

from datetime import datetime, timedelta
from model import *


# TODO: put in a .yml file
NUM_QUESTIONS = 3
MIN_QUESTIONS = 2 # Integrity constraint for Text.completed
MAX_DIFF = 0.4 # between any two elements (invariant to outliers)

def get_questions():
    """ Returns a number of questions for the users to tag.
    """
    return Text.select().where(Text.completed == False).order_by(fn.Random()).limit(NUM_QUESTIONS)


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

def min_diff(vector):
    """ Returns the minimum difference between any two elements in a list.
        Runs in O(n log n)
    """
    vector = sorted(vector)

    min_diff = vector[1]-vector[0]
    for i in range(1, len(vector) - 1):
        min_diff = min(min_diff, vector[i+1] - vector[i])

    return min_diff

def create_tags(app_uuid, user_id, tags):
    """ Creates the tags in the database.
        Returns true on success, false otherwise.
    """
    if len(tags) != NUM_QUESTIONS:
        return False

    # Apparently peewee doesn't throw an exception when you try to create
    # a record with an invalid FK, so we have to check them manually.
    for tag in tags:
        if Text.get_or_none(Text.uuid == tag["text_uuid"]) is None:
            return False

    for tag in tags:
        Tag.create(application_uuid=app_uuid,
                   user_id=user_id,
                   text_uuid=tag["text_uuid"],
                   score=tag["tag"])
        all_tags = list(Tag.select().where(Tag.text_uuid == tag["text_uuid"]))
        if len(all_tags) >= MIN_QUESTIONS:
            all_scores = [t.score for t in all_tags]
            # It is tempting to use standard deviation, but it is not sensitive
            # to outliers. e.g. stdev([1, -0.5, -0.6]) ~= 0.9
            if min_diff(all_scores) <= MAX_DIFF:
                (Text.update(completed=True)
                    .where(Text.uuid == tag["text_uuid"])
                    .execute())

    return True


def validate_captcha(secret, app_uuid):
    """ Validates the captcha.
    """
    Secret.validate(secret)
