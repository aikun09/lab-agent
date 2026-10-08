from datetime import timedelta, datetime
import jwt
from app.config import settings

def create_access_token(user_id: int) -> str:
    """创建JWT token"""
    # 过期时间
    expire = datetime.now() + timedelta(hours=settings.JWT_EXPIRE_HOURS)

    # 携带的数据
    payload = {
        "user_id": user_id,
        "exp": expire, # exp是固定的key，不能写成别的
    }

    #生成token
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY, # 密钥
        algorithm=settings.JWT_ALGORITHM, # 算法
    )

def decode_access_token(token: str) -> dict:
    """解码JWT token"""
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
