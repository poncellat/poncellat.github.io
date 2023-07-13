#!/bin/bash
python3 -m pelican -s pelicanconf.py
rm -rf docs
mv output docs