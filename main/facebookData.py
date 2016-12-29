# -*- coding: utf-8 -*-
from main.has_permission import *
from flask import Blueprint, request, safe_join, Response, send_file, make_response
from main import db
from models import Offer, Token
import json
import os
import datetime, time
from sqlalchemy import desc

facebookDate = Blueprint('facebookDate', __name__)

@facebookDate.route('/api/dashboard')
def dashboard():
    yesterday = (datetime.datetime.now()-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
    print yesterday
