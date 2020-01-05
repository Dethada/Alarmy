#!/bin/bash
read -p "Rebuild frontend? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    npm run build
fi
cd nginx/
tar -czf ../config.tar.gz ./*
cd - && cd dist
tar -czf ../dist.tar.gz ./*