from flask import flash, request


def get_request_body():
    return request.get_json(force=True, silent=True) or request.form.to_dict()


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')