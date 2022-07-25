import sqlalchemy
from luz.secret import password

def connect_to_luz():
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/luz')
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    
    return engine, connection, metadata

if __name__ == "__main__":
    connect_to_luz()