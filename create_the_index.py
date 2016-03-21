

import sys
import re
from porterStemmer import PorterStemmer
from collections import defaultdict
from array import array
import gc
import math

porter=PorterStemmer()

class CreateIndex:

    def __init__(self):
        self.index=defaultdict(list)   
        self.titleIndex={}
        self.tf=defaultdict(list)          
                                                  
        self.df=defaultdict(int)       
        self.numDocuments=0

    
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def getTerms(self, line):
       
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) 
        line=line.split()
        line=[x for x in line if x not in self.sw]  
        line=[ porter.stem(word, 0, len(word)-1) for word in line]
        return line


    def parseCollection(self):
        
        doc=[]
        for line in self.collFile:
            if line=='</page>\n':
                break
            doc.append(line)
        
        curPage=''.join(doc)
        pageid=re.search('<id>(.*?)</id>', curPage, re.DOTALL)
        pagetitle=re.search('<title>(.*?)</title>', curPage, re.DOTALL)
        pagetext=re.search('<text>(.*?)</text>', curPage, re.DOTALL)
        
        if pageid==None or pagetitle==None or pagetext==None:
            return {}

        d={}
        d['id']=pageid.group(1)
        d['title']=pagetitle.group(1)
        d['text']=pagetext.group(1)

        return d


    def writeIndexToFile(self):
        
        #write main inverted index
        f=open(self.indexFile, 'w')
        #first line is the number of documents
        print >>f, self.numDocuments
        self.numDocuments=float(self.numDocuments)
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            #print data
            postingData=';'.join(postinglist)
            tfData=','.join(map(str,self.tf[term]))
            idfData='%.4f' % (self.numDocuments/self.df[term])
            print >> f, '|'.join((term, postingData, tfData, idfData))
        f.close()
        
        #write title index
        f=open(self.titleIndexFile,'w')
        for pageid, title in self.titleIndex.iteritems():
            print >> f, pageid, title
        f.close()
        

    def getParams(self):
       
        param=sys.argv
        self.stopwordsFile=param[1]
        self.collectionFile=param[2]
        self.indexFile=param[3]
        self.titleIndexFile=param[4]
        

    def createIndex(self):
        
        self.getParams()
        self.collFile=open(self.collectionFile,'r')
        self.getStopwords()
                
        #bug in python garbage collector!
        #appending to list becomes O(N) instead of O(1) as the size grows if gc is enabled.
        gc.disable()
        
        pagedict={}
        pagedict=self.parseCollection()
        #main loop creating the index
        while pagedict != {}:                    
            lines='\n'.join((pagedict['title'],pagedict['text']))
            pageid=int(pagedict['id'])
            terms=self.getTerms(lines)
            
            self.titleIndex[pagedict['id']]=pagedict['title']
            
            self.numDocuments+=1
            
            #build the index for the current page
            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]
            
            #normalize the document vector
            norm=0
            for term, posting in termdictPage.iteritems():
                norm+=len(posting[1])**2
            norm=math.sqrt(norm)
            
            #calculate the tf and df weights
            for term, posting in termdictPage.iteritems():
                self.tf[term].append('%.4f' % (len(posting[1])/norm))
                self.df[term]+=1
            
            #merge the current page index with the main index
            for termPage, postingPage in termdictPage.iteritems():
                self.index[termPage].append(postingPage)
            
            pagedict=self.parseCollection()


        gc.enable()
            
        self.writeIndexToFile()
        
    
if __name__=="__main__":
    c=CreateIndex()
    c.createIndex()
    

