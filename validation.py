import numpy as np
import pandas as pd
import gseapy as gp
import math
import matplotlib.pyplot as plt

import scipy.stats as ss

from scipy.stats import hypergeom


def get_query_and_rank(features, node_names, index=0, mapping_file="validation_datasets/entrez_to_ENSP_to_symbols.csv"):
    """
    Converts the features to a gene list with their ranks

    Args:
        -features: Array of features.
        -node_names: List of node names.
        -index: Index of the feature column.
        -mapping_file: Location of the mapping file.

    """
    scores = features[:,index]
    order = np.argsort(scores)[::-1]
    gene_query_Id = [i for i in order]
    gene_query =[node_names[i] for i in order]
    gene_rank = scores.copy()
    gene_rank.sort()
    gene_rank = gene_rank[::-1].tolist()

    mapping = pd.read_csv(mapping_file)
    string_to_symbol = {}
    for i in range(len(mapping)):
        string_to_symbol[str(mapping.iloc[i,2])] = str(mapping.iloc[i,3])
    gene_rank = [gene for i,gene in enumerate(gene_rank) if gene_query[i] in string_to_symbol.keys()]
    gene_query = [string_to_symbol[gene] for gene in gene_query if gene in string_to_symbol.keys()]

    return gene_query, gene_rank, string_to_symbol


def compare_gene_lists(gene_query, gene_rank, gene_ref):
    N = len(gene_query)
    n = 100
    M = len(list(set(gene_query) & set(gene_ref)))
    m = len(list(set(gene_query[0:n]) & set(gene_ref)))
    print("""#elements in gene_query : \t\t\t{} (cutoff after {})
#elements from gene_ref in gene_query : \t{} ({}%)
#elements from gene_ref in gene_query[0:{}] : \t{} ({}%)""".format(N,n,M, int((100*M)/N),n,m, int((100*m)/n)))
    pass
    #hypergeometric test?
    #Proportion of indispensable vs neutral vs dispensables in the ref_gene_list


def compare_feature_distribution(feature, reference_genes, node_names, output_file):
    sample_genes, sample_scores, string_to_symbol = get_query_and_rank(feature.reshape((feature.shape[0],1)), node_names, index=0)
    index = {gene:i for i,gene in enumerate(sample_genes)}
    all_scores = [feature[index[gene]] for gene in sample_genes if gene in index]
    ref_scores = [feature[index[gene]] for gene in reference_genes if gene in index]

    bins = np.linspace(np.min(feature), np.max(feature), 100)
#     fig, ax = plt.subplots( nrows=1, ncols=1 )
    plt.hist(all_scores, bins, alpha=0.5, label='all', normed=True)
    plt.hist(ref_scores, bins, alpha=0.5, label='ref', normed=True)
    plt.legend()
    plt.savefig(output_file)
    plt.close()

    return ss.mannwhitneyu(all_scores, ref_scores)
