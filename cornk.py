from datetime import date
import numpy as np
from numpy.lib import corrcoef
import pandas as pd
from matplotlib import pyplot as plt
from stockMarketReader import readDataSet

# Need to construct a set of experts as required by CORN
class Expert:
    """
    This class serves the purpose of making a CORN expert
    """

    #constructor for this expert with the two noteworthy parameters
    def __init__(self, windowSize, corrThresh, numStocks, numDays):
        """
        Initialisation of a CORN expert with its unique parameters:
        the window size, the correlation threshold.
        Standard parameters being number of stocks and number of days.
        """
        self.windowSize = windowSize
        self.corrThresh = corrThresh
        self.corrSimSet = None
        self.numStocks = numStocks
        self.weight = 0
        # initial wealth as based on page 12 note
        self.wealthAchieved = 1
        self.currPort = None
        self.portHistory = np.empty((numStocks, numDays))
        
    def updateWeight(self, numExperts):
        """
        Update this agent's weight to be 1/numExperts as it is part of top-numExperts (K)
        """
        self.weight = 1 / numExperts

    def assignCorrSet(self, corrSet):
        """
        A function that allows us to add a correlation similar set to this specific expert - should it be needed.
        It will most likely not be needed given that this changes frequently.
        """
        self.corrSimSet = corrSet
    
    def addPort(self, portfolio, day):
        """
        A way to track past portfolios should it be needed.
        In reality this is not really going to be needed given that we can track the wealth and increase the wealth.
        """
        for i in range(self.numStocks):
            self.portHistory[day][i] = portfolio[i]
    
    def increaseWealth(self, priceVector):
        """
        Function that given a portfolio and a price relative vector will increase the agent's wealth using it.
        Note that this is meant to take in the day's (i.e at time t) price relative vector.
        """
        temp = 0
        for i in range(self.numStocks):
            temp += self.currPort[i]*priceVector[i]
        # need to set a self wealth for each specific agent
        self.wealthAchieved = self.wealthAchieved * temp

def getUniformPort():
    """
    Generate a uniform portfolio given a number of stocks.
    """
    stocks = np.ones((numStocks))
    return stocks / numStocks

def expertLearn(window, corrThresh, day, data):
    """
    Preform algorithm 1 from CORN paper.
    This algorithm is the expert learning procedure.
    Given an index date (day), the window (a specified window size), the histMarketWind (t-1 to 1) and the corrThresh which is rho our correlation coeff threshold.
    """
    corrSimSet = np.array(())
    if day <= window + 1:
        #works
        return getUniformPort()
    else:
        #check out
        for i in range(window + 1,day): #just check that this works otherwise change it to t
            # print("Test 1")
            # print("size of window: " + str(window))
            # print("I-window: " + str(i-window) + " , i-1: " + str(i-1))
            # print(data.shape)
            markWindI = marketWindow(i-window, i-1, dates, data)
            # print("Test 2")
            # print("day-window: " + str(day-window) + " , day-1: " + str(day-1))
            markWindT = marketWindow(day - window, day - 1, dates, data)
            # print("Test 3")
            # check at some point to ensure that this captures the standard deviation for the whole window (i.e output not something weird)
            # flattened just to ensure that this does happen
            pearsonCor = -1
            if np.std(markWindI.flatten()) == 0 or np.std(markWindT.flatten()) == 0:
                print("Recognised a 0 standard deviation in a market window")
                pearsonCor = 0
            # print("Test 4")
            # may need to change this to the exact calculation they use in the formula
            if pearsonCor != 0:
                pearsonCor = np.cov(markWindI, markWindT) / (np.std(markWindI.flatten()) * np.std(markWindT.flatten()) )
                # print("Test 5")
            elif  pearsonCor >= corrThresh:
                print("Appended a set")
                # append this to our set i.e add the index
                corrSimSet = np.append(corrSimSet,i)
            # print("Test 6")
    if len(corrSimSet) == 0:
        print("Empty set")
        return getUniformPort()
    else:
        # Search for the optimal portfolio
        # so using the i in the set, get the argmax
        # from what I understand, we need the price relative vector at time i, find the stock that gave the best return and all in on that stock
        tempRelative = 0
        port = np.zeros((numStocks))
        for i in corrSimSet:
            # get the price relative vector for the day
            priceRelative = dayReturn(i,dates,data)
            # index of maximum change 
            # day = dayReturn(i,dates,data)
            # day = day.reshape((numStocks,1))
            dayVal = np.argmax(day)
            if day == -1:
                print("Error occurred at day " + str(i))
            else:
                if tempRelative < day:
                    tempRelative = day
                    port = np.zeros((numStocks))
                    port[np.argmax(day,axis=0)] = 1
        print("WAS ABLE TO FIND AN OPTIMAL PORT")
        return port
        
