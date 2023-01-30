from flask import Blueprint, make_response, request, jsonify, current_app

from app.services.feature_extraction import extract_dataset

feature_bp = Blueprint('extract-feature', __name__)
from app.services import model 

@feature_bp.route('/extract-feature',methods=['POST'])
def extract_feature():
    """
    Take input as dataset dir -> extract and save to dataset_features.txt
    """
    dataset_dir = current_app.config['DATASET_PATH']
    res, status_code = extract_dataset(
     net=model.net,
     dataset_dir=dataset_dir)
    
    return make_response(
         jsonify({"message": res}),
         status_code
    )
