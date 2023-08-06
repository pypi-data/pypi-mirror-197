#! /usr/bin/python

import sys
import pandas as pd

def main():
    count=int(sys.argv[1])
    for i in range(count):
        with open(f"{sys.argv[2]}_{i}.{sys.argv[3]}","w") as f:
            f.write("sample")

if __name__=="__main__":
    main()