# user_service.py

from passlib.context import get_auto_loader
import bcrypt # Using bcrypt for universal demonstration, Argon2 recommended in production

# Initialize a context loader for standardized hashing (using bcrypt here)
# NOTE: In production, change this to Argon2 if supported by the framework
pwd_context = get_auto_loader("bcrypt") 

class PasswordHashingService:
    """
    Handles the secure transformation of plaintext passwords into salted hashes.
    """
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a plain text password using bcrypt and returns the full hash string.
        """
        if not isinstance(password, str) or not password.strip():
             raise ValueError("Password cannot be empty.")
        
        # Convert string to bytes as required by bcrypt/passlib
        password_bytes = password.encode('utf-8')
        
        # Generate the hash (this includes salting automatically)
        hashed_password = pwd_context.hash(password_bytes)
        return str(hashed_password)

    @staticmethod
    def register_user(username: str, plaintext_password: str) -> dict:
        """
        Simulates the user registration flow, ensuring hashing before saving.
        Returns a dictionary representing the data structure saved to the database.
        """
        if not username or not plaintext_password:
            raise ValueError("Username and password are required.")

        # CRITICAL FIX: Hash the password here
        hashed_pw = PasswordHashingService.hash_password(plaintext_password)

        # Simulate saving to the DB (Do NOT store plaintext!)
        user_record = {
            "username": username,
            "password_hash": hashed_pw # Storing only the hash
        }
        return user_record

    @staticmethod
    def verify_password(stored_hash: str, provided_password: str) -> bool:
        """
        Verifies a provided plaintext password against a stored hash.
        """
        try:
            provided_bytes = provided_password.encode('utf-8')
            stored_bytes = stored_hash.encode('utf-8')
            return pwd_context.verify(provided_bytes, stored_bytes)
        except ValueError:
            # Handle cases where the hash format is corrupt or invalid
            return False
