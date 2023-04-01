from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

import config
import model
import orm
import repository
import services


def index_endpoint():
    # defining a function called index_endpoint()
    return "<p>HELLO FROM THE API</p>"


def allocate_endpoint():
    clear_mappers()  # clearing out all of the mappers that were previously created
    orm.start_mappers()  # creates an ORM session with a repository
    get_session = sessionmaker(
        bind=create_engine(config.get_sqlite_filedb_uri()))
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"],
        request.json["sku"],
        request.json["qty"],
    )

    try:  # code tries to create an OrderLine object
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400
        # any errors occur, returned with a 400 status code
    # no errors occurred, the code returns 201 status code
    return {"batchref": batchref}, 201


def create_app():  # creates a Flask app
    app = Flask(__name__)  # named app
    app.config.update({"TESTING": True})
    # updates the app to add an endpoint
    # used for displaying a list of all items
    app.add_url_rule("/", "index", view_func=index_endpoint)
    app.add_url_rule(
        "/allocate", "allocate", view_func=allocate_endpoint, methods=["POST"]
    )  # posting data to the server

    return app
