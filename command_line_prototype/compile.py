# Outside model import
import warnings
warnings.filterwarnings('ignore')
import os
# Inside model import
from src.tfidf import set_up_TFIDF
from src.helper import read_train_data, read_concept_data
from src.lsa import set_up_LSA
from src.esa import set_up_ESA
from src import faiss_module
from src.read_config import read_configuration


if __name__ == '__main__':


	# Delete all the previous temporary files
	folder_path = "SavedModels"

	# Get a list of all the files in the folder
	file_list = os.listdir(folder_path)

	# Loop through the list of files and delete each one
	for file_name in file_list:
	    file_path = os.path.join(folder_path, file_name)
	    try:
	        if os.path.isfile(file_path):
	            os.remove(file_path)
	    except: pass

	flag, dataset_path, concept_dataset_path, tfidf_flag, lsa_flag, esa_flag, hidden_dimension, faiss_tfidf_flag, faiss_lsa_flag, faiss_esa_flag = read_configuration()
	if not flag: print("Please Try Again!")
	else:
		if tfidf_flag or lsa_flag or esa_flag: file_paths, dids, docs = read_train_data(dataset_path)
		if esa_flag: c_docs, c_file_paths,c_dids = read_concept_data(concept_dataset_path)

		if tfidf_flag: tfidf_vectorizer, tfidf_matrix = set_up_TFIDF(docs)
		if lsa_flag: _, _, _, dvecs = set_up_LSA(docs,hidden_dimension)
		if esa_flag: _, _, doc_concept_matrix = set_up_ESA(c_docs, tfidf_vectorizer, tfidf_matrix)

		if faiss_tfidf_flag: faiss_module.tfidf_load(tfidf_matrix)
		if faiss_lsa_flag: faiss_module.lsa_load(dvecs)
		if faiss_esa_flag: faiss_module.esa_load(doc_concept_matrix)

		print("All requirements have been compiled.")