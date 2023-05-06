from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import numpy as np
from src import preprocess
import joblib
from scipy import sparse
import os
import pickle
import itertools
import statistics


def set_up_TFIDF(docs):
    current_dir = os.getcwd()  # Get the current working directory
    # parent_dir = os.path.dirname(current_dir)  # Get the parent directory


    preprocessor = preprocess.Document_linearization()
    vectorizer = TfidfVectorizer(tokenizer=preprocessor.pre_process, stop_words=None, use_idf=True, smooth_idf=True, max_df=0.9)
    # Learn vocabulary and idf of the vectorizer from the training set based on the initialized parameters.
    vectorizer.fit(docs)
    # Returns document-term matrix.
    # The below tfidf_matrix has the TF-IDF values of all the documents in the corpus. This is a big sparse matrix.
    tfidf_matrix = vectorizer.transform(docs)
    joblib.dump(vectorizer, os.path.join(current_dir, 'SavedModels', 'TFIDF_vectorizer.pkl'))
    sparse.save_npz(os.path.join(current_dir, "SavedModels", "TFIDFmatrix.npz"), tfidf_matrix)
    print("TF-IDF model is saved in SavedModels directory.")
    return vectorizer, tfidf_matrix

def load_tfidf():
    current_dir = os.getcwd()  # Get the current working directory
    parent_dir = os.path.dirname(current_dir)  # Get the parent directory

    vectorizer = joblib.load(os.path.join(current_dir, 'SavedModels', 'TFIDF_vectorizer.pkl'))
    # The below tfidf_matrix has the TF-IDF values of all the documents in the corpus. This is a big sparse matrix.
    tfidf_matrix = sparse.load_npz(os.path.join(current_dir, 'SavedModels', "TFIDFmatrix.npz"))
    return vectorizer, tfidf_matrix


def document_wt(list1, list2):
    """
    The goal of Document weight function is to assign higher weight
    to documents containing more words from the query than documents having fewer query words
    :param list1: list of words in query after pre-processing the query.
    :param list2: list of words in the document after pre-processing.
    :return: Document-Query Overlap score in the range of [0,1].
    """
    s1 = set(list1)
    s2 = set(list2)
    intersection = float(len(s1.intersection(s2)))
    query_wt = float(len(s1))
    try:
        return intersection / query_wt
    except:
        return 0


def tfidf(vectorizer, tfidf_matrix, q, file_paths, dids, docs, k=10):
    print("The retrieval model is TFIDF.")
    qrs = [q]
    qvecs = vectorizer.transform(qrs)

    # Returns a list of all the unique words in the vocabulary of the document collection.
    feature_names = vectorizer.get_feature_names_out()
    q_idx = []
    for v in qvecs:
        q_idx.append(v.indices)
    idx = []
    for v in tfidf_matrix:
        idx.append(v.indices)

    A = cosine_similarity(qvecs, tfidf_matrix)
    row_max = A.max(axis=1)
    A = A / row_max[:, np.newaxis]
    B = np.zeros(shape=A.shape)
    for i in range(0, len(qrs)):
        for j in range(0, tfidf_matrix.shape[0]):
            B[i][j] = document_wt([feature_names[x] for x in q_idx[i]],
                                  [feature_names[x] for x in tfidf_matrix[j, :].nonzero()[1]])
    for i in range(0, len(qrs)):
        for j in range(0, tfidf_matrix.shape[0]):
            try:
                A[i][j] = statistics.harmonic_mean([A[i][j], B[i][j]])
            except:
                # Whenever divide by zero error occurs we assign the f-score as 0.
                A[i][j] = 0
    pdl = []
    x = np.argsort(A[0]).T[::-1][:k]
    index = 0
    for y in x:
        if index < k:
            if A[0][y] > 0: pdl.append(tuple((file_paths[dids[y][0]], docs[dids[y][0]], dids[y][1], A[0][y])))
        index = index + 1

    return pdl
