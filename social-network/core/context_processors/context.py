from flask import Blueprint
from datetime import datetime


context = Blueprint('context', __name__)


@context.app_context_processor
def current_time():
    return {'now': datetime.utcnow()}
