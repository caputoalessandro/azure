import pyodbc
from auth import SERVER_PASS, SERVER_USER


def main():
    
    cnxn = connect()
    crsr = cnxn.cursor()
    
    try:
        # create db
        crsr.execute('''
                CREATE TABLE products (
                    product_id int primary key,
                    product_name nvarchar(50),
                    price int
                    )
                    ''')
        
        #define and execute an insert Query
        insert_sql = "INSERT INTO [products] (product_id,product_name,price) VALUES (?,?,?)"

        #define my records
        records = [
            ("12", "A", "400"),
            ("58", "B", "700")
        ]

        #define data types
        crsr.setinputsizes(
            [
                (pyodbc.SQL_WVARCHAR, 50, 0),
                (pyodbc.SQL_WVARCHAR, 50, 0),
                (pyodbc.SQL_INTEGER, 50, 0)
            ]
        )

        #execute the insert statement
        crsr.executemany(insert_sql, records)
        crsr.commit()

    except:
        print("DB ALREADY EXIST")

    # define and execute a select query
    select_sql = "SELECT * FROM [products]"
    result = crsr.execute(select_sql)

    for r in result:
        print(f"product name: {r.product_name}, price: {r.price} euro")

    cnxn.close()


def connect(): 
    #driver
    driver = '{FreeTDS}'

    #server and database name
    server_name = 'azure-server-ale-2'
    databse_name = 'coding_test'
    server = f'{server_name}.database.windows.net,1433'

    connection_string = f'DRIVER={{FreeTDS}};SERVER={server};DATABASE={databse_name};UID={SERVER_USER};PWD={SERVER_PASS}'

    #create pyodbc connection object
    cnxn: pyodbc.Connection = pyodbc.connect(connection_string)
    return cnxn


if __name__ == "__main__":
    main()

