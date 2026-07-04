from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
Base = declarative_base()

class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String,nullable=True)
    mobile_number = Column(Integer)

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey(Contact.id))
    category_name = Column(String)
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
