import os
import dataset


def connect_to_db():

    constr = os.environ['CONSTR']
    constr %= os.environ['DB_KEY']
    db = dataset.connect(constr, reflect_metadata=False)
    return db