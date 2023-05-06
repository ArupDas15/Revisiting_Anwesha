# Overview of Command Line Prototype for Anwesha: Bangla Search Engine

Command Line Prototype of Anwesha is developed to motivate the researchers or user who are willing to install the Bangla Search Engine and use it via command line. 

This prototype doesn't provide any User Interface (UI) support.

The prototype allows custom configuration by using the following file: `./files/configuration.txt`

The default query can be set in the following file: `./files/query.txt`

`compile.py` can be used to compile the documents for search.

`retrieval.py` is used to search using different algorithms via the compiled methods.

The prototype offers algorithms such as tf-idf, LSA, ESA. It also provides support to FAISS (Facebook AI Similarity Search) which helps in case of Large Scale Database.

# Steps to Install the Basic Requirements:

1. Install Python 3.8: https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe and install it.

2. Download and Install Anaconda: Refer the documentation - https://docs.anaconda.com/free/anaconda/install/windows/
Set the base interpreter as Python-3.8.10 installed in step 1 and activate it.

3. Use pip command to install below libraries: 

      `pip install flask, flask-cors, git+https://github.com/riteshpanjwani/pyiwn@master#egg=pyiwn, scikit-learn, scipy, stopwordsiso, bnlp_toolkit, indic-nlp-library, nltk, python-dotenv, weighted-levenshtein, git+https://github.com/libindic/indic-trans.git, bnunicodenormalizer, faiss-cpu`

# Example run of the Codebase where all the algorithms are compiled:


(my_env) C:\Users\joyoj\OneDrive\Desktop\command_line_prototype>python compile.py

TFIDF flag is enabled and Data will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel

LSA flag is enabled and Data will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel

Latent Dimension: 500

ESA flag is enabled and Data will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel

External Knowledge Sources will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\command_line_prototype\Concept_database

FAISS TFIDF flag is enabled.

FAISS LSA flag is enabled.

FAISS ESA flag is enabled.

The database from 'C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel' has been loaded.

The database from 'C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\command_line_prototype\Concept_database' has been loaded.

TF-IDF model is saved in SavedModels directory.

LSA model is saved in SavedModels directory.

ESA model is saved in SavedModels directory.

FAISS TFIDF model is saved in SavedModels directory.

FAISS LSA model is saved in SavedModels directory.

FAISS ESA model is saved in SavedModels directory.

All requirements have been compiled.

(my_env) C:\Users\joyoj\OneDrive\Desktop\command_line_prototype>python retrieval.py

Welcome to Anwesha: A Bangla Search Prototype!

Please Wait! All the components are being loaded!

TFIDF flag is enabled and Data will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel

LSA flag is enabled and Data will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel

Latent Dimension: 500

ESA flag is enabled and Data will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_
MTP\Complete_Test_Collection_without_RBR\Train_Dataset\14_travel

External Knowledge Sources will be loaded from: C:\Users\joyoj\OneDrive\Desktop\Desktop Files and Folders\new_MTP\command_line_prototype\Concept_database

FAISS TFIDF flag is enabled.

FAISS LSA flag is enabled.

FAISS ESA flag is enabled.

All the documents are successfully loaded.

All the concept documents are successfully loaded.

All the components are successfully loaded!

The Default Query is:  ডুয়ার্স ভ্রমণের অভিজ্ঞতা

Press 1 for default query

Press 2 for custom query

Press 'Q'/'q' to exit: 1

Which retrieval algorithm do you want to use?

1.TFIDF without FAISS.

2.LSA without FAISS.

3.ESA without FAISS.

4.TFIDF with FAISS.

5.LSA with FAISS.

6.ESA with FAISS.

Please provide your choice of Algorithm or Press 'Q'/'q' to exit: 1

Provide the number of documents to be retrieved: 10

The retrieval model is TFIDF.

The retrieved documents are:

Document ID: 14056 Similarity Score: 0.871

ডোয়ার্স বক্সা চাপড়ামারী গোরুমরা জলদাপাড়া আলিপুরদুয়ার বিন্দু বীরপাড়া চালসা কোচবিহার গোরুবাথান জল

Document ID: 14016 Similarity Score: 0.8

ডুয়ার্স পর্যটন দেখার জন্য সেরা 10টি মন্ত্রমুগ্ধকর স্থান ডুয়ার্সে ভ্রমণের সময় দেখার জন্য সেরা 10টি


Document ID: 14037 Similarity Score: 0.6325

লাটাগুড়ি গোরুমরা ট্যুর প্যাকেজ: গোরুমরা এক্সটেনসিভ ট্যুর 4N 5D আচ্ছাদিত স্থান: ডুয়ার্স - গোরুমরা ব

Document ID: 14072 Similarity Score: 0.5857

বাংলার দুয়ারে বর্ষার বিরতি যদিও বর্ষাকালে জাতীয় উদ্যানগুলি বন্ধ থাকে, আপনি ডুয়ার্সে ছুটি কাটাতে ভ

Document ID: 14113 Similarity Score: 0.4759

পশ্চিমবঙ্গের ঝালং বিন্দু ভ্রমণ 3রা অক্টোবর, 2018 ডুয়ার্স হল মনোরম সৌন্দর্যের কেন্দ্রবিন্দু এবং বিস্