def dayReturn(day, dates, data):
    """
    Given a day, the dates and a dataframe.
    Get stock market data for the given day - organise it vertically.
    TODO CHECK THAT THIS WORKS
    NOTE data here is the newly created price relative matrix for market history
    """
    day = int(day)
    if day != 0:
            # yesterdayReturn = data[data['Date'] == dates[day-1]]
            # yesterdayReturn = yesterdayReturn.Close.to_numpy()
            # todayReturn = data[data['Date'] == dates[day]]
            # todayReturn = todayReturn.Close.to_numpy()
            # todayReturn = todayReturn / yesterdayReturn
            # return todayReturn.reshape(len(todayReturn),1)
            # want a column for day before so
            # since already encoded in this format
            # print(data.shape)
            todayReturn = np.zeros((numStocks))
            # print(todayReturn.shape)
            # print(data.shape)
            try:
                for x in range(numStocks):
                    # print("X IS : " + str(x))
                    # print("TODAY RETURN AT " + str(todayReturn[x]))
                    todayReturn[x] = data[x][day]
                    # print("TODAY RETURN AT " + str(todayReturn[x]))
                return todayReturn
            except:
                print(data.shape)
                print(day)
                print(data[:][day])
                input()
    else:
        # Find number of stocks and then return 1 for each
        # startDate = data[data['Date'] == dates[0]]
        # tickers = np.unique(startDate.Ticker.to_numpy())
        numOfStocks =  data.shape[0]
        return np.ones((numOfStocks))


def getDatesVec(data):
    """
    Get the vector of dates that spans a given stock market data set - specifically done for CORN algorithm but not exclusive to it
    note that this requires the pandas dataframe of data
    NOTE pandas dataframe for data
    """
    startDate = data.Date.min()
    startDate = data[data['Date'] == startDate]
    startDate = startDate.Ticker.to_numpy()
    tick = np.unique(startDate)[0]
    tickerDates = data[data['Ticker'] == tick]
    tickerDates = np.unique(data.Date.to_numpy())
    return tickerDates

def cornDataRead():
    name = input("Name of data set\n")
    if name == "BIS":
        return np.loadtxt("BISPRICERELATIVES.txt")
    elif name == "BOV":
        return np.loadtxt("BOVPRICERELATIVES.txt")
    elif name == "EUR":
        return np.loadtxt("EURPRICERELATIVES.txt")
    elif name == "JSE":
        return np.loadtxt("JSEPRICERELATIVES.txt")
    elif name == "NAS":
        return np.loadtxt("NASPRICERELATIVES.txt")
    elif name == "SP5":
        return np.loadtxt("SP5PRICERELATIVES.txt")
    else:
        print("ERROR INPUT CORRECT NAME")
        return cornDataRead()

