#!/usr/bin/env bash

set -o errexit

# requires: git scons build-essential python3-pip python3-setuptools python3-wheel

git clone https://github.com/Olga-Yakovleva/RHVoice.git
cd RHVoice
git checkout dc36179
scons

