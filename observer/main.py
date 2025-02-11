import argparse

from observer.model.observations import Thought, Observation


class Main:
    parser: argparse.ArgumentParser

    def __init__(self):
        print("Initializing main class")

    def parse_args(self):
        print("Processing arguments")
        self.parser = argparse.ArgumentParser(
            prog='Observer',
            description='A tool for collecting observations from data',
            epilog='Use --help to see more options'
        )
        self.parser.add_argument('-v', '--verbose', action='store_true', help='')
        self.parser.add_argument('-f', '--file', type=str, help='input file path')
        self.parser.add_argument('-t', '--type', type=str, help='type of input [pdf] # todo: more')
        self.parser.add_argument('-o', '--out-file', type=str, help='output file path')
        self.parser.add_argument('-j', '--out-type', type=str, help='output file format [csv] # todo: more')
        self.args = self.parser.parse_args()

    def run(self):
        print("Starting run")
        self.parse_args()

def run():
    Main().run()