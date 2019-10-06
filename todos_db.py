import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


DB_PATH = os.environ.get('DATABASE_URL')

Base = declarative_base()


class TodoItem(Base):
    __tablename__ = 'todos_table'

    uid = sqla.Column(sqla.INTEGER, primary_key=True)
    description = sqla.Column(sqla.TEXT)
    is_completed = sqla.Column(sqla.INTEGER, default=0)


def create_session():
    engine = sqla.create_engine(DB_PATH)
    
    metadata = sqla.MetaData()
    todos_table = sqla.Table('todos_table',
                        metadata,
                        sqla.Column('uid', sqla.INTEGER, primary_key=True, autoincrement=True),
                        sqla.Column('description', sqla.TEXT),
                        sqla.Column('is_completed', sqla.INTEGER, default=0))
    
    metadata.create_all(engine)
    Sessions = sessionmaker(engine)
    return Sessions()


def get_task_by_id(session, uid):
    return session.query(TodoItem).filter(TodoItem.uid == uid)[0]


def make_task_completed(session, uid):
    task = get_task_by_id(session, uid)
    task.is_completed = 1
    session.commit()


def task_to_dict(task):
    return {'uid': task.uid,
            'description': task.description.capitalize(),
            'is_completed': task.is_completed}


def get_all_tasks(session):
    return session.query(TodoItem).all()


def add_task(session, description):
    task = TodoItem(description=description)
    session.add(task)
    session.commit()


def delete_task(session, uid):
    task = get_task_by_id(session, uid)
    session.delete(task)
    session.commit()


def get_not_completed_tasks(session):
    query = session.query(TodoItem).filter(TodoItem.is_completed == '0').count()
    return query
