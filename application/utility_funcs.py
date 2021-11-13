from application import session, Node, Tag
from sqlalchemy.orm.exc import UnmappedInstanceError

def isNode(id):
    '''
    Utility function used to check if node has been created
    '''
    return session.query(Node).filter_by(id=id).first()

# def isTag(id):
#     '''
#     Utility function used to check if tag has been created
#     '''
#     return session.query(Tag).filter_by(t)