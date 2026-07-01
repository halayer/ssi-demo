#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import enum
import json
from datetime import datetime
from base64 import b64encode, b64decode

import ccore


TIME_FORMAT = "%d.%m.%Y %H:%M:%S"


class Issuer(enum.Enum):
    LBA = 1
    LUFTHANSA = 2


class CredentialType(enum.Enum):
    PILOT = 1
    AIRSIDE_EMPLOYEE = 2


class VC(object):
    
    def __init__(self, issuer: Issuer, begin: datetime, end: datetime,
                 typ: CredentialType, subject_public_key):
        self.issuer = issuer
        self.begin = begin
        self.end = end
        self.typ = typ
        self.subject = subject_public_key

    def dump(self):
        return {
            "issuer":  self.issuer.value,
            "begin":   self.begin.strftime(TIME_FORMAT),
            "end":     self.end.strftime(TIME_FORMAT),
            "typ":     self.typ.value,
            "subject": b64encode(ccore.dump_public_key(self.subject)).decode()
        }

    @staticmethod
    def load(d: dict):
        issuer = Issuer(d["issuer"])
        begin = datetime.strptime(d["begin"], TIME_FORMAT)
        end = datetime.strptime(d["end"], TIME_FORMAT)
        typ = CredentialType(d["typ"])
        subject = ccore.load_public_key(b64decode(d["subject"].encode()))

        return VC(issuer, begin, end, typ, subject)

    def sign(self, secret_key):
        self.signature = ccore.sign(secret_key,
                                    json.dumps(self.dump()).encode())

        return self.signature

    def check(self, public_key, signature: bytes):
        if ccore.check(public_key, signature, json.dumps(self.dump()).encode()):
            self._signature = signature
            return True
        
        return False