# does not rely on using pandas dataframe
def generateHistoricalMarket(data, dates, numStocks):
    """
    Function to generate a set of historical price relative vectors.
    Given a data set, the dates as a numpy array and the number of stocks in the data set.
    """
    print(len(dates))
    relatives = np.empty((numStocks, len(dates)))
    initalDay = np.ones((numStocks))
    relatives[:,0] = initalDay
    numErrors = 0
    errorDays = np.array(())
    for i in range(1,len(dates)):
        try:
            marketToday = data[data['Date'] == dates[i]]
            marketYesterday = data[data['Date'] == dates[i-1]]
            change = marketToday.Close.to_numpy()/marketYesterday.Close.to_numpy()
            change = change.reshape(numStocks)
            relatives[:,i] = change
            if i % 100 == 0:
                percent = i/len(dates)
                statement = "Percentage: " + str(percent*100) + "%, number of errors: " + str(numErrors)
                print(statement)
        except:
            numErrors += 1
            errorDays = np.append(errorDays, i)
            #acknowledge where errors occured we appeneded a 1's array
            relatives[:,i] = np.ones((numStocks))
    for i in errorDays:
        print("Error at day: " +str(i))
    print(numErrors)
    name = "SP5PRICERELATIVES.txt"
    print("Saving data as " + name)
    np.savetxt(name,relatives)
    print("Saved")
    content = np.loadtxt(name)
    print("Length of saved item was as follows(numStocks,length):" + str(relatives.shape))
    print("Loaded")
    print("Shape " + str(content.shape))
    return relatives

# relies on using day return a few times
def marketWindow(startDate, endDate, dates, data):
    """
    Return a market window from t-w to t-1 (inclusive of endpoints) therefore w in width.
    startDate is the index to start on.
    endDate is the index to end on.
    dates contains a vector of dates in the data.
    data is a capture of the data set.
    """
    # Finding out the length of the stocks is useful here
    width = endDate - startDate + 1
    # Make a window that can contain all stocks
    if(width != 1):
        market = np.empty((numStocks,width))
        count = 0
        for i in range(startDate, endDate + 1):
            window = dayReturn(i,dates,data)
            # print(window)
            for j in range(numStocks):
                market[j][count] = window[j]
            count += 1
        return market
    else:
        return dayReturn(endDate,dates,data)

# only relies on dayReturn for the use of data
def calcReturns(portfolios, dates, data, initialCapital = 1):
    """
    Function which generates returns given an initial portfolio.
    Portfolios need to be a matrix that is the width of the number of tradingdays(individual portfolios), length of the number of stocks - which describe how the portfolio looks.
    Each portfolio must be simplex, so they each are a value greater than or equal to zero, and their values sum to 1.
    """
    returns = np.array(())
    for i in range(len(dates)):
        day = dayReturn(i, dates, data)
        val = 0
        for j in range(numStocks):
            val += portfolios[i][j] * day[j]
        returns = np.append(returns, val)
    return initialCapital * returns

def initExperts(windowSize, numStocks, P):
    """
    Initialise all the experts. 
    Given a windowSize(max) assign some to each.
    For a number of stocks that are given by the tickers.
    For P where we will figure out our correlation.
    """

    # init W*P experts
    experts = []
    for i in range(0,windowSize-1):
        for j in range(P):
            # __init__(self, windowSize, corrThresh, numStocks, numDays):
            expert = Expert(i,j/P, numStocks, len(dates))
            experts.append(expert)
    return experts

def printExperts(experts, windowSize, P):
    """
    Function to print the experts.
    Pay attention to the indexing, since a 0 window does not make sense it feels
    """
    for i in range(0,windowSize-1):
        for j in range(0,P):
            print("Expert at " + str(i*(windowSize-1) + j) +" with characteristics:"+str(experts[i*(windowSize-1) +j].windowSize) + "," + str(experts[i*(windowSize-1) +j].corrThresh))

def findTopK(experts):
    """
    Function to find the top-K experts.
    Based on a chosen K
    An array of the indices of where the best elements occurred) NOTE THAT THIS WILL BE A FLATTENED ARRAY
    """
    expertsWealth = np.empty((windowSize-1,P))
    for i in range(windowSize-1):
        for j in range(P):
            expertsWealth[i][j] = experts[i*(windowSize-1) + j].wealthAchieved
            print(experts[i*(windowSize-1) + j].wealthAchieved)
            print(expertsWealth)
    indicesBest = np.array(())
    # need to flatten to be able to use delete
    expertsWealth = expertsWealth.flatten()
    for i in range(K):
        currBest = np.argmax(expertsWealth)
        indicesBest = np.append(indicesBest, currBest)
        # Create a sentinel value to ignore
        expertsWealth[currBest] = -999
    return indicesBest

