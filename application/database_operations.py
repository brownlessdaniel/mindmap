from pathlib import Path
from collections import OrderedDict
from sqlalchemy import inspect
from application import base, session, Node, process_output


@process_output.formatOutput
@process_output.outputSettings
def deleteDatabase(args=None):
    '''
    Deletes the db
    Returns dictionary.
    '''    
    if len(list(Path.cwd().glob("mindmap.db"))) == 0:
        return {'status':'failure','msg':'database could not be found'}
    else:
        [item.unlink() for item in Path.cwd().glob("mindmap.db")]
        return {'status':'success','msg':'database deleted!'}

@process_output.formatOutput
@process_output.outputSettings
def refreshDatabase(args):
    '''
    Deletes all data stored in db. If sample, populates db with sample data.
    Returns dictionary.
    '''
    base.metadata.drop_all()
    base.metadata.create_all()
    if args['sample']:
        # parent = Node(master=True,label='MasterNode')
        parent = Node(label='MasterNode', parent=0)
        child1 = Node(label='child1Node',parent=1)
        child2 = Node(label='child2Node',parent=1)
        session.add(parent)
        session.add(child1)
        session.add(child2)
        session.commit()

        return {'status':'success','msg':'database refreshed with sample data!'}
    
    return {'status':'success','msg':'database refreshed!'}

@process_output.formatOutput
@process_output.outputSettings
def describe(filter=None):
    '''
    Outputs entire contents of database.
    Allows filtering.
    '''
    output = OrderedDict()

    for n in session.query(Node).all():
        output[n.uid] = {c.key: getattr(n, c.key) for c in inspect(n).mapper.column_attrs}

    return output

@process_output.formatOutput
@process_output.outputSettings
def createNode(args):
    '''
    Creates a child node, given the parent node uid.
    Requires a label.
    Returns success message
    '''
    n = Node(parent=args.get('parent'),label=args['label'])
    session.add(n)
    session.commit()
    return {'status':'success','msg':'node created!'}
    
def deleteNode(args):
    '''
    Selects a node based on it's uid, and deletes it.
    returns a success message
    '''
    n = session.query(Node).filter_by(uid=args.get('uid')).first()
    session.remove(n)
    session.commit()
    return {'status':'success','msg':'node delete!'}