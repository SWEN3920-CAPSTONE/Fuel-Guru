from flask import request


def get_request_body():
    return request.get_json(force=True, silent=True) or request.form.to_dict()
