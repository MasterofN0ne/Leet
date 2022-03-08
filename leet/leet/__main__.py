import argparse


from .funcmodule import hello
from .classmodule import SheetOps
import sys
from google.oauth2.service_account import Credentials
import asyncio


def main():
    sho = SheetOps()
    
    if sho.args.command == "new":  sho.new_spreadsheet()
    elif sho.args.command == "init": sho.initializer()
    elif sho.args.command == "commit": sho.commit()
    elif sho.args.command == "push": sho.insert_values()
    elif sho.args.command == "folder": sho.create_folder()

if __name__ == '__main__':
    main()
    