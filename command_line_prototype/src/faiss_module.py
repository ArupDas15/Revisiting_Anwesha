import faiss
import os
import numpy as np
from scipy.sparse import csr_matrix


def load(faiss_tfidf_flag, faiss_lsa_flag, faiss_esa_flag):
	if faiss_tfidf_flag: return faiss.read_index(os.path.join("SavedModels", "faiss_tfidf_index.index"))
	if faiss_lsa_flag: return faiss.read_index(os.path.join("SavedModels", "faiss_lsa_index.index"))
	if faiss_esa_flag: return faiss.read_index(os.path.join("SavedModels", "faiss_esa_index.index"))
	print("All FAISS indices are loaded.!")

def tfidf_load(tfidf_matrix):
	tfidf_matrix = tfidf_matrix.toarray()
	nlist = 5
	quantizer = faiss.IndexFlatL2(tfidf_matrix.shape[1])
	index = faiss.IndexIVFFlat(quantizer, tfidf_matrix.shape[1], nlist, faiss.METRIC_INNER_PRODUCT)
	index.train(tfidf_matrix.astype('float32'))
	index.add(tfidf_matrix.astype('float32'))
	faiss.write_index(index,os.path.join("SavedModels", "faiss_tfidf_index.index"))
	print("FAISS TFIDF model is saved in SavedModels directory.")

def tfidf(vectorizer,index,q,k=10):
	print("The retrieval model is FAISS TFIDF.")
	qrs = [q]
	qvecs = vectorizer.transform(qrs)
	qvecs = qvecs.toarray().astype('float32')
	D, I = index.search(qvecs, k)
	return D, I

def lsa_load(dvecs):
	# dvecs = dvecs.toarray()
	nlist = 5
	quantizer = faiss.IndexFlatL2(dvecs.shape[1])
	index = faiss.IndexIVFFlat(quantizer, dvecs.shape[1], nlist, faiss.METRIC_INNER_PRODUCT)
	index.train(dvecs.astype('float32'))
	index.add(dvecs.astype('float32'))
	faiss.write_index(index,os.path.join("SavedModels", "faiss_lsa_index.index"))
	print("FAISS LSA model is saved in SavedModels directory.")

def lsa(svd_transformer,index,q,k=10):
	print("The retrieval model is FAISS LSA.")
	qrs = [q]
	qvecs = svd_transformer.transform(qrs)
	qvecs = qvecs.astype('float32')
	D, I = index.search(qvecs, k)
	return D, I


def esa_load(doc_concept_matrix):
	doc_concept_matrix = doc_concept_matrix.toarray()
	nlist = 5
	quantizer = faiss.IndexFlatL2(doc_concept_matrix.shape[1])
	index = faiss.IndexIVFFlat(quantizer, doc_concept_matrix.shape[1], nlist, faiss.METRIC_INNER_PRODUCT)
	index.train(doc_concept_matrix.astype('float32'))
	index.add(doc_concept_matrix.astype('float32'))
	faiss.write_index(index,os.path.join("SavedModels", "faiss_esa_index.index"))
	print("FAISS ESA model is saved in SavedModels directory.")

def esa(vectorizer,c_vectorizer,c_tfidf_matrix,index,q,k=10):
	print("The retrieval model is FAISS ESA.")
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
			except: continue
		q_concept_matrix[i] = tfidf_vec
	newqvecs = csr_matrix(q_concept_matrix)
	newqvecs = newqvecs.toarray().astype('float32')
	D, I = index.search(newqvecs, k)
	return D, I
