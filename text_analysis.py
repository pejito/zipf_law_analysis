'''
This short amount of code is meant to simulate the text acquisition portion of a search engine by the following process: 

If a raw HTML page is given (with tags and everything):
    1. Intake an HTML page
    2. Strip it of tags
    3. Count the freqeuncy of words 
    4. Remove common words (such as 'the', 'a', 'an', 'of', etc.) 

Once step 4 has been completed, use the remaining words to perform Zipf's Law and Heap's Law.
'''


import numpy as np
import matplotlib.pyplot as plt
import io
import math
import zipfile
import re

def sort_dictionary(word_dict):
    lambda_func = lambda word_freq:word_freq[1]
    sorted_word_dict = {k:v for k,v in sorted(word_dict.items(), key = lambda_func, reverse=True)}
    return sorted_word_dict

def strip_tags(content):
    content = str(content)
    
    return content
    '''
    inside = 0
    text = ''
    
    if "<p>" in content: #Checking for <p> tag within the text; if none, start at the loop and process as normal
        start = content.find("<p>")
        end = content.rfind("<br/>")
        content = content[start:end]
    else:
        pass
        for char in content:
            if char == '<': 
                inside = 1
            elif (inside == 1 and char =='>'):
                inside = 0
            elif inside == 1:
                continue
            else:
                text += char
    print(text + '1')
    

    This doesn't have to be used anymore becauase the crawler group was able to return raw text documents! Thank y'all :)
    '''

def count_word_freq(content):
    word_list = content.split()
    word_freq = []
    for w in word_list:
        word_freq.append(word_list.count(w))
        print(w)
    word_freq_dict = sort_dictionary(dict(list(zip(word_list, word_freq))))
    return word_freq_dict

#Prob(r) = freq(r) / N [ frequency of a word / total number of words]
def zipf_law(word_freq_dict):
    r, Pr = 0, 0
    zipf_law_inter = []
    x = []
    y = []
    #zipf_law_value = []
    for word, freq in word_freq_dict.items():
        zipf_law_inter.append(freq)
        
    zipf_law_inter.insert(0,0) #Need to insert/pad a 0 into the 0 spot since lists are 0-indexed.
    sum_of_words = sum(zipf_law_inter)
    
    for i in range(1, len(zipf_law_inter) - 1 ): #Since the dict is sorted in a descending order already, the position in the list can be assumed to be the word's rank (starting from 0 to  n - 1).
        r = i
        Pr = zipf_law_inter[r] / sum_of_words
        #c = (r * Pr) / 100
        #zipf_law_value.append(c)
        x_axis_value = math.log(r)
        x.append(x_axis_value)
        y_axis_value = math.log(Pr)
        y.append(y_axis_value)
    
    x = np.asarray(x, dtype = float)
    y = np.asarray(y, dtype = float)
    return x, y

#instead of plotting r vs Pr, -> log(r) on x-axis // log(Prob(r)) on y-axis
def plot_zipf_law(x, y):
    plt.plot(x, y)
    plt.xlabel("Log(r)")
    plt.ylabel("Log(Probability(r))")
    plt.title("Zipf's law plot")
    plt.show()



def main():
    #count word frequency for each crawl, apply count_word_freq to all txt documents
    with open(r"C:\Users\ryanf\Desktop\SchoolStuff\CS4250\french.txt", "w", encoding="utf-8") as ff:
        with zipfile.ZipFile(r"C:\Users\ryanf\Downloads\repository fr.zip", "r") as z:
            for name in z.namelist():
                with io.TextIOWrapper(z.open(name), encoding="utf-8") as rf:
                    ff.write(rf.read())
                    
    with open(r"C:\Users\ryanf\Desktop\SchoolStuff\CS4250\french.txt", "r", encoding="utf-8") as final_file_inter:
        str = final_file_inter.read()
        new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', str)
        open(r"C:\Users\ryanf\Desktop\SchoolStuff\CS4250\french.txt", 'w').write(new_str)
        
    with open(r"C:\Users\ryanf\Desktop\SchoolStuff\CS4250\french.txt", "r", encoding="utf-8") as final_file:
        content = strip_tags(final_file.read())
        test_dict = count_word_freq(content)
        print(test_dict)
        x, y = zipf_law(test_dict)
        plot_zipf_law(x,y)

if __name__ == '__main__':
    main()

