from passlib.context import CryptContext

context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

def create_hash(password: str) -> str:
    return context.hash(password)

def validate_hash(hash: str)-> bool:
    return context.verify(hash)