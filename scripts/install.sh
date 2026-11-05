#!/bin/bash
# Backend installation
# Create virtual environment for the project

# echo "Move installation to Docker file"

# Fail early if Node.js is outside the range required by client/package.json "engines"
node -e '
const need = [[22,23,4],[24,22,1],[26,12,1]];
const v = process.versions.node.split(".").map(Number);
const ok = need.some(([a,b,c]) => v[0]===a && (v[1]>b || (v[1]===b && v[2]>=c)));
if (!ok) { console.error("Unsupported Node.js " + process.versions.node + ". Required: ^22.23.4 || ^24.22.1 || ^26.12.1"); process.exit(1); }
' || exit 1

cd ..

python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required python packages
cd server
pip3 install --upgrade pip3
pip3 install -r requirements.txt

# Frontend installation
cd ../client
npm install --no-optional

cd ../scripts || exit
