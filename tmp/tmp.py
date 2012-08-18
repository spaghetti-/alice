#!/usr/bin/python

from Alice import util

f = open('streams.list')
for line in f:
    line = line.rstrip('\n\r')
    util.streams.addstream(line)
f.close()
print util.streams.count()
