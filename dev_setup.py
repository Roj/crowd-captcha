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
        source="https://twitter.com/realDonaldTrump/status/869858333477523458"
    )


if __name__ == "__main__":
    create_tables()
    create_dev_data()

