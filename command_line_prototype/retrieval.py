# Outside model import
import warnings
warnings.filterwarnings('ignore')
import os
import sys
# Inside model import
from src.tfidf import load_tfidf, tfidf
from src.lsa import load_LSA, lsa
from src.esa import load_ESA, esa
from src.helper import load_train_data, load_concept_data
from src import faiss_module
from src.read_config import read_configuration


if __name__ == '__main__':
	print("Welcome to Anwesha: A Bangla Search Prototype!")
	print("Please Wait! All the components are being loaded!")

	flag, dataset_path, concept_dataset_path, tfidf_flag, lsa_flag, esa_flag, hidden_dimension, faiss_tfidf_flag, faiss_lsa_flag, faiss_esa_flag = read_configuration()
	try:
		if tfidf_flag or lsa_flag or esa_flag: docs, file_paths, dids = load_train_data()
		if esa_flag: c_docs, c_file_paths, c_dids = load_concept_data()
		if tfidf_flag: tfidf_vectorizer, tfidf_matrix = load_tfidf()
		if lsa_flag: lsa_vectorizer, svd_transformer,svd_model, dvecs = load_LSA() 
		if esa_flag: c_vectorizer, c_tfidf_matrix, doc_concept_matrix = load_ESA()
		if faiss_tfidf_flag: faiss_tfidf_index = faiss_module.load(True, False, False) 
		if faiss_lsa_flag: faiss_lsa_index = faiss_module.load(False, True, False)
		if faiss_esa_flag: faiss_esa_index = faiss_module.load(False, False, True)
		print("All the components are successfully loaded!")
	except:
		print("File corrupted! Please compile again!")
		sys.exit()
	while True:
		current_dir = os.getcwd()  # Get the current working directory
		with open(os.path.join(current_dir, 'files', 'query.txt'), encoding='utf-8') as f: q = f.read()
		print("\nThe Default Query is: ",q)
		q_key = str(input("Press 1 for default query\nPress 2 for custom query\nPress 'Q'/'q' to exit: "))
		if q_key == 'Q' or q_key == 'q': break
		elif q_key == '2': q = str(input("Please enter the Bangla Query: "))
		elif q_key == '1': pass
		else:
			print('Sorry, Wrong Input! Please try again!')
			continue

		print("\nWhich retrieval algorithm do you want to use?")

		algo_list = []
		i = 1
		if tfidf_flag:
			algo_list.append(str(i)+".TFIDF without FAISS.")
			i += 1
		if lsa_flag:
			algo_list.append(str(i)+".LSA without FAISS.")
			i += 1
		if esa_flag:
			algo_list.append(str(i)+".ESA without FAISS.")
			i += 1
		if faiss_tfidf_flag: 
			algo_list.append(str(i)+".TFIDF with FAISS.")
			i += 1
		if faiss_lsa_flag: 
			algo_list.append(str(i)+".LSA with FAISS.")
			i += 1
		if faiss_esa_flag: 
			algo_list.append(str(i)+".ESA with FAISS.")
			i += 1

		for algo in algo_list:
			print(algo)

		val = input("Please provide your choice of Algorithm or Press 'Q'/'q' to exit: ")
		if val =='Q' or val == 'q': break
		my_list = [str(i) for i in range(1, i)]
		if val not in my_list:
			print('Sorry, Wrong Input! Please try again!')
			continue
		st = algo_list[int(val)-1]
		if 'TFIDF without FAISS' in st: key = 1 
		elif 'LSA without FAISS' in st: key = 2
		elif 'ESA without FAISS' in st: key = 3
		elif 'TFIDF with FAISS' in st: key = 4
		elif 'LSA with FAISS' in st: key = 5
		elif 'ESA with FAISS' in st: key = 6 
		


		k = int(input("Provide the number of documents to be retrieved: "))

		if key in [1,2,3]:
			if key == 1: res = tfidf(tfidf_vectorizer, tfidf_matrix, q, file_paths, dids, docs, k)
			elif key == 2: res = lsa(lsa_vectorizer, svd_transformer, svd_model, docs, file_paths, dids, dvecs, q, k)
			elif key == 3: res = esa(tfidf_matrix, tfidf_vectorizer, c_vectorizer, c_tfidf_matrix, doc_concept_matrix, q, docs, file_paths, dids, k)
			print("The retrieved documents are: ")
			for i in res:
				print("Document ID:",i[2],"Similarity Score:",round(i[3],4))
				print(i[1][:100].replace('\n',' '))
		else:
			print("Facebook AI Similarity Search...")
			if key == 4: D, I = faiss_module.tfidf(tfidf_vectorizer,faiss_tfidf_index,q,k)
			elif key == 5: D, I = faiss_module.lsa(svd_transformer,faiss_lsa_index,q,k)
			elif key == 6: D, I = faiss_module.esa(tfidf_vectorizer,c_vectorizer,c_tfidf_matrix,faiss_esa_index,q,k)
			print("The retrieved documents are: ")
			for i in range(k):
				print("Document ID:",int(dids[int(I[0][i])][1]),"Similarity Score :",round(D[0][i],4))
				print(docs[int(I[0][i])][:100].replace('\n',' '))			