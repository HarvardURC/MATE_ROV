#!/usr/bin/env python3

import robomodules
import os
from messages import MsgType
from flask import Flask, send_file, render_template, request, url_for, redirect

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

def main():
    server = robomodules.Server(ADDRESS, PORT, MsgType)
    server.run()

if __name__ == "__main__":
    main()
