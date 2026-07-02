#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             "src"))

import vc
import ccore


indir = lambda filename: os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      filename)

PILOT_VC = indir("pilot.vc")
EMPLOYEE_VC = indir("employee.vc")


def main():
    # Generate three keypairs
    usr_sk, usr_pk = ccore.generate_keypair()
    lba_sk, lba_pk = ccore.generate_keypair()
    lh_sk, lh_pk   = ccore.generate_keypair()

    # Create two VCs
    now = datetime.now()
    pilot = vc.VC(vc.Issuer.LBA,
                  now, now + timedelta(weeks=52),
                  vc.CredentialType.PILOT, usr_pk)
    employee = vc.VC(vc.Issuer.LUFTHANSA,
                     now, now + timedelta(weeks=4),
                     vc.CredentialType.AIRSIDE_EMPLOYEE, usr_pk)

    # Sign the VCs
    pilot.sign(lba_sk)
    employee.sign(lh_sk)

    # Save the VCs to disk
    pilot.save(PILOT_VC)
    employee.save(EMPLOYEE_VC)

    # Load the VCs from disk
    del pilot
    del employee

    pilot = vc.VC.open(PILOT_VC)
    employee = vc.VC.open(EMPLOYEE_VC)

    # Remove files
    os.remove(PILOT_VC)
    os.remove(EMPLOYEE_VC)

    # Verify the VCs
    assert(pilot.currently_valid() and pilot.check(lba_pk))
    assert(employee.currently_valid() and employee.check(lh_pk))

    print("[+] VC files test successful!")

if __name__ == "__main__":
    main()
