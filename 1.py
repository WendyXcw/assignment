import whoosh
from whoosh.fields import *

#import dataset
from sklearn.datasets import fetch_20newsgroup
dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('header','footers','quotes'))
documents = dataset.data
print(documents.target_names)

#tokenization
import pandas as pd
news_df = pd.DataFrame({'document':documents})

# removing everything except alphabets
news_df['clean_doc'] = news_df['document'].str.replace("[^a-zA-Z#]", " ")
# removing short words
news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
# make all the lowercase
news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: x.lower())

#texts = news_df['clean_doc']




#Define the schema of your index, which specifies the fields of documents in the index
#Read more: https://whoosh.readthedocs.io/en/latest/schema.html
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
#Creating your Index object in a directory, following schema defined above. 
#Here we save the Index object in a subfolder named 'indexdir' in your working directory
ix = create_in(".", schema)
#Once your Index object is ready, you can add documents to the index using IndexWriter
writer = ix.writer()
for i in range(len(texts)):
print ("adding document "+str(i))
writer.add_document(title=u"document "+str(i), path=u".",content=texts[i]) #python iterator i starting from 0
#Calling commit() on the IndexWriter after adding all documents and it will update the index
writer.commit(optimize=True)
#So far you have defined a schema, created an Index object, and added some documents. Following we will try search
using the index
#similar to adding document using writer, you need to create a searcher object to search
searcher = ix.searcher()
#The Searcher needs a Query object, you can construct a query use QueryParser to parse a string.
parser = QueryParser("content", ix.schema)
stringquery = parser.parse("word")
results = searcher.search(stringquery)
print ("search 1 result:")
print (results)
for r in results:
print (r)
#Or you can construct more complicated query like this one below:
from whoosh.query import *
myquery = Or([Term("content", u"word"), Term("content", "world")])
results2 = searcher.search(myquery)
print ("search 2 result:")
print (results2)
for r in results2:
print (r)


