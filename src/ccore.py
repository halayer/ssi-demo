#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

import utils


# Constants
KEY_ENCODING = serialization.Encoding.Raw

SECRET_KEY_FORMAT = serialization.PrivateFormat.Raw
SECRET_KEY_ENCRYPTION = serialization.NoEncryption()

PUBLIC_KEY_FORMAT = serialization.PublicFormat.Raw


# Public functions
def generate_keypair():
    secret_key = ed25519.Ed25519PrivateKey.generate()
    public_key = secret_key.public_key()

    return secret_key, public_key

# Serialisation routines for secret keys
def dump_secret_key(secret_key):
    return secret_key.private_bytes(
        encoding=KEY_ENCODING, format=SECRET_KEY_FORMAT,
        encryption_algorithm=SECRET_KEY_ENCRYPTION
    )

def load_secret_key(secret_bytes: bytes):
    return ed25519.Ed25519PrivateKey.from_private_bytes(secret_bytes)

def save_secret_key(secret_key, filename: str):
    utils.write_file(filename, dump_secret_key(secret_key))

def open_secret_key(filename: str):
    return load_secret_key(utils.read_file(filename))

# Serialisation routines for public keys
def dump_public_key(public_key):
    return public_key.public_bytes(
        encoding=KEY_ENCODING, format=PUBLIC_KEY_FORMAT
    )

def load_public_key(public_bytes: bytes):
    return ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)

def save_public_key(public_key, filename: str):
    utils.write_file(filename, dump_public_key(public_key))

def open_public_key(filename: str):
    return load_public_key(utils.read_file(filename))

# Routines for cryptographic signatures
def sign(secret_key, data: bytes):
    return secret_key.sign(data)

def check(public_key, signature: bytes, data: bytes):
    try:
        public_key.verify(signature, data)

        return True
    except InvalidSignature:
        return False
