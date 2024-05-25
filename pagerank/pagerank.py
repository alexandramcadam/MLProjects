import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents) 
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    pages = list(corpus.keys()) #list of pages
    links = list(corpus[page]) #list of links from given page
    
    #create probability distribution dictionary
    pd = {}
    for page in pages:
        pd.update({page:0})

    if len(links) != 0:

        prob1 = damping_factor * 1/len(links) #randomly choose link from page
        for link in links:
            pd[link] = prob1
        
        prob2 = (1 - damping_factor)/len(pages) #randomly choose any page
        for page in pages:
            pd[page] = pd[page] + prob2

        
    else: #no links, equal probability among all pages
    
        for page in pages:
            pd[page] = 1/len(pages) #equal prob among pages, same as prob1 + prob2

    return pd



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pages = list(corpus.keys())
    page = random.choice(pages) #choose random page to start 
    
    samples = [] #markov chain 
    
    for i in range(n): #remaining samples choose using transition model 
        samples.append(page)
        tm = transition_model(corpus, page, damping_factor)
        weights = list(tm.values())
        page = random.choices(pages, weights=weights)[0] #returns a list of 1
        
        
    ranks = {}
    for page in pages:
        counter = 0
        for sample in samples:
            if sample == page:
                counter +=1
        pr = counter/n
        ranks.update({page:pr})
        
    return ranks 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pages = list(corpus.keys())
    
    #fix corpus for pages with no outgoing links 
    for x in corpus:
        if len(corpus[x]) == 0:
            corpus[x] = set(pages) #set to link to all pages 

    
    ranks = {}
    pr = 1/len(pages) #set default pagerank all equal 
    for page in pages:
        ranks.update({page:pr})
        
    #iteration algorithm 
    converge = False
    while converge==False:
    
        oldranks = ranks.copy()
        for page in pages:
            prob1 = (1-damping_factor)/len(pages) #choosing random page 
            
            #calculate prob2
            inlinks = [] #find incoming links to page
            for x in corpus:
                if page in corpus[x]: 
                    inlinks.append(x)

            sum=0
            for link in inlinks:
                numlinks = len(corpus[link])        
                sum+=oldranks[link]/numlinks
                
            prob2 = damping_factor*sum
            
            pr = prob1 + prob2
            ranks[page]=pr #update pageranks 


        #check if converged 
        counter = 0
        for page in pages:
            difference = abs(oldranks[page] - ranks[page])
            if difference < 0.001: 
                counter+=1
        if counter == len(pages): #all converged
            converge = True
             
    
    return ranks    


if __name__ == "__main__":
    main()
