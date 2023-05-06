from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src import preprocess
import joblib
import os
import pickle
import itertools


def set_up_LSA(docs, rank=600):
    preprocessor = preprocess.Document_linearization()
    vectorizer = TfidfVectorizer(tokenizer=preprocessor.pre_process, stop_words=None,
                                     use_idf=True,
                                     smooth_idf=True, max_df=0.9)
    svd_model = TruncatedSVD(n_components=rank,
                             algorithm='randomized',
                             n_iter=10)
    svd_transformer = Pipeline([('tfidf', vectorizer),
                                ('svd', svd_model)])
    dvecs = svd_transformer.fit_transform(docs)
    np.save(os.path.join('SavedModels', 'dvecs'), dvecs)
    joblib.dump(svd_transformer, os.path.join('SavedModels', 'svd_transformer.pkl'))
    joblib.dump(svd_model, os.path.join('SavedModels', 'svd_model.pkl'))
    print("LSA model is saved in SavedModels directory.")
    return vectorizer, svd_transformer, svd_model, dvecs


def load_LSA():
    vectorizer = joblib.load(os.path.join('SavedModels', 'TFIDF_vectorizer.pkl'))
    svd_transformer = joblib.load(os.path.join('SavedModels', 'svd_transformer.pkl'))
    svd_model = joblib.load(os.path.join('SavedModels', 'svd_model.pkl'))
    dvecs = np.load(os.path.join('SavedModels', 'dvecs.npy'))
    return vectorizer, svd_transformer,svd_model, dvecs


def lsa(vectorizer, svd_transformer, svd_model, docs, file_paths, dids, dvecs, q, k=10):
    print("The retrieval model is LSA.")
    qrs = [q]
    qvecs = svd_transformer.transform(qrs)
    A = cosine_similarity(qvecs, dvecs)

    pdl = []
    x = np.argsort(A[0]).T[::-1][:k]
    index = 0
    for y in x:
        if index < k:
            if A[0][y] > 0: pdl.append(tuple((file_paths[dids[y][0]], docs[dids[y][0]], dids[y][1], A[0][y])))
        index = index + 1

    return pdl