import re
import os

def validity(dataset_path, concept_dataset_path, tfidf_flag, lsa_flag, esa_flag, hidden_dimension, faiss_tfidf_flag, faiss_lsa_flag, faiss_esa_flag):
    if tfidf_flag:
        if dataset_path and os.path.exists(dataset_path):
            print("TFIDF flag is enabled and Data will be loaded from:",dataset_path)
        else:
            print("Datset path is not properly mentioned.")
            return False
    if lsa_flag:
        if dataset_path and os.path.exists(dataset_path):
            print("LSA flag is enabled and Data will be loaded from:",dataset_path,"\nLatent Dimension:",hidden_dimension)
        else:
            print("Datset path is not properly mentioned.")
            return False
    if esa_flag:
        if dataset_path and concept_dataset_path and os.path.exists(dataset_path) and os.path.exists(concept_dataset_path):
            print("ESA flag is enabled and Data will be loaded from:",dataset_path,"\nExternal Knowledge Sources will be loaded from:",concept_dataset_path)
        else:
            print("Either Datset or External Knowledge Source path is not properly mentioned.")
            return False

    if faiss_tfidf_flag:
        if tfidf_flag: print("FAISS TFIDF flag is enabled.")
        else:
            print("Please enable TFIDF flag.")
            return False

    if faiss_lsa_flag:
        if lsa_flag: print("FAISS LSA flag is enabled.")
        else:
            print("Please enable LSA flag.")
            return False 

    if faiss_esa_flag:
        if esa_flag: print("FAISS ESA flag is enabled.")
        else:
            print("Please enable ESA flag.")
            return False 
    return True


def read_configuration():
    current_dir = os.getcwd()  # Get the current working directory
    # parent_dir = os.path.dirname(current_dir)  # Get the parent directory
    # Open the file in read mode
    with open(os.path.join(current_dir, 'files', 'configuration.txt'), 'r') as file: lines = file.readlines()
    for idx in range(len(lines)):
        lines[idx] = lines[idx].replace('\n','')

    dataset_path = None
    concept_dataset_path = None
    tfidf_flag = False
    lsa_flag = False
    hidden_dimension = 600
    esa_flag = False
    faiss_tfidf_flag = False
    faiss_lsa_flag = False
    faiss_esa_flag = False

    for line in lines:
        if 'dataset_path' in line and 'concept_dataset_path' not in line:
            dataset_path = line.strip().split('=')[1].strip().strip("'")

        if 'concept_dataset_path' in line:
            concept_dataset_path = line.strip().split('=')[1].strip().strip("'")

        if 'tfidf_flag' in line and 'faiss_tfidf_flag' not in line and 'True' in line: tfidf_flag = True
        if 'lsa_flag' in line and 'faiss_lsa_flag' not in line and 'True' in line: lsa_flag = True

        if 'latent_dimension' in line:
            pattern = r'\d+'
            match = re.search(pattern, line)
            hidden_dimension = int(match.group())

        if 'esa_flag' in line and 'faiss_esa_flag' not in line and 'True' in line: esa_flag = True

        if 'faiss_tfidf_flag' in line and 'True' in line: faiss_tfidf_flag = True
        if 'faiss_lsa_flag' in line and 'True' in line: faiss_lsa_flag = True
        if 'faiss_esa_flag' in line and 'True' in line: faiss_esa_flag = True

    flag = validity(dataset_path, concept_dataset_path, tfidf_flag, lsa_flag, esa_flag, hidden_dimension, faiss_tfidf_flag, faiss_lsa_flag, faiss_esa_flag)
    return flag, dataset_path, concept_dataset_path, tfidf_flag, lsa_flag, esa_flag, hidden_dimension, faiss_tfidf_flag, faiss_lsa_flag, faiss_esa_flag

if __name__=='__main__':
    print(read_configuration())