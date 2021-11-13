from pathlib import Path
from collections import OrderedDict
from sqlalchemy import inspect
from application import base, session, Node, Tag, process_output, utility_funcs


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
        t1 = Tag(tag_key='Group',tag_value='One')
        t2 = Tag(tag_key='Group',tag_value='Two')
        t3 = Tag(tag_key='Date',tag_value='13/11/2021')
        session.add(parent)
        session.add(child1)
        session.add(child2)
        session.add(t1)
        session.add(t2)
        session.add(t3)
        session.commit()
        parent.tags.append(t1)
        child1.tags.append(t2)
        child1.tags.append(t3)
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
    print(dir(Node))
    output = OrderedDict()
    for n in session.query(Node).all():
        print([c.key for c in inspect(n).mapper.column_attrs])
        output[n.id] = {c.key: getattr(n, c.key) for c in inspect(n).mapper.column_attrs}

    return output

@process_output.formatOutput
@process_output.outputSettings
def createNode(args):
    '''
    Takes id of a parent node, and optional label string. Checks if parent exists. 
    If so, creates child node and returns success message.
    Otherwise, returns failure message.
    returns dict.
    '''
    if utility_funcs.isNode(id=args.get('parent')):
        n = Node(parent=args.get('parent'),label=args['label'])
        session.add(n)
        session.commit()
        return {'status':'success','msg':'node created!'}
    else:
        return {'status':'failure','msg':'node could not be found!'}

@process_output.formatOutput
@process_output.outputSettings
def deleteNode(args):
    '''
    Takes the id of a node. Checks if it exists. If so, selects and deletes it, returning success message.
    Otherwise, return failure message.
    Returns dict.
    '''
    if utility_funcs.isNode(id=args.get('id')):
        n = session.query(Node).filter_by(id=args.get('id')).first()
        session.delete(n)
        session.commit()
        return {'status':'success','msg':'node delete!'}
    else:
        return {'status':'failure','msg':'node could not be found!'}

