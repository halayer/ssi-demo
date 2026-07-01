#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


from datetime import datetime, timedelta

import ccore
import vc


def main():
    usr_sk, usr_pk = ccore.generate_keypair()
    lba_sk, lba_pk = ccore.generate_keypair()

    now = datetime.now()
    wc = vc.VC(vc.Issuer.LBA, now, now + timedelta(weeks=4),
               vc.CredentialType.PILOT, usr_pk)
    wc.sign(lba_sk)

    rc = vc.VC.load(wc.dump())
    print(rc.check(lba_pk, wc.signature))

if __name__ == "__main__":
    main()
