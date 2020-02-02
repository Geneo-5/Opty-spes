#!/bin/sh

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

# lancement du navigateur web
case "${machine}" in
    Linux)      sensible-browser http://127.0.0.1:31415;;
    Mac)        open http://127.0.0.1:31415;;
    *)          echo "Ouvrez votre navigateur sur la page http://127.0.0.1:31415";;
esac

# lancement server
case "${machine}" in
    Linux)      run="/bin/env python3";;
    Mac)        run="/opt/local/bin/python3.7";;
    *)          run="python3";;
esac
cd srv
${run} server.py
exit 0