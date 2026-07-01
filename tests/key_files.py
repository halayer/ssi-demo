#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             "src"))

import ccore


indir = lambda filename: os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      filename)

TEST_STRING = b"bjfdbfvjkd vkjl-snvifnvLsmvlksng irh gierj fae9pwu r9w\n\r"

USR_SK = indir("usr_sk.key")
USR_PK = indir("usr_pk.key")
LBA_SK = indir("lba_sk.key")
LBA_PK = indir("lba_pk.key")


def main():
    # Generate two keypairs
    usr_sk, usr_pk = ccore.generate_keypair()
    lba_sk, lba_pk = ccore.generate_keypair()

    # Save all keys to disk
    ccore.save_secret_key(usr_sk, USR_SK)
    ccore.save_public_key(usr_pk, USR_PK)
    ccore.save_secret_key(lba_sk, LBA_SK)
    ccore.save_public_key(lba_pk, LBA_PK)

    # Load all keys from disk
    usr_sk_ = ccore.open_secret_key(USR_SK)
    usr_pk_ = ccore.open_public_key(USR_PK)
    lba_sk_ = ccore.open_secret_key(LBA_SK)
    lba_pk_ = ccore.open_public_key(LBA_PK)

    # Remove key files
    os.remove(USR_SK)
    os.remove(USR_PK)
    os.remove(LBA_SK)
    os.remove(LBA_PK)

    # Generate signatures with loaded and original version of each public key
    usr1 = ccore.sign(usr_sk, TEST_STRING)
    usr2 = ccore.sign(usr_sk_, TEST_STRING)
    lba1 = ccore.sign(lba_sk, TEST_STRING)
    lba2 = ccore.sign(lba_sk_, TEST_STRING)

    # Verify signatures in all four combinations for each keypair
    # (original, original), (original, loaded), (loaded, original),
    # (loaded, loaded)
    assert(ccore.check(usr_pk, usr1, TEST_STRING))
    assert(ccore.check(usr_pk_, usr1, TEST_STRING))
    assert(ccore.check(usr_pk, usr2, TEST_STRING))
    assert(ccore.check(usr_pk_, usr2, TEST_STRING))
    assert(ccore.check(lba_pk, lba1, TEST_STRING))
    assert(ccore.check(lba_pk_, lba1, TEST_STRING))
    assert(ccore.check(lba_pk, lba1, TEST_STRING))
    assert(ccore.check(lba_pk_, lba2, TEST_STRING))

    print("[+] Key files test successful!")

if __name__ == "__main__":
    main()
