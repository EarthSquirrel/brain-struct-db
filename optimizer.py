# Uses conda brain-struct-db
import centrality as center
import sys
import random


# scoring matrix for all the features and algs
# degree, closeness, between, pagerank 
scoring_mat = {
    'fast': [2, 0, 0, 1],
    'exact': [1, 1, 0, 0], 
    'global': [0, 1, 1, 2], 
}


def negate_scores(scores):
    ma = max(scores)
    new = [ma-x for x in scores]
    # print(scores)
    # print(new)
    return new


if __name__ == '__main__':
    # print(sys.argv)
    # pick the speed 
    if sys.argv[1] == '0':  # slow
        print('Scoring for slow')
        ns = negate_scores(scoring_mat['fast'])
        scoring_mat['fast'] = ns
    # pick accurate
    if sys.argv[2] == '0':
        print('scoring for less exact')
        ns = negate_scores(scoring_mat['exact'])
        scoring_mat['exact'] = ns
    # pick global
    if sys.argv[3] == '0':
        print('scoring for local')
        ns = negate_scores(scoring_mat['global'])
        scoring_mat['global'] = ns
    
    # sum up the scores for each algorithm
    sums = [0, 0, 0, 0]
    for i in range(0,4):
        for key in list(scoring_mat.keys()):
            sums[i] += scoring_mat[key][i]

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
    
    # Print statistics
    f = scoring_mat['fast']
    e = scoring_mat['exact']
    g = scoring_mat['global']
    print('      Degree Close Between PageRank')
    print('Fast:   {}    {}     {}       {}'.format(f[0], f[1], f[2], f[3]))
    print('Exact:  {}    {}     {}       {}'.format(e[0], e[1], e[2], e[3]))
    print('Global: {}    {}     {}       {}'.format(g[0], g[1], g[2], g[3]))
    print('Sums:   {}    {}     {}       {}'.format(sums[0], sums[1], sums[2], sums[3]))

    print('Picking from: ', alg_run)
    if len(alg_run) > 1:
        alg = alg_run[random.randint(0, len(alg_run)-1)]
    else:
        alg = alg_run[0]
    print('Running: ', alg)
    #print('\n')
    #alg()
    """
    # Print statistics
    f = scoring_mat['fast']
    e = scoring_mat['exact']
    g = scoring_mat['global']
    print('      Degree Close Between PageRank')
    print('Fast:   {}    {}     {}       {}'.format(f[0], f[1], f[2], f[3]))
    print('Exact:  {}    {}     {}       {}'.format(e[0], e[1], e[2], e[3]))
    print('Global: {}    {}     {}       {}'.format(g[0], g[1], g[2], g[3]))
    print('Sums:   {}    {}     {}       {}'.format(sums[0], sums[1], sums[2], sums[3]))

    print('Picking from: ', alg_run)
    print('Ran: ', alg)
    """
