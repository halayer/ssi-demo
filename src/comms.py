#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import struct


# Each protocol message consists of a first byte indicating the type,
# and the rest is type-dependent.
#
# Messages:
# Type | Name  | Data
# -----+-------+---------------------------
#   1  | Hello |
#   2  | Need  | Required credential type
#   3  | Here  | VC including signature
#   4  | Sign  | Bytes to be signed (nonce)
#   5  | Verif | Signature of nonce
#  99  | Close | Close connection.
#
# This simultaneously represents the normal communication flow, when taking the
# type number as a time-order. The first message is sent by the subject.
# Upon deviation from this protocol, the receiving party sends a Close-message
# and terminates the connection. The connection may also be closed by any party
# at any step.


# Constants
TYPE_HELLO = 1
TYPE_NEED  = 2
TYPE_HERE  = 3
TYPE_SIGN  = 4
TYPE_VERIF = 5
TYPE_CLOSE = 99


# Private functions
def _expect(sock, typ: int, enforce_length=None):
    data = sock.recv(1024)

    if data[0] != typ:
        send_close(sock)
        return False
    
    if enforce_length is not None:
        if len(data) != enforce_length:
            return False

    return data[1:]

def _pb(val: int): return struct.pack("B", val)


# Public functions
def send_hello(sock):
    sock.send(_pb(TYPE_HELLO))

def await_hello(sock):
    return _expect(sock, TYPE_HELLO, 1) == b""

def send_need(sock, typ: int):
    sock.send(_pb(TYPE_NEED) + _pb(typ))

def await_need(sock):
    data = _expect(sock, TYPE_NEED, 2)

    if data is False: return False
    
    return data[0]

def send_here(sock, data: bytes):
    sock.send(_pb(TYPE_HERE) + data)

def await_here(sock):
    return _expect(sock, TYPE_HERE)

def send_sign(sock, data: bytes):
    sock.send(_pb(TYPE_SIGN) + data)

def await_sign(sock):
    return _expect(sock, TYPE_SIGN)

def send_verif(sock, signature: bytes):
    sock.send(_pb(TYPE_VERIF) + signature)

def await_verif(sock):
    return _expect(sock, TYPE_VERIF)

def send_close(sock):
    sock.send(_pb(TYPE_CLOSE))
    sock.close()
