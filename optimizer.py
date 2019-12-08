# Uses conda brain-struct-db
from pymongo import MongoClient, TEXT as mongoText
from pymongo.errors import DuplicateKeyError
import json
from neo4j import GraphDatabase
import re
import centrality as center
import sys
import random


# scoring matrix for all the features and algs
# degree, closeness, between, pagerank 
scoring_mat = {
    'fast': [3, 2, 2, 2],  # TODO 
    'accurate': [1, 1, 1, 0], 
    'global': [0, 1, 1, 3], 
    'diffusion': [0, 1, 2, 3]
}


def negate_scores(scores):
    ma = max(scores)
    new = [ma-x for x in scores]
    return new


if __name__ == '__main__':
    # pick the speed 
    if sys.argv[1] == '0':  # slow
        print('Want it slow')
        ns = negate_scores(scoring_mat['fast'])
        scoring_mat['fast'] = ns
    # pick accurate
    if sys.argv[2] == '0':
        ns = negate_scores(scoring_mat['accurate'])
        scoring_mat['accurate'] = ns
    # pick global
    if sys.argv[3] == '0':
        ns = negate_scores(scoring_mat['global'])
        scoring_mat['global'] = ns
    # pick diffusion
    if sys.argv[4] == '0':
        ns = negate_scores(scoring_mat['diffusion'])
        scoring_mat['diffusion'] = ns

    # sum up the scores for each algorithm
    sums = [0, 0, 0, 0]
    for i in range(0,4):
        for key in list(scoring_mat.keys()):
            sums[i] += scoring_mat[key][i]
    print(sums)

    ma = max(sums)

    alg_run = []
    if ma == sums[0]:
        alg_run.append(center.degree_centrality)
    if ma == sums[1]:
        alg_run.append(center.closeness_centrality)
    if ma == sums[2]:
        alg_run.append(center.betweenness_centrality)
    if ma == sums[3]:
        alg_run.append(center.pagerank)

    print('Picking from: ', alg_run)
    if len(alg_run) > 1:
        alg = alg_run[random.randomint(0, len(alg_run))]
    else:
        alg = alg_run[0]
    print('Running: ', alg)
    alg()
