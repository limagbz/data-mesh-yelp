import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, String

load_dotenv()

USER = os.environ.get("POSTGRESQL_USER")
PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
HOST = os.environ.get("POSTGRESQL_HOST")
PORT = os.environ.get("POSTGRESQL_PORT")

# NOTE: Add here the database and tables name for signaling
SIGNAL_TABLES_DATABASES = [
    {"database": "user_domain", "table": "debezium_signal"},
    {"database": "business_domain", "table": "debezium_signal"},
    {"database": "checkin_domain", "table": "debezium_signal"},
    {"database": "evaluations_domain", "table": "debezium_signal"},
]

for st in SIGNAL_TABLES_DATABASES:
    engine = create_engine(
        f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{st.get("database")}'
    )
    meta = MetaData()
    table = Table(
        st.get("table"),
        meta,
        Column("id", String(42), primary_key=True),
        Column("type", String(32)),
        Column("data", String(2048)),
    )
    table.create(engine)
