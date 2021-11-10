from pathlib import Path
from collections import OrderedDict
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
        parent = Node(master=True,label='MasterNode')
        child1 = Node(label='child1Node',parent=1)
        child2 = Node(label='child2Node',parent=1)
        session.add(parent)
        session.add(child1)
        session.add(child2)
        session.commit()

        return {'status':'success','msg':'database refreshed with sample data!'}
    
    return {'status':'success','msg':'database refreshed!'}



@process_output.formatOutput
def describe(filter=None):
    '''
    Outputs entire contents of database.
    Allows filtering.
    '''
    output = OrderedDict()
    for n in session.query(Node).all():
        attributes = OrderedDict()
        
        attributes['master']=n.master
        attributes['parent']=n.parent
        attributes['label']=n.label
        attributes['note']=n.note
        attributes['doc']=n.doc
        attributes['colour']=n.colour
        attributes['hidden']=n.hidden
        attributes['hide_children']=n.hide_children
        output[n.uid]=attributes
    return output


def findChildren(node):
    pass # Hmm
    