# No reliance on dataframe data
def runCorn(dates, data, windowSize, P):
    """
    Run the CORN-K algorithm on the data set
    TODO CHANGE THIS TO WORK WITH THE NEW EXPERT ARRAY AND HOW IT IS A FLAT ARRAY
    """
    portfolioHist = np.array((numStocks,len(dates)))
    # create experts which a 1D array
    experts = initExperts(windowSize,numStocks,P)
    # going downwards window size increases, going rightwards the corrThresh increases
    totError = 0
    windowError = np.zeros((windowSize-1))
    corrThreshError = np.zeros((P))
    # starting from first day to the final day
    # first day we get an initial wealth of 0 (t = 0)
    returns = np.array(())
    returns = np.append(returns,1)
    for i in range(len(dates)):
        print("i is: " + str(i))
        # for each window size as based on the experts which is of length windowSize - 1
        for w in range(windowSize - 1):
            # for each corrThresh in the width which is P wide
            for p in range(P):
                # Apply the corn expert learning algorithm on this expert using its parameters
                experts[(windowSize-1)*w + p].currPort = expertLearn(experts[(windowSize-1)*w + p].windowSize, experts[(windowSize-1)*w + p].corrThresh, i, data)
        # combine our experts' portfolios
        portfolio = np.zeros((numStocks,))
        # update our total wealth
        day = dayReturn(i,dates,data)
        returns = np.append(returns, np.dot(portfolio, day))
        #update the experts' individual wealths
        expertDayEarly = experts
        for m in range(windowSize-1):
            for n in range(P):
                experts[(windowSize-1)*m + n].increaseWealth(day) 
        # TOP-K and expert weights update
        # first need to find these top-K experts
        # so select top K experts based on historical performance - so search through experts and find their wealths, as a 2D matrix, find those indices and work backwards ?
        # this will not be a 2D array and instead an array that is flattened
        # Given that experts should also be a flattened array this should be acceptable
        topK = findTopK(expertDayEarly)
        # since topK contains the indices of the top-k experts we will just loop through the experts
        for x in range((windowSize-1)*P):
            # set their weights (TOP K)
            if x in topK:
                experts[x].weight = 1 / K
            # set the weights for the rest to be 0 
            else:
                experts[x].weight = 0

        # generating the portfolio
        todayPortNumerator = np.zeros(numStocks)
        todayPortDenom = np.zeros(numStocks)
        for x in range((windowSize-1)*P):
            if experts[x].weight != 0:
                todayPortNumerator += experts[x].weight * (experts[x].wealthAchieved * experts[x].currPort)
                todayPortDenom += experts[x].weight * experts[x].wealthAchieved
            else:
                pass
        todayPort = todayPortNumerator / todayPortDenom
        for x in range(numStocks):
            print(x)
            portfolioHist[x][i] = todayPort[x]

data = readDataSet()
dataset = cornDataRead()
print(dataset)
dates = getDatesVec(data)
print(len(dates))
tempStartFind = data[data['Date'] == dates[0]]
tempTickersFind = np.unique(tempStartFind.Ticker.to_numpy())
numStocks = len(tempTickersFind)
today = dayReturn(1,dates,dataset)
print("CURRENT TESTS")
print(today)
market = marketWindow(1,1,dates,dataset)
print(market)
windowSize = 5
P = 5
K = 5
# for i in range(len(dates)- windowSize):
#     market = marketWindow(i,i+windowSize,dates,dataset)
    # print(i)
    # print(market)
# print("CHECKING EXPERT PORTFOLIO")
# uniformExp = expertLearn(windowSize, 0, 2, dataset)
# print("UNIFORM EXPERT")
# print(uniformExp)
# print("NORMAL EXPERT")
# normalExpert = expertLearn(25, 0.66, 103, dataset)
# print(normalExpert)
input("Ready to continue ? \n")
experts = initExperts(windowSize,numStocks,P)
printExperts(experts, windowSize, P)
print(type(experts))
print(type(experts[0]))
print(findTopK(experts))
# # printExperts(experts,windowSize,P)
runCorn(dates,dataset,windowSize,P)
