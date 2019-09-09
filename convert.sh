#!/usr/bin/env bash
convert           \
   -verbose       \
   -density 150   \
   -trim          \
    arbol.gv.pdf  \
   -quality 1000   \
   -flatten       \
   -sharpen 0x1.0 \
    arbol.jpg