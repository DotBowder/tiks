#!/bin/bash

file="./identity_files/$3_rsa_2048"
ssh-keygen -t rsa -b 2048 -f $file -N ""

#
