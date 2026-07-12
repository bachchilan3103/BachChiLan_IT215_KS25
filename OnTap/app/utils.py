from datetime import datetime

def format_response(status_code: int, data, message: str, path: str, error=None):
    return {
        "statusCode": status_code,
        "data": data,
        "message": message,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "path": path,
        "error": error
    }
