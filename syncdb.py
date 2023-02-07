import time

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert

# constants
# example: mssql+pyodbc://username:password@mssql_server
MSSQL_CONNECTION_LINE = 'mssql+pyodbc://username:password@mssql_server'
# example: postgresql://username:password@postgres_server/dbname
POSTGRESQL_CONNECTION_LINE = 'postgresql://username:password@postgres_server/dbname'
# Define block size for sync
BLOCK_SIZE = 1000
# MSSQL table name to synchronize
TABLE_NAME = 'table_name'

# Connect to MSSQL database
mssql_engine = create_engine(MSSQL_CONNECTION_LINE)

# Connect to PostgreSQL database
postgres_engine = create_engine(POSTGRESQL_CONNECTION_LINE)

# Read metadata from MSSQL
mssql_metadata = MetaData(bind=mssql_engine)
table = Table(TABLE_NAME, mssql_metadata, autoload=True)

# Create table in PostgreSQL if it doesn't exist
postgres_metadata = MetaData(bind=postgres_engine)
table.metadata = postgres_metadata
table.create(checkfirst=True)  # because after first run all other runs table exist

# Get total number of rows from MSSQL
mssql_conn = mssql_engine.connect()
row_count = mssql_conn.execute(select([table.c.id]).select_from(table).count()).scalar()
mssql_conn.close()

# Copy data from MSSQL to PostgreSQL in blocks
postgres_conn = postgres_engine.connect()
total_time = 0
for i in range(0, row_count, BLOCK_SIZE):
    start_time = time.perf_counter()
    data = mssql_conn.execute(select([table]).select_from(table).offset(i).limit(BLOCK_SIZE))
    postgres_conn.execute(
        insert(table).from_select(table.columns.keys(), data)
        .on_conflict_do_update(
            index_elements=table.primary_key,
            set_={c: getattr(table.c, c) for c in table.columns.keys()}
        )
    )
    end_time = time.perf_counter()
    batch_time = end_time - start_time
postgres_conn.close()

print(f"Table: {TABLE_NAME}")
print(f"Total rows synced: {row_count}")
print(f"Total time: {total_time:.2f} seconds")
