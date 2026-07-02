#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import os
import sys
import argparse
from datetime import datetime, timedelta

import vc
import ccore


def main():
    parser = argparse.ArgumentParser(
        description="Generate verifiable credentials")

    parser.add_argument("usr_pk", help="User public key file",
                        default="usr_pk.key")
    parser.add_argument("lba_sk", help="LBA secret key file",
                        default="lba_sk.key")
    parser.add_argument("lh_sk", help="Lufthansa secret key file",
                        default="lh_sk.key")
    parser.add_argument("-o", "--out", help="Output directory for VC files")

    args = parser.parse_args()

    usr_pk = ccore.open_public_key(args.usr_pk)
    lba_sk = ccore.open_secret_key(args.lba_sk)
    lh_sk  = ccore.open_secret_key(args.lh_sk)

    outdir = args.out
    if not outdir: outdir = os.getcwd()
    elif not os.path.isdir(outdir):
        print(f"[-] Given output directory {outdir} does not exist!")
        return

    in_outdir = lambda filename: os.path.join(outdir, filename)

    PILOT_VC    = in_outdir("pilot.vc")
    EMPLOYEE_VC = in_outdir("employee.vc")

    now = datetime.now()
    pilot = vc.VC(vc.Issuer.LBA,
                  now, now + timedelta(weeks=52),
                  vc.CredentialType.PILOT, usr_pk)
    employee = vc.VC(vc.Issuer.LUFTHANSA,
                     now, now + timedelta(weeks=4),
                     vc.CredentialType.AIRSIDE_EMPLOYEE, usr_pk)

    pilot.sign(lba_sk)
    employee.sign(lh_sk)

    pilot.save(PILOT_VC)
    employee.save(EMPLOYEE_VC)

if __name__ == "__main__":
    main()
