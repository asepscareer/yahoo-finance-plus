from starlette.responses import JSONResponse

def success(data, status_code=200):
    return JSONResponse(
        content={
            "data": data,
            "message": "Success!",
        },
        status_code=status_code,
    )

def notsuccess(msg, status_code=400):
    return JSONResponse(
        content={
            "data": None,
            "message": msg,
        },
        status_code=status_code,
    )
