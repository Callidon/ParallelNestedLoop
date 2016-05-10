#!/usr/bin/env python3
# Parse SPARQl query generated by WatDiv to isolate specific patterns
# author : Thomas Minier

import re
import json
import os
import argparse
from node import Node
from triplePattern import TriplePattern

# create a list of triple patterns from a BGP contains in a text line
def loadBGP(line):
    queryBGP = list()
    bgp = re.search('WHERE {(.*)}', line).group(1)
    for triple in bgp.split(' . '):
        elements = triple.strip().split(' ')
        # check if current triple pattern is well formed
        if (len(elements) < 3) or (len(elements) > 3):
            raise SyntaxError('The pattern {} is not well formed : it must contains exactly three nodes.'.format(triple.strip()))

        # seralize it
        subject = Node(elements[0], elements[0] == '%p%')
        predicate = Node(elements[1], elements[1] == '%p%')
        obj = Node(elements[2], elements[2] == '%p%')
        queryBGP.append(TriplePattern(subject, predicate, obj))
    return queryBGP

# Main function
def main():
    parser = argparse.ArgumentParser(description='Parse SPARQl query generated by WatDiv to isolate specific patterns')
    parser.add_argument('-p', '--patterns-folder', type=str, required=True,
                        help='folder which contains query patterns for parsing')
    parser.add_argument('-q', '--queries-file', type=str, required=True,
                        help='file which contains queries to parse')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='output file')
    args = parser.parse_args()

    queryPatterns = list()
    results = list()

    # load all the patterns
    for patternFile in os.listdir(args.patterns_folder):
        queryBGP = list()
        with open("{}/{}".format(args.patterns_folder, patternFile), 'r') as reader:
            line = reader.read()
            queryPatterns.append(loadBGP(line))

    # search patterns in the queries file
    with open(args.queries_file, 'r') as reader:
        # search for each line/query
        for line in reader:
            # load current query as list of triple patterns
            bgp = loadBGP(line)
            # if this query match a pattern, save it as a result
            if bgp in queryPatterns:
                results.append(line)

    # output results in file
    with open(args.output, 'w') as writer:
        for result in results:
            writer.write(result)

if __name__ == '__main__':
    main()
