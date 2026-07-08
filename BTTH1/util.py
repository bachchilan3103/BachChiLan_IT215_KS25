from datetime import datetime

def standard_response(status_code: int, message: str, error: str | None, data: dict | None, path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
