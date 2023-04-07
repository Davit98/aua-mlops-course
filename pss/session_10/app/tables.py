from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TestTable(Base):
    __tablename__ = "test_table"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    age = Column(Integer)

    def __repr__(self):
        return f"<TestTable(row_id={self.row_id}, name={self.name}, age={self.age})>"
    