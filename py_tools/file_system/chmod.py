#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chmod.py
#  
#  Copyright 2017 David Deng <ddengca@gmail.com>


def make_executable(path):
    import os
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bit to X
    os.chmod(path, mode)
