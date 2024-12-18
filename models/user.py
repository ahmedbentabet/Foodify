from sqlalchemy import Column, String
from base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

# Example: Inserting a new User record
new_user = User(username="Ahmed", email="ahmed@example.com", 
                password_hash="hashedpassword", role="client")
print(new_user.id)  # Outputs a new UUID like '550e8400-e29b-41d4-a716-446655440000'
