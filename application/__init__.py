from pathlib import Path
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import declarative_base, Session, relationship, backref
from configparser import ConfigParser
from collections import OrderedDict


basedir=Path(__file__).parent.absolute()

# Init config reader
config=ConfigParser()
config.read('application/config.ini')

# Init database
base=declarative_base()
db_path = str(config['settings']['databasepath']).strip()
if db_path[-1] == '/':
    db_path = db_path[:-1]

engine = create_engine(f'sqlite:///{db_path}/mindmap.db')
base.metadata.bind=engine
session=Session(engine)
m=MetaData()
m.reflect(engine)

association = Table('association', base.metadata,
    Column('id',Integer,primary_key=True),
    Column('node_id', Integer, ForeignKey('node.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Tag(base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag_key = Column(String)
    tag_value = Column(String)
    nodes = relationship(
        "Node",
        secondary=association,
        lazy='dynamic',
        back_populates="tags")


class Node(base):
    '''
    The individual boxes.
    If master, parents = none (?0?)
    '''
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True) # Should auto-increment    
    # master = Column(Boolean,default=False)
    parent = Column(Integer)    
    label = Column(String, default='')
    note = Column(String, default='')
    doc = Column(String, default='')
    tags = relationship("Tag", secondary=association, lazy='dynamic', back_populates="nodes")
    colour = Column(String, default='#ffffff')
    hidden = Column(Boolean, default=False)
    hide_children = Column(Boolean, default=False)
    

    def getColumnHeaders(self):
        '''
        Returns list of attributes.
        '''
        inspector = inspect(self)
        return [c_attr.key for c_attr in inspector.mapper.column_attrs]

    