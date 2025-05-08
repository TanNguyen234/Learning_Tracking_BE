from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    created_at = Column(DateTime)

class Skills(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    status = Column(String, default="in_progress")
    created_at = Column(DateTime)

class StudyLogs(Base):
    __tablename__ = 'study_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)
    note = Column(String)
    created_at = Column(DateTime)

class Goals(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    target_hours = Column(Integer)
    current_hours = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default="in_progress") # in_progress / completed / failed
    created_at = Column(DateTime)

class Notifications(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String)
    is_read = Column(Boolean)
    created_at = Column(DateTime)