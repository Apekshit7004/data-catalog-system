from passlib.context import CryptContext

# initialize bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password to hash
password = "admin123"

# generate hash
hashed_password = pwd_context.hash(password)

print("Hashed password:", hashed_password)

# verify correct password
is_valid = pwd_context.verify(password, hashed_password)
print("Password valid:", is_valid)

# verify wrong password
is_valid_wrong = pwd_context.verify("wrong_password", hashed_password)
print("Wrong password valid:", is_valid_wrong)