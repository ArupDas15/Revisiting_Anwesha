import scipy as scipy
import sklearn as sklearn
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


def set_up_ESA(c_docs, tr_vectorizer, tr_tfidf_matrix, lemmatiser=False, save_model=False):
    preprocessor = preprocess.Document_linearization()
    c_vectorizer = TfidfVectorizer(tokenizer=preprocessor.pre_process, stop_words=None,
                                       use_idf=True,
                                       smooth_idf=True, max_df=0.9)
    # Learn vocabulary and idf of the vectorizer from the training set based on the initialized parameters.
    c_vectorizer.fit(c_docs)
    # Returns document-term matrix.
    # The below tfidf_matrix has the TF-IDF values of all the documents in the corpus. This is a big sparse matrix.
    c_tfidf_matrix = c_vectorizer.transform(c_docs)
    tr_doc_term_matrix = tr_tfidf_matrix.toarray()
    # The rows in tr_doc_term_matrix represents the documents. To find which document is referred to do
    # tr_file_paths[row_number_of_tr_doc_term_matrix]
    # The columns in tr_doc_term_matrix represents the terms of the vocabulary of the train dataset.
    c_doc_term_matrix = c_tfidf_matrix.toarray()
    tr_doc_concept_matrix = np.zeros((tr_doc_term_matrix.shape[0], c_doc_term_matrix.shape[0]))

    # Returns a list of all the unique words in the vocabulary of Train Dataset.
    tr_feature_names = tr_vectorizer.get_feature_names_out()
    # Returns a list of all the unique words in the vocabulary of Concept Dataset.
    c_feature_names = c_vectorizer.get_feature_names_out()
    for i in range(0, tr_doc_term_matrix.shape[0]):
        # tr_feature_index is a numpy array. It contains the indices of the terms in document i that have non-zero
        # tfidf score.
        tr_feature_index = tr_tfidf_matrix[i, :].nonzero()[1]
        # Get the tfidf score for all the indices in tf_feature_index.
        tr_tfidf_scores = zip(tr_feature_index, [tr_tfidf_matrix[i, x] for x in tr_feature_index])
        # Create a tfidf vector of size = no. of concepts(articles) in the concept corpus. THe tfidf vector
        # represents the document vector of document i.
        tfidf_vec = np.zeros((c_doc_term_matrix.shape[0]))
        # w represents the term 't'
        # s represents the tfidf score of the term 't' in document 'd'.
        for w, s in [(tr_feature_names[i], s) for (i, s) in tr_tfidf_scores]:

            try:
                c_word_index = c_vectorizer.vocabulary_[w]

                temp_vec = np.zeros((c_doc_term_matrix.shape[0]))
                for j in range(0, c_doc_term_matrix.shape[0]):
                    temp_vec[j] = c_doc_term_matrix[j][c_word_index] * s
                tfidf_vec = tfidf_vec + temp_vec

            except:

                # if a term in train dataset is not present as a concept in the concept dataset then its tfidf score
                # is set to 0.
                continue
        # tr_filewrite.close()
        tr_doc_concept_matrix[i] = tfidf_vec
    doc_concept_matrix = csr_matrix(tr_doc_concept_matrix)
    joblib.dump(c_vectorizer, os.path.join('SavedModels', 'c_TFIDF_vectorizer.pkl'))
    sparse.save_npz(os.path.join("SavedModels", "c_TFIDFmatrix.npz"), c_tfidf_matrix)
    sparse.save_npz(os.path.join("SavedModels", "doc_concept_matrix.npz"), doc_concept_matrix)
    print("ESA model is saved in SavedModels directory.")
    return c_vectorizer, c_tfidf_matrix, doc_concept_matrix


def load_ESA():
    c_vectorizer = joblib.load(os.path.join('SavedModels', 'c_TFIDF_vectorizer.pkl'))
    # The below tfidf_matrix has the TF-IDF values of all the documents in the corpus. This is a big sparse matrix.
    c_tfidf_matrix = sparse.load_npz(os.path.join('SavedModels', "c_TFIDFmatrix.npz"))
    doc_concept_matrix = sparse.load_npz(os.path.join('SavedModels', "doc_concept_matrix.npz"))
    # return c_vectorizer, c_tfidf_matrix, c_vectorizer_lem, c_tfidf_matrix_lem, doc_concept_matrix, doc_concept_matrix_lem
    return c_vectorizer, c_tfidf_matrix, doc_concept_matrix


def esa(tr_tfidf_matrix, vectorizer, c_vectorizer, c_tfidf_matrix, doc_concept_matrix, q, docs, file_paths, dids, k=10):
    print("The retrieval model is ESA.")
    qrs = [q]
    qvecs = vectorizer.transform(qrs)

    c_doc_term_matrix = c_tfidf_matrix.toarray()
    tr_feature_names = vectorizer.get_feature_names_out()
    q_concept_matrix = np.zeros((len(qrs), c_doc_term_matrix.shape[0]))
    # Returns a list of all the unique words in the vocabulary of Train Dataset.
    for i in range(0, len(qrs)):
        q_feature_index = qvecs[i, :].nonzero()[1]
        q_tfidf_scores = zip(q_feature_index, [qvecs[i, x] for x in q_feature_index])

        tfidf_vec = np.zeros((c_doc_term_matrix.shape[0]))

        # w represents the term 't'
        # s represents the tfidf score of the term 't' in document 'd'.
        for w, s in [(tr_feature_names[i], s) for (i, s) in q_tfidf_scores]:
            try:
                c_word_index = c_vectorizer.vocabulary_[w]
                # All the documents in the Concept_Dataset is considered to be a wikipedia concept.
                temp_vec = np.zeros((c_doc_term_matrix.shape[0]))
                for j in range(0, c_doc_term_matrix.shape[0]):
                    temp_vec[j] = c_doc_term_matrix[j][c_word_index] * s

                tfidf_vec = tfidf_vec + temp_vec
            except:
                continue
        q_concept_matrix[i] = tfidf_vec

    newqvecs = csr_matrix(q_concept_matrix)
    A = cosine_similarity(newqvecs, doc_concept_matrix)
    pdl = []
    x = np.argsort(A[0]).T[::-1][:k]
    index = 0
    for y in x:
        if index < k:
            if A[0][y] > 0: pdl.append(tuple((file_paths[dids[y][0]], docs[dids[y][0]], dids[y][1], A[0][y])))
        index = index + 1

    return pdl
