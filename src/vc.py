#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import enum
import json
from datetime import datetime
from base64 import b64encode, b64decode

import ccore
import utils


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

    def dump(self, only_tbs: bool = False):
        ret = {
            "issuer":  self.issuer.value,
            "begin":   self.begin.strftime(TIME_FORMAT),
            "end":     self.end.strftime(TIME_FORMAT),
            "typ":     self.typ.value,
            "subject": b64encode(ccore.dump_public_key(self.subject)).decode()
        }

        if self.has_signature and not only_tbs:
            ret["signature"] = b64encode(self.signature).decode()

        return ret

    @staticmethod
    def load(d: dict):
        issuer = Issuer(d["issuer"])
        begin = datetime.strptime(d["begin"], TIME_FORMAT)
        end = datetime.strptime(d["end"], TIME_FORMAT)
        typ = CredentialType(d["typ"])
        subject = ccore.load_public_key(b64decode(d["subject"].encode()))

        vc = VC(issuer, begin, end, typ, subject)

        if "signature" in d.keys():
            vc.signature = b64decode(d["signature"].encode())

        return vc

    def save(self, filename: str):
        utils.write_file(filename, json.dumps(self.dump()).encode())

    @staticmethod
    def open(filename: str):
        return VC.load(json.loads(utils.read_file(filename).decode()))

    def sign(self, secret_key):
        self.signature = ccore.sign(secret_key,
                                    json.dumps(self.dump(True)).encode())

        return self.signature

    @property
    def has_signature(self):
        return hasattr(self, "signature")

    def check(self, public_key):
        if not self.has_signature:
            raise ValueError("This VC does not have a signature.")

        return ccore.check(public_key, self.signature,
                           json.dumps(self.dump(True)).encode())

    def currently_valid(self):
        return self.begin <= datetime.now() <= self.end
