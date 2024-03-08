import textwrap
import pyodbc
from auth import SERVER_PASS, SERVER_USER

def main():
    #driver
    driver = '{FreeTDS}'

    #server and database name
    server_name = 'azure-server-ale-2'
    databse_name = 'coding_test'
    server = f'{server_name}.database.windows.net,1433'

    #full connection string
    connection_string = textwrap.dedent(
        f"""
        Driver={driver};
        Server={server};
        Database={databse_name}; 
        Uid={SERVER_USER}; 
        Pwd={SERVER_PASS};
        Encrypt=yes; 
        TrustServerCertificate=no;
        Connection Timeout=30;
        """
    )

    #create pyodbc connection object
    cnxn: pyodbc.Connection = pyodbc.connect(connection_string)
    crsr: pyodbc.Cursor = cnxn.cursor()

    #define and execute a select query Query
    select_sql = "SELECT * FROM [news_articles_cnbc]"
    crsr.execute(select_sql)

    #define and execute an insert Query
    insert_sql = "INSERT INTO [new_articles_cnbc] (news_id,news_source,guid) VALUES (?,?,?)"

    #define my records
    records = [
        ("ABC123", "cnbc", "400"),
        ("ABC456", "cnbc_finance", "700")
    ]

    #define data types
    crsr.setinputsizes(
        [
            (pyodbc.SQL_WVARCHAR, 50, 0),
            (pyodbc.SQL_WVARCHAR, 50, 0),
            (pyodbc.SQL_WVARCHAR, 50, 0)
        ]
    )

    #execute the insert statement
    crsr.executemany(insert_sql,records)

    crsr.commit()
    cnxn.close()


if __name__ == "__main__":
    main()