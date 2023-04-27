# -*- coding: utf-8 -*-
"""RESTful API for accessing BMSB Simulation Results"""

import os

from flask import Flask
from flask_restx import Api, Namespace, Resource

from db import Database, Query

__author__ = "Luke Zaruba"
__credits__ = ["Luke Zaruba", "Mattie Gisselbeck"]
__status__ = "Production"

# Set up DB Connection
db = Database.initialize_from_env()


# Configure API
app = Flask(__name__)
api = Api(
    app,
    prefix="/api/v1",
    doc="/api/v1/doc",
    version="1.0",
    title="Minnesota BMSB Spread Simulation & Hazard Analysis API",
    description="A RESTful API used for accessing geospatial data related to municipal BMSB hazard risk in Minnesota.",
)

# Create Namespaces
huff_simple_ns = Namespace(
    "huffsimple",
    description="Operations for accessing results of the simple Huff Simulation.",
)
huff_decay_ns = Namespace(
    "huffdecay",
    description="Operations for accessing results of the Huff (with Distance Decay) Simulation.",
)
gravity_ns = Namespace(
    "gravity", description="Operations for accessing results of the Gravity Simulation."
)

# Add Namespaces to API
api.add_namespace(huff_simple_ns)
api.add_namespace(huff_decay_ns)
api.add_namespace(gravity_ns)


# Routes for Huff (Simple) Namespace
@huff_simple_ns.route(
    "/incoming/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class HSIncoming(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.SIMPLE_HUFF_IN, top)[0][0]
        db.close()

        # Return
        return out


@huff_simple_ns.route(
    "/outgoing/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class HSOutgoing(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.SIMPLE_HUFF_OUT, top)[0][0]
        db.close()

        # Return
        return out


@huff_simple_ns.route(
    "/probability/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class HSProbability(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.SIMPLE_HUFF_RISK, top)[0][0]
        db.close()

        # Return
        return out


# Routes for Huff (Decay) Namespace
@huff_decay_ns.route(
    "/incoming/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class HDIncoming(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.DECAY_HUFF_IN, top)[0][0]
        db.close()

        # Return
        return out


@huff_decay_ns.route(
    "/outgoing/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class HDOutgoing(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.DECAY_HUFF_OUT, top)[0][0]
        db.close()

        # Return
        return out


@huff_decay_ns.route(
    "/probability/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class HDProbability(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.DECAY_HUFF_RISK, top)[0][0]
        db.close()

        # Return
        return out


# Routes for Gravity Namespace
@gravity_ns.route(
    "/incoming/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class GIncoming(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.GRAVITY_IN, top)[0][0]
        db.close()

        # Return
        return out


@gravity_ns.route(
    "/outgoing/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class GOutgoing(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.GRAVITY_OUT, top)[0][0]
        db.close()

        # Return
        return out


@gravity_ns.route(
    "/probability/<top>",
    doc={"params": {"top": "The number of top ranked results that will be returned."}},
)
class GProbability(Resource):
    def get(self, top):
        # Query
        db.connect()
        out = db.query(Query.GRAVITY_RISK, top)[0][0]
        db.close()

        # Return
        return out


if __name__ == "__main__":
    # Development
    # app.run(debug=True)

    # Production
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
