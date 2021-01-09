from functools import wraps

from fastjsonschema import JsonSchemaException

from src.utils.errors import API_ERROR

from flask import request


def check_required_query_params_exist(required_params):
    def decorator(f):
        @wraps(f)
        def decorated_function(**kwargs):

            if request.method == 'GET':
                request_args = request.args

                for param in required_params:
                    if param not in request_args or request_args.get(param) == '':
                        raise API_ERROR(
                            error_type="queryParamsError",
                            message=f"{param} must be passed in the query string",
                            status_code=400
                        )

            response = f(**kwargs)
            return response

        return decorated_function

    return decorator


def validate_body(data, validator):
    try:
        validator(data)

    except JsonSchemaException as e:
        raise API_ERROR(
            error_type="requestBodyError",
            message="Invalid request body",
            status_code=400,
            details=e.message
        )