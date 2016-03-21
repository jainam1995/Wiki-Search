# Wiki-Search
---

###An offline mini search engine for Wikipedia pages.

The collection of data being used is a 16GB dump of wikipedia pages.The tf-idf meathod is used for indexing. Three types of search queries are entertained :  
* One word query : Displays pages that have that word, ranked according to tf-idf.  
* Full text search : Displays pages that have any of that word, ranked according to tf-idf.  
* Pattern search : Displays pages that have the words in that order, ranked according to tf-idf. Enclose the seach query within " " in this case.

---

#####Create index on the Wiki pages :  
`python create_the_index.py stopwords.txt collection.txt indexfile.txt titleindex.txt`  

#####Searching in the document list :  
`python index_the_query.py stopwords.txt indexfile.txt titleindex.txt`  


 Now type the search query. a ranked list of document titles will appear !!   
