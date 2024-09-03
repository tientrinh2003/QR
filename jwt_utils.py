import jwt

class JWTUtils:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encode(self, payload):
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            print("Invalid token")
            return None
