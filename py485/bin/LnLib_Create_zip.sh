#!/bin/bash

# __author__  : 'Loreto Notarantonio'
# __version__ : '07-11-2017 15.16.40'

outDIR=$1
ACTION=$2

    if [[ ! -d "$outDIR" ]]; then
        echo "output directory [$outDIR] is not valid..."
        echo "please enter it: Es: . | bin/ | .."
        exit 1
    fi

    # dirs to be included in zip file
    includeDirectories="LnLib/"
    for dir in ${includeDirectories}; do
        if [[ ! -d "$dir" ]]; then
            echo "required directory [$dir] NOT FOUND..."
            echo "... cannot continue!"
            exit 1
        fi
    done

    echo "I am in directory:.. ${PWD}"
        zipFileName="LnLib_$(date +"%Y-%m-%d").zip"
        CMD="zip -r  --exclude='*.git*' --exclude='*/__pycache__/*' ${outDIR}/${zipFileName} $includeDirectories"
        if [[ "$ACTION" == "--GO" ]]; then
            # $EXECUTE zip -r --exclude='*.git*' ${outDIR}/${zipFileName} $LnLibDir $sourceDir
            echo $CMD
            eval $CMD
            echo
            echo
            echo "${outDIR}/${zipFileName} has been crated."
            echo
        else
            echo $CMD
            echo
            echo "immettere --GO per eseguire"
        fi
    echo



