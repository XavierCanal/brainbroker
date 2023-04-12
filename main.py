from flask import request, jsonify, Flask
import logging
import sys
from getStock import *
from utils.mongo.historical import aggregateCompany

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/aggregateCompanies', methods=['POST'])
def update_companies():
    company_list = []
    for company in request.json['companies']:
        df = getStock(company)
        df['data'] = df.index
        data_dict = df.to_dict('records')
        return aggregateCompany(company, data_dict)


def setupLogger():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler with custom formatter
    formatter = logging.Formatter('\033[32m%(levelname)s:%(message)s\033[0m')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5050)
    setupLogger()
    logging.info("Server started")
