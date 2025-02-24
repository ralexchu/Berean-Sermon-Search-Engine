import os
import requests
import pandas as pd

def main():
    my_secret = os.getenv("GITHUB")
    if not my_secret:
        raise EnvironmentError("MY_SECRET environment variable not set")
    else:
        print('pass')

if __name__ == '__main__': 
    main()

