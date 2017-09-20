#! /bin/bash
#
# rst2html.sh
# Copyright (C) 2017 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
#


for i in $(find "../Веб-программирование" -maxdepth 1 -type f -name \*.rst)
do
  RST_FILE=$i
  RST_FILE_NAME=$(basename $i)
  HTML_FILE="./.html/${RST_FILE_NAME}.html"
  HTML_DIR=$(dirname ${HTML_FILE})
  mkdir -p $HTML_DIR
  echo $RST_FILE_NAME
  rst2html5.py "$i" > "$HTML_FILE"
done
