# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
from pprint import pprint

from observation_extractor.model.observations import Observation
from observation_extractor.ingestors.pdf import ingest_pdf
from observation_extractor.filters.negatives import filter_negative_observations
from observation_extractor.writers.csv import write_observations_to_csv
from observation_extractor.writers.dynamodb import write_observations as write_observations_to_ddb

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'examples')


class Main:
    """
    Main class for the observer cli script
    """
    parser: argparse.ArgumentParser
    verbose: bool
    args: dict
    questions: list[str]
    observations: list[Observation]
    filtered_observations: list[Observation]
    questions_file: str

    def __init__(self):
        print("Initializing main class")
        self.verbose = False
        self.filtered_observations = []
        self.observations = []
        self.questions = []

    def parse_args(self):
        """
        Parse command line arguments
        """
        print("Parsing arguments")
        self.parser = argparse.ArgumentParser(
            prog='Observer',
            description='A tool for collecting observations from data',
            epilog='Use --help to see more options'
        )
        self.parser.add_argument('-v', '--verbose', action='store_true', default=False,
                                 help='Enable verbose outputs')
        self.parser.add_argument('-f', '--file', type=str,
                                 help='input file path')
        self.parser.add_argument('-i', '--case-id', type=str, metavar='case-id',
                                 help='a case id to associate with observations from this document')
        self.parser.add_argument('-d', '--dynamodb-table', type=str,
                                 help='name of an Amazon DynamoDB table to write observations to')
        self.parser.add_argument('-t', '--type', type=str,
                                 help='type of input [pdf] # todo: more')
        self.parser.add_argument('-o', '--out', type=str,
                                 help='output file path or table name')
        self.parser.add_argument('-j', '--out-type', type=str, metavar='out-type',
                                 help='output file format [csv, ddb] # todo: more')
        self.parser.add_argument('-q', '--questions', type=str,
                                 help='path to a text file with questions for your data')
        self.parser.add_argument('-c', '--count', type=int, default=3,
                                 help='maximum questions to include in a prompt')
        self.args = self.parser.parse_args()
        print(f"Running with args: [{self.args}]")

    def load_questions(self):
        """
        Load questions from a file
        """
        print("Loading questions")
        if self.args.questions:
            self.questions_file = self.args.questions
        else:
            self.questions_file = os.path.join(RESOURCES_DIR, 'example-questions.txt')
        print(f"Loading questions from file: {self.questions_file}")
        with open(self.questions_file, 'r') as f:
            contents = f.readlines() # input should be a newline delimited list of questions.
            self.questions.extend(contents)
        if self.verbose:
            print("Found Questions")
            for question in self.questions:
                print(f"\tQ: {question}")

    def run(self):
        self.parse_args()
        print(self.args.out_type)

        if self.args.verbose:
            print("Enabled verbose output")
            self.verbose = True
            print("Starting run")

        self.load_questions()

        questions_queue = self.questions.copy()

        # split the questions across as many prompts as we need to
        while len(questions_queue) > 0:
            max_at_a_time = self.args.count
            questions_subset = []
            for i in range(max_at_a_time):
                try:
                    question_to_add = questions_queue.pop() # get a question if available
                    questions_subset.append(question_to_add)
                except Exception as e:
                    # most likely we ran out of questions
                    # todo: check the exception explicitly
                    print(e)
                finally:
                    if self.verbose:
                        print("Done processing questions")
            if self.verbose:
                print(f"Processing: {max_at_a_time} questions")
                for q in questions_subset:
                    print(f"Q: {q}")

            metadata = {
                'question_set': self.args.questions
            }
            if self.args.case_id:
                case_id = self.args.case_id
                print(f"Got case id: {case_id}")
                metadata['case_id'] = case_id


            if self.args.type == "pdf":
                if self.verbose:
                    print("Got file type 'pdf'")
                input_file_path = self.args.file
                new_observations = ingest_pdf(input_file_path, questions_subset, metadata=metadata, verbose=self.verbose)
                self.observations.extend(new_observations)

        if self.verbose:
            print(f"Observations: ")
            for observation in self.observations:
                pprint(observation)

        # apply filters
        self.filtered_observations = filter_negative_observations((self.observations))

        # write out the filtered observations
        if self.args.out_type == 'csv': # local csv file - path specified in out
            write_observations_to_csv(self.filtered_observations, self.args.out)
        elif self.args.out_type == 'ddb': # Amazon DynamoDB table - table specified in out
            write_observations_to_ddb(case_id=case_id, observations=self.filtered_observations, table=self.args.out)

def run():
    Main().run()