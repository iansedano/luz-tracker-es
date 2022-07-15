from luz.luz_db import connect_to_luz
import sqlalchemy

engine, connection, metadata = connect_to_luz()

# Create Users table
price_table = sqlalchemy.Table(
    "price",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, nullable=False, primary_key=True),
    sqlalchemy.Column("date", sqlalchemy.BigInteger, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
)

metadata.create_all(engine)
