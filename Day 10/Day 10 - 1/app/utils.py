from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# Function for comapring the 2 hashes
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)