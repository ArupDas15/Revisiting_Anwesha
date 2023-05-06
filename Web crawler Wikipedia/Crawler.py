from googletrans import Translator
import wikipedia
import os
from datetime import date
import warnings
warnings.filterwarnings('ignore')

class Crawler:
	def __init__(self):
  		self.related_links = []
  		self.actual_query = ""
  		self.crawled_num_of_articles = 0
  		self.required_num_of_articles = 0

	def ben_to_eng(self,text):
		try:
		    translator = Translator()
		    text = translator.translate(text, dest='en').text
		    return text
		except:
			print(text)
			pass

	def eng_to_ben(self,text):
		try:
			translator = Translator()
			text = translator.translate(text, dest='bn').text
			return text
		except:
			print(text)
			pass

	def is_bengali(self,text):
	    # loop through each character in the text
	    for char in text:
	        # check if the Unicode value of the character is in the Bengali range
	        if ord(char) >= 0x0980 and ord(char) <= 0x09FF:
	            return True
	    return False

	def is_english(self,text):
	    # loop through each character in the text
	    for char in text:
	        # check if the Unicode value of the character is in the Basic Latin or Latin-1 Supplement range
	        if (ord(char) >= 0x0000 and ord(char) <= 0x007F) or \
	           (ord(char) >= 0x0080 and ord(char) <= 0x00FF):
	            continue
	        else:
	            return False
	    return True

	def save_article(self, title, content, lang):
		if lang == 'en':
			title = self.eng_to_ben(title)
			content = self.eng_to_ben(content)

		print(title)
		folder_name = self.actual_query.upper().replace(' ', '_')
		if not os.path.exists('database'):
		    os.mkdir('database')
		if not os.path.exists(os.path.join('database', folder_name)):
		    os.mkdir(os.path.join('database', folder_name))
		if not os.path.exists(os.path.join('database', folder_name, 'CRAWLED_DATA')):
		    os.mkdir(os.path.join('database', folder_name, 'CRAWLED_DATA'))

		file_name = os.path.join('database', folder_name, 'CRAWLED_DATA', f'{title}_{date.today()}.txt')
		with open(file_name, 'w', encoding='utf-8') as file:
			file.write(content)

		self.crawled_num_of_articles += 1

	def search_wikipedia(self,terms,lang):
		try:
			wikipedia.set_lang(lang)
			while terms:
				if self.crawled_num_of_articles >= self.required_num_of_articles:
					print("Required number of articles are crawled!")
					return
				query = terms.pop(0)
				try:
					page = wikipedia.page(query)
				except wikipedia.exceptions.DisambiguationError as e:
					for option in e.options:
						terms.append(option)
					continue

				except: continue

				# print the title and summary of the page
				title = page.title
				if lang == 'bn':
					content = page.content
				else:
					content = page.summary
				self.save_article(title,content,lang)
		except: pass



	def crawl(self,query,num_of_articles=10):
		self.actual_query = query
		self.required_num_of_articles = num_of_articles

		query = self.eng_to_ben(query)
		wikipedia.set_lang('bn')
		related_terms = list(wikipedia.search(query, results=self.required_num_of_articles))
		self.search_wikipedia(related_terms,'bn')

		query = self.ben_to_eng(query)
		wikipedia.set_lang('en')
		related_terms = list(wikipedia.search(query, results=self.required_num_of_articles-self.crawled_num_of_articles))
		self.search_wikipedia(related_terms,'en')

if __name__=='__main__':
	file = open("search_query.txt","r", encoding='utf-8',errors='ignore')
	query = file.readline()
	file.close()
	if not query: print("Please enter keywords in 'search_query.txt' file.")
	else:
		num_of_articles = int(input("Enter number of articles to be retrieved: "))
		c = Crawler()
		c.crawl(query,num_of_articles)