#!/bin/sh

for f in *.solidity; do
    name="`echo $f | cut -d. -f1`.lll.abi"
    solc --abi $f | grep -E "^\[" > $name
done
