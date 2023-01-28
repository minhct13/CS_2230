from flask import Blueprint, make_response, request, jsonify

from app.services import model
from app.services.query import query_image

query_bp = Blueprint('query_bp', __name__)

@query_bp.route('/query',methods=['POST'])
def query():
    """
    Take input as base64 image -> response matched images in db
    """
    image = request.json.get("base64", "")
    res, status_code = query_image(
                            net=model.net,
                            image=image)
    
    return make_response(
         jsonify({"message": res}),
         status_code
    )
