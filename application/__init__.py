from pathlib import Path
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, Session, relationship, backref
from configparser import ConfigParser


basedir=Path(__file__).parent.absolute()

# Init config reader
config=ConfigParser()
config.read('application/config.ini')


# banned_words=config['settings']['bannedwords']

# Init database
base=declarative_base()
# db_path = str(config['settings']['databasepath']).strip()
# if db_path[-1] == '/':
#     db_path = db_path[:-1]

# engine = create_engine(f'sqlite:///{db_path}/tagdb.db')
engine = create_engine('sqlite:///mindmap.db')
base.metadata.bind=engine
session=Session(engine)
m=MetaData()
m.reflect(engine)


# association = Table('association', base.metadata,
#     Column('id',Integer,primary_key=True),
#     Column('object_id', Integer, ForeignKey('object.id')),
#     Column('tag_id', Integer, ForeignKey('tag.id'))
# )

class Node(base):
    '''
    The individual boxes.
    If master, parents = none (?0?)
    '''
    __tablename__ = 'node'
    uid = Column(Integer, primary_key=True) # Should auto-increment    
    master = Column(Boolean,default=False)
    parent = Column(Integer)    
    label = Column(String, default='')
    note = Column(String, default='')
    doc = Column(String, default='')
    colour = Column(String, default='#ffffff')
    hidden = Column(Boolean, default=False)
    hide_children = Column(Boolean, default=False)

    def findChildren(uid):
        '''
        Query db for all nodes with parent=uid.
        Return list of child uids.
        '''
        nodes = [n.uid for n in session.query(Node).filter_by(parent=uid)]
        return nodes

