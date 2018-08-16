from model import *

DEV_APP_UUID = "87c590b0-d62d-4dee-9eaf-36d81ae31939"
DEV_APP_SECRET = "4532ee1b-98b2-43cc-adc9-e406a2a9ae5f"


def create_dev_data():
    # application.
    algo2 = Application.create(uuid=DEV_APP_UUID, name='Algoritmos 2 - Buchwald', secret=DEV_APP_SECRET)
    
    # sample texts.
    Text.create(
        uuid="c163ba15-4c4b-43f2-81bf-dcf7f07d191b",
        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        source="https://twitter.com/amnesty/status/1026785111923195904"
    )
    Text.create(
        uuid="88517534-b8c0-4012-8067-6f5529a86910",
        text="Morbi lacinia at velit sit amet porta.",
        source="https://twitter.com/realdonaldtrump/status/449525268529815552"
    )
    Text.create(
        uuid="29d1a37f-c002-40f2-beb8-cc8a3510ee85",
        text="Phasellus malesuada molestie nunc, id suscipit sapien pharetra nec.",
        source="https://twitter.com/realDonaldTrump/status/869858333477523458",
        completed=True
    )
    Text.create(
        uuid="ca98ac2d-5e91-4157-a3c8-d96d30513d2e",
        text="Our nothingness differs little; it is a trivial and chance circumstance that you should be the reader of these exercises and I their author.",
        source="https://twitter.com/amnesty/status/1026785111923195904"
    )
    Text.create(
        uuid="5adb3921-5fd6-4182-b619-56aab3bcda41",
        text="One of the schools of Tlön goes so far as to negate time; it reasons that the present is indefinite, that the future has no reality other than as a present hope, that the past has no reality other than as a present memory. ",
        source="https://twitter.com/borges/status/81924819285986"
    )


if __name__ == "__main__":
    create_tables()
    create_dev_data()

