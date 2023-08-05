import hashlib as _hashlib
import string as _string

class StringExtensions:
    def __init__(self, data: str):
        self.data = data

    def Hash(self, hashFunc=_hashlib.sha256()) -> str:
        hashFunc.update(self.data.encode())
        return hashFunc.hexdigest()

    @staticmethod
    def Random(length:int, charset=_string.ascii_letters + _string.digits):
        '''
        Generates random string with a specified length and consisting of specified charset
        @param charset: 
            * a simple string of different characters to sample the random string from.
              repeating same characters multiple times, increases probability of that character being picked more often.
            * You can enter your own characters or/and combine with defaults below.
                * string.ascii_lowercase - a-z
                * string.ascii_uppercase - A-Z
                * string.ascii_letters - lowercase + uppercase
                * string.digits - 0-9
                * string.punctuation -- all symbols
                * string.printable -- a string containing all ASCII characters considered printable
        '''
        import random
        return ''.join([random.choice(charset) for _ in range(length)])