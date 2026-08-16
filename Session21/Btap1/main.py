import bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        plain_password_bytes,
        hashed_password_bytes
    )


# Dữ liệu kiểm thử
password = "Rikkei@123"

hashed_password = hash_password(password)

print("Password:", password)
print("Hashed password:", hashed_password)

print(
    "Đúng mật khẩu:",
    verify_password("Rikkei@123", hashed_password)
)

print(
    "Sai mật khẩu:",
    verify_password("Rikkei@456", hashed_password)
)