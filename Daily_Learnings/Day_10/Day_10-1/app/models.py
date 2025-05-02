from .databases import Base
from sqlalchemy import Boolean, Column, ForeignKey,Integer,String, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default='True' ,nullable=False)
    created_At = Column(TIMESTAMP,server_default=text('now()') ,nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") ,nullable=False)

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_At = Column(TIMESTAMP,server_default=text('now()') ,nullable=False)