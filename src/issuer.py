#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

pk = None

def init():
    global pk

    # Generate key pair
    sk = ed25519.Ed25519PrivateKey.generate()
    pk = sk.public_key()
