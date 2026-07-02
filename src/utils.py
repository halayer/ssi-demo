#! /usr/bin/env python

# Author: henning-arvid.ladewig@airbus.com


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()

def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)
