from flask import Blueprint
from flask_restful import Api
from resources.all_properties import Page

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Page, '/properties')