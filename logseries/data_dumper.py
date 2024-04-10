"""
    Dump out the data so we can see what is going on in there.
"""
import os, sys
import pandas as pd
import read_logs

if __name__ == "__main__":
    df = read_logs.read_logs()
    print(df)

