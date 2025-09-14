from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import hashlib
import base64
from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    auth_id = Column(Integer, ForeignKey("user_auth.id"), nullable=False)

    role = relationship("UserRolesModel", back_populates="users")
    auth = relationship("UserAuthModel", back_populates="auth_users")

    # ✅ Method to hash password before saving (alphanumeric only)
    def set_password(self, plain_password: str):
        hash_bytes = hashlib.sha256(plain_password.encode()).digest()
        b64_encoded = base64.b64encode(hash_bytes).decode('utf-8')
        self.password = ''.join(filter(str.isalnum, b64_encoded))

    # ✅ Method to verify password
    def verify_password(self, plain_password: str) -> bool:
        hash_bytes = hashlib.sha256(plain_password.encode()).digest()
        b64_encoded = base64.b64encode(hash_bytes).decode('utf-8')
        return self.password == ''.join(filter(str.isalnum, b64_encoded))


class UserRolesModel(Base):
    __tablename__ = "user_roles"

    roles_list = ["ADMIN", "USER"]

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship("UserModel", back_populates="role")


class UserAuthModel(Base):
    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token = Column(String(255), nullable=False)
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    auth_users = relationship("UserModel", back_populates="auth")
