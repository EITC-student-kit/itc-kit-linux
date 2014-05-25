#!/bin/bash

if [ $1 = "table" ]
then
    conky -c ~/.itc-kit/conky/table;
fi

if [ $1 = "rings" ]
then
    conky -c ~/.itc-kit/conky/rings;
fi

