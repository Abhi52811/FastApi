from .databases import Base
from sqlalchemy import Boolean, Column,Integer,String, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default='True' ,nullable=False)
    created_At = Column(TIMESTAMP,server_default=text('now()') ,nullable=False)
