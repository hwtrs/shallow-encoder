#!/usr/bin/env python3

# JASSjr_search.py
# Copyright (c) 2023, 2024 Vaughan Kitchen
# Minimalistic BM25 search engine.

from transformers import AutoTokenizer
from array import array
from collections import deque
import math
import struct
import sys

# Load a pre-trained tokenizer (BERT base uncased for general tokenization)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

k1 = 0.9  # BM25 k1 parameter
b = 0.4   # BM25 b parameter

def read_file(filename):
    with open(filename, mode='rb') as file:
        return file.read()

def read_lines(filename):
    with open(filename) as file:
        return file.readlines()

def decode_vocab(buffer):
    """Decode the vocabulary from binary format."""
    offset = 0
    while offset < len(buffer):
        length, = struct.unpack_from('B', buffer, offset=offset)
        offset += 1

        word, = struct.unpack_from(f'{length}s', buffer, offset=offset)
        offset += length + 1  # Null terminated

        where, size = struct.unpack_from('ii', buffer, offset=offset)
        offset += 8

        yield word.decode(), where, size

contents_vocab = read_file('vocab.bin')
doc_lengths = array('i', read_file('lengths.bin'))  # Read document lengths
doc_ids = read_lines('docids.bin')  # Read primary keys

# Compute the average document length for BM25
average_length = sum(doc_lengths) / len(doc_lengths)
vocab = {}

# Build the vocabulary in memory
for word, offset, size in decode_vocab(contents_vocab):
    vocab[word] = (offset, size)

# Open the postings list file
postings_fh = open("postings.bin", "rb")

# Search (one query per line)
for query in sys.stdin:
    query_id = 0
    accumulators = {}  # Dictionary for BM25 scores

    # Tokenize the query using Hugging Face's tokenizer
    tokenized_query = tokenizer.tokenize(query)

    # If the first token is a number, assume it's a TREC query number and remove it
    terms = deque(tokenized_query)
    if terms[0].isdigit():
        query_id = terms.popleft()

    for term in terms:
        try:
            # Check if the token exists in the vocabulary
            offset, size = vocab[term]
            postings_length = size / 8

            if len(doc_lengths) == postings_length:
                continue

            # Compute BM25 IDF
            idf = math.log(len(doc_lengths) / postings_length)

            # Read postings list
            postings_fh.seek(offset)
            for docid, freq in struct.iter_unpack('ii', postings_fh.read(size)):
                rsv = idf * ((freq * (k1 + 1)) / (freq + k1 * (1 - b + b * (doc_lengths[docid] / average_length))))
                accumulators[docid] = accumulators.get(docid, 0) + rsv
        except KeyError:
            pass

    # Convert accumulators into a sorted list
    accumulators = sorted(accumulators.items(), key=lambda x: (-x[1], x[0]))

    # Print top 1000 results in TREC format
    for i, (docid, rsv) in enumerate(accumulators[:1000], start=1):
        if rsv == 0:
            break
        print(f"{query_id} Q0 {doc_ids[docid].strip()} {i} {rsv:.4f} JASSjr")
