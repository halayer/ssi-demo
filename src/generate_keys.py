#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import os
import sys

import ccore


def main(outdir: str = None):
    # Generate the three keypairs
    usr_sk, usr_pk = ccore.generate_keypair()
    lba_sk, lba_pk = ccore.generate_keypair()
    lh_sk, lh_pk = ccore.generate_keypair()

    # Determine filepaths
    if outdir is None: outdir = os.getcwd()
    elif not os.path.isdir(outdir):
        print(f"[-] Given output directory {outdir} does not exist!")
        return

    in_outdir = lambda filename: os.path.join(outdir, filename)

    USR_SK = in_outdir("usr_sk.key")
    USR_PK = in_outdir("usr_pk.key")
    LBA_SK = in_outdir("lba_sk.key")
    LBA_PK = in_outdir("lba_pk.key")
    LH_SK  = in_outdir("lh_sk.key")
    LH_PK  = in_outdir("lh_pk.key")

    # Save keys
    ccore.save_secret_key(usr_sk, USR_SK)
    ccore.save_public_key(usr_pk, USR_PK)
    ccore.save_secret_key(lba_sk, LBA_SK)
    ccore.save_public_key(lba_pk, LBA_PK)
    ccore.save_secret_key(lh_sk, LH_SK)
    ccore.save_public_key(lh_pk, LH_PK)

if __name__ == "__main__":
    if len(sys.argv) == 1: main()
    elif len(sys.argv) == 2: main(sys.argv[1])
    else:
        print("usage: generate_keys.py <output directory>")
