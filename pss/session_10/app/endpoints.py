from flask import jsonify
from prepare_db import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from tables import TestTable


def home():
    return "I simply add rows to the db."


def add_row(name, age):
    engine = create_engine(DB_URL)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    
    # This is the new row that needs to be added.
    new_row = TestTable(name=name, age=age)
    
    with Session() as sess:
        sess.add(new_row)
        sess.commit()
        
    engine.dispose()  # Close the connection to the db.
    return jsonify({}), 200
    
    
def get_all_data():
    engine = create_engine(DB_URL)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    
    # Reading the data.
    with Session() as sess:
        result = sess.query(TestTable.name, TestTable.age).all()
        
    engine.dispose()
    result = [tuple(row) for row in result]  # This is to make the result json serializable.
    return jsonify(result), 200
