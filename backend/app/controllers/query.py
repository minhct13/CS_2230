from flask import Blueprint, make_response, request, jsonify

# from app.services.query import QueryService

query_bp = Blueprint('query_bp', __name__)

@query_bp.route('/query',methods=['POST'])
def query():
    """
    Take input as base64 image -> response matched images in db
    """
#     image = request.json.get("base64", "")
#     res, status_code = QueryService().query(image)
    res, status_code = 'goi dc roi',200
    return make_response(
         jsonify({"message": res}),
         status_code
    )
