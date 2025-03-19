import argparse

def parse()-> (str, str, str):
    argparser =  argparse.ArgumentParser(description="Send SMS")
    argparser.add_argument("-s", type=str, required=True, help="Sender num")
    argparser.add_argument("-r", type=str, required=True, help="Recipient num")
    argparser.add_argument("-m", type=str, required=True, help="Text SMS")
    args = argparser.parse_args()
    return (args.s, args.r, args.m)