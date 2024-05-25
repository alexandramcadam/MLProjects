from nim import train, play

ai = train(10000)
dict1 = ai.q #only has 9 values? - not adding q values correctly 

#print(ai.q[((1,2,0,0),(1,2))])
#print(ai.q[(0,1,2,0),(2,2)])
#print(ai.q[(0,0,1,2),(3,2)])
#play(ai)
