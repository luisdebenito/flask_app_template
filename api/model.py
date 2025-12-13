from flask import Blueprint, request
from utils.response import Response
from repository.modelRepository import ModelRepository
from mappers.modelSerializer import ModelSerializer

Model_b = Blueprint("api_model", __name__)

@Model_b.route("/model", methods=["GET"])
def getAll():
    results = ModelRepository.getAll()
    serialized_results = ModelSerializer.serializeList(results)
    return Response.success(serialized_results)

