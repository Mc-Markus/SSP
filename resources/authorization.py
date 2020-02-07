from .db_connection import db_connect
from sqlalchemy.orm import sessionmaker
import datetime
from .models import Token, Coach, User


## NOTE FOR MY PEERS USE THIS METHOD TO AUTHENTICATE YOUR ENDPOINTS ##
## Give token and needed scope for access to an endpoint ##
def check_authorization_by_scope(token, needed_scope_permission):
    from .models import Token, Coach, User
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        if "earer" in token:
            Token = session.query(Token).filter(Token.token == token[7:]).first()
        else:
            Token = session.query(Token).filter(Token.token == token).first()
        session.close()

    ##TODO add datetime.now < datetime(Token.__dict__["expired"]) not sure if correct syntax if it does not work during testing remove this
        if needed_scope_permission in Token.__dict__["scope"]:
            return True
        else:
            return False
    except:
        return False
