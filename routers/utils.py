def ResponseModel(data, code, message):
    return {
        "data": data,
        "code": code,
        "message": message
    }

def ErrorResponseModel(error, code):
    return{
        "error": error,
        "code": code
    }