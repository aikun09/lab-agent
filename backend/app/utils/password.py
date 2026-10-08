import bcrypt


def hash_password(password: str) -> str:
    """哈希加密"""
    return bcrypt.hashpw(
        password.encode("utf-8"),  # 编码
        bcrypt.gensalt(),  # 加盐 保证密码随机性
    ).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码有效性"""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