Document ID: 14177 Similarity Score: 0.4609

ডুয়ার্স ডুয়ার্সে একটি আকস্মিক তবুও স্মরণীয় ট্রিপ 23শে নভেম্বর 2017 যেহেতু আমরা সবাই এখন লকডাউনের

Document ID: 14092 Similarity Score: 0.452

ডুয়ার্স ভারত ভারত ডুয়ার্স ডুয়ার্স ভারতে অবস্থিত ভূটান সংলগ্ন জনপ্রিয় একটি পর্যটন কেন্দ্র। ডুয়ার্স (D

Document ID: 14006 Similarity Score: 0.4351

ঝালং বিন্দু জলঢাকা 24 আগস্ট, 2019 তারিখে পারদ দ্বারা জলঢাকা জল প্রকল্প নিয়ে ঝালং ও বিন্দু জুন মাসে

Document ID: 14116 Similarity Score: 0.4345

ঝালং - ডুয়ার্সের সুন্দর গন্তব্য আপনি যদি একটি সুন্দর জায়গায় একটি স্মরণীয় ছুটির ভ্রমণের সন্ধান কর

Document ID: 14028 Similarity Score: 0.4147

ম্যাগনিফিসেন্ট ডোয়ার্স ট্যুর অর্ণব দ্বারা, নভেম্বর 18, 2015। আমি সবেমাত্র একটি দুর্দান্ত ডুয়ার্স স

The Default Query is:  ডুয়ার্স ভ্রমণের অভিজ্ঞতা

Press 1 for default query

Press 2 for custom query

Press 'Q'/'q' to exit: 1

Which retrieval algorithm do you want to use?

1.TFIDF without FAISS.

2.LSA without FAISS.

3.ESA without FAISS.

4.TFIDF with FAISS.

5.LSA with FAISS.

6.ESA with FAISS.

Please provide your choice of Algorithm or Press 'Q'/'q' to exit: 5

Provide the number of documents to be retrieved: 10

Facebook AI Similarity Search...

The retrieval model is FAISS LSA.

The retrieved documents are:

Document ID: 14016 Similarity Score : 0.3282

ডুয়ার্স পর্যটন দেখার জন্য সেরা 10টি মন্ত্রমুগ্ধকর স্থান ডুয়ার্সে ভ্রমণের সময় দেখার জন্য সেরা 10টি

Document ID: 14056 Similarity Score : 0.2532

ডোয়ার্স বক্সা চাপড়ামারী গোরুমরা জলদাপাড়া আলিপুরদুয়ার বিন্দু বীরপাড়া চালসা কোচবিহার গোরুবাথান জল

Document ID: 14092 Similarity Score : 0.2304

ডুয়ার্স ভারত ভারত ডুয়ার্স ডুয়ার্স ভারতে অবস্থিত ভূটান সংলগ্ন জনপ্রিয় একটি পর্যটন কেন্দ্র। ডুয়ার্স (D

Document ID: 14072 Similarity Score : 0.1714

বাংলার দুয়ারে বর্ষার বিরতি যদিও বর্ষাকালে জাতীয় উদ্যানগুলি বন্ধ থাকে, আপনি ডুয়ার্সে ছুটি কাটাতে ভ

Document ID: 14037 Similarity Score : 0.1518

লাটাগুড়ি গোরুমরা ট্যুর প্যাকেজ: গোরুমরা এক্সটেনসিভ ট্যুর 4N 5D আচ্ছাদিত স্থান: ডুয়ার্স - গোরুমরা ব

Document ID: 14113 Similarity Score : 0.1214

পশ্চিমবঙ্গের ঝালং বিন্দু ভ্রমণ 3রা অক্টোবর, 2018 ডুয়ার্স হল মনোরম সৌন্দর্যের কেন্দ্রবিন্দু এবং বিস্

Document ID: 14006 Similarity Score : 0.106

ঝালং বিন্দু জলঢাকা 24 আগস্ট, 2019 তারিখে পারদ দ্বারা জলঢাকা জল প্রকল্প নিয়ে ঝালং ও বিন্দু জুন মাসে

Document ID: 14099 Similarity Score : 0.1025

চাপড়ামারী NJP থেকে 60 কিমি দূরে অবস্থিত এবং হাতির জনসংখ্যার জন্য পরিচিত, চাপরামারি ডুয়ার্স অঞ্চলের

Document ID: 14177 Similarity Score : 0.0983

ডুয়ার্স ডুয়ার্সে একটি আকস্মিক তবুও স্মরণীয় ট্রিপ 23শে নভেম্বর 2017 যেহেতু আমরা সবাই এখন লকডাউনের

Document ID: 14103 Similarity Score : 0.0966

ডুয়ার্সে সামসিং ডুয়ার্সের সমতল ভূমির পাহাড়ি ঢাল এবং সবুজ বেল্টের মধ্য দিয়ে গড়িয়ে আপনাকে সামসিং

The Default Query is:  ডুয়ার্স ভ্রমণের অভিজ্ঞতা

Press 1 for default query

Press 2 for custom query

Press 'Q'/'q' to exit: q

(my_env) C:\Users\joyoj\OneDrive\Desktop\command_line_prototype>