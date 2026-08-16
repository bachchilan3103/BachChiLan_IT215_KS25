from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError, ExpiredSignatureError


SECRET_KEY = "my-secret-key-123456"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_minutes: int) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes
    )

    payload["exp"] = expire

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except ExpiredSignatureError:
        raise ValueError("Token đã hết hạn")

    except JWTError:
        raise ValueError("Token không hợp lệ")
    
token = create_access_token(
    data={
        "sub": "student01@gmail.com",
        "user_id": 1,
        "role": "student"
    },
    expires_minutes=30
)

print("Access Token:")
print(token)

print("\nPayload:")
print(decode_access_token(token))