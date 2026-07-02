#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import json

import vc
import comms


# Public functions
def verifier_role(sock,
                  required_credential_type: vc.CredentialType,
                  accepted_authorities):
    if not comms.await_hello(sock): return False, "Subject did not send hello."

    comms.send_need(sock, required_credential_type.value)

    data = comms.await_here(sock)
    if not data: return False, "Subject did not send VC."

    cred = vc.VC.load(json.loads(data.decode()))
    if not cred.currently_valid():
        comms.send_close(sock)
        return False, "VC's validity period not active."
    if cred.typ != required_credential_type:
        comms.send_close(sock)
        return False, "VC does not provide requested permission."

    auth = any([cred.check(auth) for auth in accepted_authorities])
    if not auth:
        comms.send_close(sock)
        return False, "VC not signed by any recognized authority."

    nonce = secrets.token_bytes(32)
    comms.send_sign(sock, nonce)

    proof = comms.await_verif(sock)
    if not proof:
        return False, "Subject did not give his signature."

    if not ccore.check(cred.subject, proof, nonce):
        comms.send_close(sock)
        return False, "Subject could not verify his identity."

    comms.send_close(sock)
    return True
