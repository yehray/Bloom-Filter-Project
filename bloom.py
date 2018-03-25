
import argparse
import bfProjectUtils as util
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt

class HashType1(object):
    #Implement Hash Type 2
    def __init__(self, config, genHashes):
        self.k = config['k']
        self.n = config['n']
        self.seeds = []
        #set random seed to be generated seed at config load
        # random.seed(config['genSeed'])
        #if generate new random hashes
        if genHashes :
            #build seed list self.seeds
            for i in range(0,self.k):
                si = random.randint(0, config['N'])
                self.seeds.append(si)
        #if not gen (task 2), then use hashes that are in config dictionary
        else :
            self.seeds = config['seeds']
    
    def getHashList(self, x):
        res = []
        for i in range(0,self.k):
            random.seed(np.int64(self.seeds[i] + x))
            res.append(random.randint(0, self.n - 1))
        #your code goes here
        return res


class HashType2(object):
    #Implement Hash Type 2

    def __init__(self, config, genHashes):
        self.k = config['k']
        self.n = config['n']
        self.N = config['N']
        self.prime = util.findNextPrime(self.n)
        self.NPrime = util.findNextPrime(self.N)
        #generate new random hashes, or not if task2
        if genHashes :
            #set random seed to be generated seed at config load
            # random.seed(config['genSeed'])
            #build lists of coefficients self.a and self.b
            a = []
            b = []
            for i in range(0,self.k):
                a.append(random.randint(1, self.n - 1))
                b.append(random.randint(0, self.n - 1))
            self.a = a
            self.b = b
        #if not gen (task 2), then use hashes that are in config dictionary
        else :
            self.a = config['a']
            self.b = config['b']           
            
            
    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using 
        (self.a[i] * x + self.b[i] mod P) mod n 
        to give i'th hash value.

        """
        res = []
        for i in range(0,self.k):
            res.append(long(((self.a[i]*x + self.b[i]) % self.NPrime) % self.prime))
        return res
    
    


class BloomFilter(object):     
    def __init__(self, config):
        """        
        Args:
            config (dictionary): Configuration of this bloom filter
            config['N'] (int) universe size
            config['m'] (int) number of elements to add to filter
            config['n'] (int) number of bits in bloom filter storage array
            config['k'] (int) number of hash functions to use
            config['task'] (int) the task this bloom filter is to perform (1,2,3)
            config['type'] (int) type of hash function (1, 2, -1==unknown type)
            if type 1 hash :
                config['seeds'] (list of k ints) : seed values for k hash functions for type 1 hash function
            if type 2 hash : 
                config['a'] (list of k ints) : a coefficients for k hash functions for type 2 hash function
                config['b'] (list of k ints) : b coefficients for k hash functions for type 2 hash function
            
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """
        #task this boom filter is performing
        self.task = config['task']
        #task 1 requires generated seeds for hashes, task 2 uses provided seeds/coefficients
        genHashes = (self.task != 2)
        #type of hash for this bloom filter
        self.type = config['type']
        if(self.type == 1):
            self.hashFunc = HashType1(config,genHashes)
        elif(self.type == 2):
            self.hashFunc = HashType2(config,genHashes)
        else:
            print('BloomFilter for task ' + str(self.task) + ' ctor : Unknown Hash type : ' + str(self.type))
        self.hashTable = [0]*config['n']


    def add(self, x):
        # Adds x to the data structure, using self.hashFunc     
        addVal = self.hashFunc.getHashList(x)
        for i in addVal:
            self.hashTable[i] = 1
        pass
    

    def contains(self, x):
        # Indicates whether data structure contains x, using self.hashFunc, with the possibility of false positives
        retVal = True
        addVal = self.hashFunc.getHashList(x)
        for i in addVal:
            if self.hashTable[i] == 0:
                retVal = False
        
        return retVal


"""
function will take data list, insert first m elements into bloom filter, and check all elements in datalist for membership, returning a list of results of check  
"""
def testBF(data, bf, m):
    #add first m elements
    for i in range(0,m):
        bf.add(data[i]) 
    print('Finished adding '+ str(m) +' integers to bloom filter')
    resList =[]
    #test membership of all elements
    for i in range(0,len(data)):
        resList.append(str(bf.contains(data[i])))
    return resList


"""
function will support required test for Task 2.  
"""
def task2(configData):        
    #instantiate bloom filter object    
    bf = BloomFilter(configData)

    #bfInputData holds a list of integers.  Using these values you must :
    #   insert the first configData['m'] of them into the bloom filter
    #   test all of them for membership in the bloom filter
    bfInputData = util.readIntFileDat(configData['inFileName'])

    if(len(bfInputData) == 0):
        print('No Data to add to bloom filter')
        return
    else :
        print('bfInputData has '+str(len(bfInputData)) +' elements')
    #testBF will insert elements and test membership
    outputResList = testBF(bfInputData, bf, configData['m'])            
    #write results to output file
    util.writeFileDat(configData['outFileName'],outputResList)
    #load appropriate validation data list for this hash function and compare to results    
    util.compareResults(outputResList,configData)    
    print('Task 2 complete')    

# Plot results for task 1
def task1(configData):
    bfInputData = util.readIntFileDat(configData['inFileName'])
    ht1 = HashType1(configData, True)
    ht2 = HashType2(configData, True)
    ht1.k = 1
    ht2.k = 1
    ht1list = []
    ht2list = []
    x = bfInputData[:10000]
    for i in range(0,10000):
        ht1list.append(ht1.getHashList(bfInputData[i]))
        ht2list.append(ht2.getHashList(bfInputData[i]))

    plt.scatter(x, ht1list, marker = '.', s = 1)
    plt.axis((0,max(x),0,max(ht1list)[0]))
    plt.title('Type 1 Hash Function Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    plt.scatter(x, ht2list, marker = '.', s = 1)
    plt.axis((0,max(x),0,max(ht2list)[0]))
    plt.title('Type 2 Hash Function Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    ht1list = []
    ht2list = []
    x = []
    for i in range(0,20000):
        if bfInputData[i]%2 == 0:
            x.append(bfInputData[i])
            ht1list.append(ht1.getHashList(bfInputData[i]))
            ht2list.append(ht2.getHashList(bfInputData[i]))

    plt.scatter(x, ht1list, marker = '.', s = 1)
    plt.axis((0,max(x),0,max(ht1list)[0]))
    plt.title('Type 1 Hash Function Even Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    plt.scatter(x, ht2list, marker = '.', s = 1)
    plt.axis((0,max(x),0,max(ht2list)[0]))
    plt.title('Type 2 Hash Function Even Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    print('Task 1 complete')

# Plot results for task 3
def task3(configData):
    configData['task'] = 3
    numTrials = 10
    kVals10 = [4,5,6,7,8,9,10]
    kVals15 = [6,7,8,9,10,11,12,13,14,15]
    c10Type1 = []
    c10Type2 = []
    c15Type1 = []
    c15Type2 = []
    c10equation = []
    c15equation = []

    # calculate theoretical false positive rate when c = 10
    for i in kVals10:
        c10equation.append((1 - np.exp(-(i/10.0)))**i)
    # calculate theoretical false positive rate when c = 15
    for i in kVals15:
        c15equation.append((1 - np.exp(-(i/15.0)))**i)

    # test c = 10 for Type 1
    print('Testing c = 10 Type 1 hash...')
    c = 10
    hashType = 1
    for i in kVals10:
        c10Type1.append(computeFalsePositive(configData, numTrials, i, c, hashType))
    # test c = 10 for Type 2
    print('Testing c = 10 Type 2 hash...')
    hashType = 2
    for i in kVals10:
        c10Type2.append(computeFalsePositive(configData, numTrials, i, c, hashType))
    # test c = 15 for Type 1
    print('Testing c = 15 Type 1 hash...')
    c = 15
    hashType = 1
    for i in kVals15:
        c15Type1.append(computeFalsePositive(configData, numTrials, i, c, hashType))
    # test c = 15 for Type 2
    print('Testing c = 15 Type 2 hash...')
    hashType = 2
    for i in kVals15:
        c15Type2.append(computeFalsePositive(configData, numTrials, i, c, hashType))


    # generate plots
    fig = plt.figure()
    c10Type1Plot, = plt.plot(kVals10, c10equation, label='Theoretical False Positive Rate')
    kVals10Plot, = plt.plot(kVals10, c10Type1, label='False Positive Rate')
    plt.title('c = 10, Type 1 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c10Type1Plot, kVals10Plot], ['Theoretical False Positive Rate', 'False Positive Rate'])
    fig.savefig('c10Type1')

    fig = plt.figure()
    c10Type2Plot, = plt.plot(kVals10, c10equation, label='Theoretical Positive Rate')
    kVals10Plot, = plt.plot(kVals10, c10Type2, label='False Positive Rate')
    plt.title('c = 10, Type 2 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c10Type2Plot, kVals10Plot], ['Theoretical False Positive Rate', 'False Positive Rate'])
    fig.savefig('c10Type2')

    fig = plt.figure()
    c15Type1Plot, = plt.plot(kVals15, c15equation, label='Theoretical False Positive Rate')
    kVals15Plot, = plt.plot(kVals15, c15Type1, label='False Positive Rate')
    plt.title('c = 15, Type 1 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c15Type1Plot, kVals15Plot], ['Theoretical False Positive Rate', 'False Positive Rate'])
    fig.savefig('c15Type1')

    fig = plt.figure()
    c10Type2Plot, = plt.plot(kVals15, c15equation, label='Theoretical False Positive Rate')
    kVals15Plot, = plt.plot(kVals15, c15Type2, label='False Positive Rate')
    plt.title('c = 15, Type 2 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c10Type2Plot, kVals15Plot], ['Theoretical False Positive Rate', 'False Positive Rate'])
    fig.savefig('c15Type2')

    print('Task 3 complete')

def computeFalsePositive(configData, numTrials, k, c, hashType):
    configData['k'] = k
    configData['type'] = hashType
    configData['n'] = util.findNextPrime(c*configData['m'])
    sumFalsePositive = 0
    for i in range(0,numTrials):
        # initialize bloom filter
        bf = BloomFilter(configData)
        bfInputData = util.readIntFileDat(configData['inFileName'])
        # add data to bloom filter
        for j in range(0,configData['m']):
            bf.add(bfInputData[j])
        falsePositive = 0
        #test false positive
        for l in range(configData['m'],len(bfInputData)):
            if bf.contains(bfInputData[l]):
                falsePositive += 1
        sumFalsePositive += falsePositive/float(configData['m'])
    avgFalsePositive = sumFalsePositive/numTrials
    return avgFalsePositive
    

"""     
main
"""     
def main():	
    parser = argparse.ArgumentParser(description='BloomFilter Project')
    parser.add_argument('-c', '--configfile',  help='File holding configuration of Bloom Filter', default='testConfigHashType1.txt', dest='configFileName')
    parser.add_argument('-i', '--infile',  help='Input file of data to add to Bloom Filter', default='testInput.txt', dest='inFileName')
    parser.add_argument('-o', '--outfile',  help='Output file holding Bloom Filter results', default='testOutput.txt', dest='outFileName')	
    parser.add_argument('-t', '--task',  help='Which task to perform (1,2,3)', type=int, choices=[1, 2, 3], default=2, dest='taskToDo')
    parser.add_argument('-v', '--valfile',  help='Validation file holding Bloom Filter expected results', default='validResHashType1.txt', dest='valFileName')
    
    args = parser.parse_args()
        
    configData = util.buildBFConfigStruct(args)
    
    if configData['task'] == 2 :
        task2(configData)
    elif configData['task'] == 1 :
        task1(configData)
    elif configData['task'] == 3 :
        task3(configData)
    else :
        print ('Unknown Task : ' + str(configData['task']))  

if __name__ == '__main__':
    main()
    