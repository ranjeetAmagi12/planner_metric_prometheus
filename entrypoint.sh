#!/bin/bash

if [ -d "/etc/secrets/" ]; then
    echo "Beginning to load secrets"
    for file in $(ls /etc/secrets/*);
    do
        while read -rd $'' line
        do
            # Export in-line to child process and export through bash for global scope
            export $line
            echo export "$line" >> ~/.bashrc
        done < <(jq -r <<<"$(cat $file)" 'to_entries|map("\(.key)=\(.value)\u0000")[]')
    done
    source ~/.bashrc
    echo "Succefully loaded secrets"
else
    echo "Could not find /etc/secrets directory."
fi

uvicorn main:app --host 0.0.0.0 --port 8080