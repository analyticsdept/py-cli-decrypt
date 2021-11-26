from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from deferred_raise import deferred_raise
import base64
import json

class MetaCrypt():
    def __init__(self):
        pass

    def to_bytes(self, data):

        if data == None:
            return None

        if isinstance(data, bytes):
            return data

        if isinstance(data, str):
            return bytes(data.encode("utf-8"))

        if not isinstance(data, str):
            return bytes(str(data).encode("utf-8"))


    def encrypt_symmetric_siv(self, data = None, header = None, key = None, nonce = None):
        """
        `data` bytes, data to encrypt

        `header` bytes, header
        
        `key` 32 byte length, encryption key
        
        `nonce` 16 byte length, nonce - use a static nonce to produce the same output
        """

        data = self.to_bytes(data) if data else deferred_raise('no data')
        header = self.to_bytes(header) if header else deferred_raise('no header')
        key = self.to_bytes(key) if key else deferred_raise('no key')
        nonce = self.to_bytes(nonce) if nonce else deferred_raise('no nonce')
        
        cipher = AES.new(key, AES.MODE_SIV, nonce=nonce)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
        json_v = [ base64.b64encode(x).decode('utf-8') for x in (nonce, header, ciphertext, tag) ]
        result = json.dumps(dict(zip(json_k, json_v)))
        return result

    def decrypt_symmetric_siv(self, data = None, key = None):
        """
        `data` bytes, data to encrypt
        
        `key` 32 byte length, encryption key
        """
        try:
            b64 = json.loads(data)
            json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
            jv = {k:base64.b64decode(b64[k]) for k in json_k}

            cipher = AES.new(key, AES.MODE_SIV, nonce=jv['nonce'])
            cipher.update(jv['header'])
            plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
            return plaintext
        except (ValueError, KeyError) as e:
            raise Exception(f'could not decrypt data: {type(e).__name__} >> {str(e)}')