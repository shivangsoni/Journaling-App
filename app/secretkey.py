import os
import binascii

# Generate a random secret key
secret_key = binascii.hexlify(os.urandom(24)).decode()

print(f"SECRET_KEY = '{secret_key}'")
