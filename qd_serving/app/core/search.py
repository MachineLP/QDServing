# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  Search
   Author :       machinelp
   Date :         2020-09-01
-------------------------------------------------

'''

import os
import sys
import json
import time 
from config.config import config
from app.tils.logging import logging
from flask_restful import Resource,Api
from app.core.hash_ring import HashRing
from app.grpc.grpc_client import get_res_by_grpc
from flask import Flask,abort, make_response, request, jsonify

hash_ring = HashRing( config.GRPC_HOST_LIST )

class Search(Resource):
    def __init__(self):
        pass

    def post(self):

        if not request.json or 'content' not in request.json :
            res = { "code": "400", "data": [], "message": "request is not json or content not in json" }
            return jsonify ( res )

        else:
            logging.info( "[TTSInference] [post] request.json:{}".format( request.json ) )
            text = request.json["content"]
            logging.info( "[TTSInference] [post] text:{}".format( text ) )
            grpc_host = hash_ring.get_node( str(time.time()) )
            data = get_res_by_grpc( grpc_host,text)
            res = { "code": "200", "data": data, "message": "" }
            return jsonify ( res ) 
