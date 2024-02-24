import bcrypt
import os
from hashlib import pbkdf2_hmac

class PasswordManager():
    '''
    Library that manages the user's password.
    This class is responsible for Hashing and comparing the password before and after storing in the database
    '''
    def hash(self, password: str) -> str:
        '''
        Hashes the password that will be stored in the database
        '''
        prepared_password = self._prepare_password(password)
        hash = bcrypt.hashpw(prepared_password, bcrypt.gensalt())
        return hash

    def compare(self, password: str, hash:str) -> bool:
        '''
        Compares the received raw password to the stored one
        '''
        if isinstance(hash, str):
            hash = hash.encode()
        prepared_password = self._prepare_password(password)
        return bcrypt.checkpw(prepared_password, hash)
    
    def _prepare_password(self, password:str)-> str:
        '''
        Prepare the password by adding pepper and salt
        to it, before it's final hashed and stored.
        '''
        pepper=os.getenv("PASSWORD_SECRET_KEY","")
        iterations = 30000
        return pbkdf2_hmac('sha256', password.encode(), pepper.encode(), iterations).hex().encode()