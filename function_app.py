import azure.functions as func
import logging
from db import connect
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('table_name', "products")

    cnxn = connect()
    crsr = cnxn.cursor()
    select_sql = "SELECT * FROM [products]"
    result = crsr.execute(select_sql)
    records = [(r.product_name,r.price) for r in result]

    return func.HttpResponse(
        body=json.dumps(obj=records, indent=4)
        status_code = 200
    )