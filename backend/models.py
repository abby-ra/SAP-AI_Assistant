from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)
    role = Column(String)
    department = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversations = relationship("Conversation", back_populates="creator")
    comments = relationship("Comment", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    
    conversation_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"))
    title = Column(String)
    visibility = Column(String) # public, private, department
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    creator = relationship("User", back_populates="conversations")
    queries = relationship("Query", back_populates="conversation")
    comments = relationship("Comment", back_populates="conversation")

class Query(Base):
    __tablename__ = "queries"
    
    query_id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    question = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="queries")
    insight = relationship("Insight", back_populates="query", uselist=False)

class Insight(Base):
    __tablename__ = "insights"
    
    insight_id = Column(String, primary_key=True, default=generate_uuid)
    query_id = Column(String, ForeignKey("queries.query_id"))
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    query = relationship("Query", back_populates="insight")

class Comment(Base):
    __tablename__ = "comments"
    
    comment_id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Reaction(Base):
    __tablename__ = "reactions"
    
    reaction_id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    reaction_type = Column(String) # like, helpful, disagree
    created_at = Column(DateTime, default=datetime.utcnow)
