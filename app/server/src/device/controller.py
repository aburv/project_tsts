"""
Device Controller
"""

from flask import Blueprint, Response, request

from src.auth import client_auth
from src.device.service import DeviceServices
from src.responses import ValidResponse, APIException

DEVICE_BLUEPRINT = Blueprint('device', __name__)


@DEVICE_BLUEPRINT.route("/register", methods=["POST"])
@client_auth
def set_device_data() -> Response:
    """
    :return:
    :rtype:
    """
    data = request.json.get("data", {})
    try:
        device = DeviceServices().register_device(data)
        return ValidResponse(
            domain="New Device",
            detail=data,
            content=device
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()
