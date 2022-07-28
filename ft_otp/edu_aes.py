# -*- coding: utf-8 -*-
#
# ./modules/aes.py
# Eduardo Banderas Alba
# 2022-07
#
# Clase para el cifrado de las claves.
#
"""
Usage:
from aes import aes
cipher = aes('my password', 'my seed')
cipher.encrypted
cipher.decrypted

cipher.encrypt('this my secret message')
cipher.encrypted

cipher.decrypt(cipher.encrypted)
cipher.decrypted
"""
import hmac, sys

from hashlib import sha256
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# from utils.tools           import *


class aes(object):
    _key = None
    _round = 4000
    _debug = False
    _encrypt = None
    _decrypt = None
    _encrypted = None
    _decrypted = None

    class aesException(Exception):
        def __init__(self, msg):      self.msg = msg

        def __str__(self):            return repr(self.msg)

    # class aesException

    def __init__(self, k, s, debug=False, logger=sys.stderr.write):
        self.seed = s
        self.key = k
        self.debug = debug

    def __del__(self):
        if self.debug:
            logger('* aes object:')
            logger({
                'key': self.key.hex(),
                'round': self._round,
                'seed': self.seed,
                'mode': AES.MODE_CBC,
                'block_size': AES.block_size,
                'encrypt': self.encrypted,
                'decrypt': self.decrypted
            })

    def encrypt(self, plain):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        self._encrypted = b64encode(iv + cipher.encrypt(
            pad(plain.encode('UTF-8'),
                AES.block_size
                )))

    # encrypt

    def decrypt(self, encrypt):
        encrypt = b64decode(encrypt)
        iv = encrypt[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        try:
            self._decrypted = unpad(
                cipher.decrypt(encrypt[AES.block_size:]),
                AES.block_size
            )
        except:
            raise aes.aesException("ERROR: decryption failed, the password is correct")

    # decrypt

    def _kdf(self, v):
        try:
            kdf = b''
            for i in range(0, self._round):
                for c in v:
                    kdf = hmac.new(
                        self.seed.encode('UTF-8'),
                        self.seed.encode('UTF-8') + kdf + c.encode('UTF-8'),
                        digestmod=sha256
                    ).digest()

            return kdf

        except:
            raise aes.aesException('ERROR: Seed not defined')

    # _kdf

    @property
    def encrypted(self):
        data = None
        if self._encrypted:
            data = self._encrypted.decode('UTF-8')

        return data

    @encrypted.setter
    def encrypted(self, v):
        self._encrypted = v

    @property
    def decrypted(self):
        data = None
        if self._decrypted:
            data = self._decrypted.decode('UTF-8')

        return data

    @decrypted.setter
    def decrypted(self, v):
        self._decrypted = v

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, v):
        self._seed = v

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, v):
        self._key = self._kdf(v)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, v):
        self._debug = v
