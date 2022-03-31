import nltk
# from nltk.tokenize import word_tokenize
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
# from nltk.stem import PorterStemmer
import gensim
import string
from gensim.parsing.preprocessing import STOPWORDS
nltk.download('punkt')
all_stopwords = gensim.parsing.preprocessing.STOPWORDS
all_stopwords_gensim = STOPWORDS.union(set([
'add','insert','update','delete','remove','fix','modify','updating','inserting',
',','.','version','master','create','#','(',')',"'",':','cc','-','--','<','>','{','}',
'updates','updated','changes','adding',"''","``",'release','allow','[',']','//',
'bump','build','@','use','docs','`','/','support','ref','added','view','test','data']))
# ps = PorterStemmer()
nltk.download('wordnet')
def text_cleaning(a):
 a = a.lower()
 lemmatizer = WordNetLemmatizer()
 remove_punctuation = [char for char in a if char not in string.punctuation]
 #print(remove_punctuation)
 remove_punctuation=''.join(remove_punctuation)
 #print(remove_punctuation)   
 return [lemmatizer.lemmatize(word) for word in remove_punctuation.split() if word.lower() not in all_stopwords_gensim]
# text_cleaning("Programmers program with programming languages!")
# print(text_cleaning("prahar Pandya"))