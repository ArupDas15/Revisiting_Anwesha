# AutoCompletion of Words module for Bangla Search Engine

In this module provided the English transliteration of Bangla Word prefix, top 12 Bangla autocompleted words are suggested.

## Installation Steps

### Requirements (Python+Java)

1. Install Python version 3.11.1.

2. Install Java version 19.0.1.

### Python Libraries for Connection

Install "jnius_config" and "jnius" libraries of python. Run the below commands in the command prompt for installation.

```
pip install jnius_config
```
and 
```
pip install jnius
```

## Guide to Run

Run the below commands to compile the Java source code.

```
mkdir out
javac -d out -encoding utf-8 src/*.java
```

After the successful compilation and creation of Java classes run the below Python command to run the application.

```
python Main_python.py
```

## Output 

Output will be similar to the below code snippet. 

```
Enter the input word (Type 'Q' to Stop): am
আমরা
আমাদের
আমি
আমার
আমাকে
আমেরিকা
আমল
আমরি
আমন্ত্রণ
আমদানি
আমলে
আম

Enter the input word (Type 'Q' to Stop): amr
আমরা
আমরি
আমরাও
আমরাই
আমরির
আমরণ
আমরিতে
আমর
আমরুল
আমরে
আমরক্ত
আম্র

Enter the input word (Type 'Q' to Stop): Q
```

Press 'Q' to stop running the application.

## Reference

The source code is inspired and modified from https://github.com/reyadussalahin/Smart-Autocompletion-of-Bangla-Word
