#!/bin/bash
python3 -m pelican
rm -rf docs
mv output docs