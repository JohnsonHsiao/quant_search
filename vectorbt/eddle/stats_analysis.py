from turtle import pd
import pandas as pd

import numpy as np
import pandas as pd           
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import datetime as dt
import time
plt.style.use('ggplot')
data1d=pd.read_csv('/Users/edisonalbert/Documents/data4h1day/ETHUSDT_UPERP_1d.csv',parse_dates=True)
print(data1d)
print(type(data1d))
data1d['delta']=data1d['close']-data1d['open']
print(data1d['delta'])
print(len(data1d['delta']))




#statistical data of sequential red candal 
#for example: probability of reversing after four red candal in a row



#1day
negative=[]
cc=0
for i in range(len(data1d['delta'])):
    
    if data1d['delta'][i]<0:
        cc=cc+1
        negative.append(cc)
    else:
        negative.append(0)
        cc=0


print(len(negative))
print(len(data1d['delta']))


c=[]
odd1=[]
odd2=[]
odd3=[]
odd4=[]
odd5=[]
odd6=[]
odd8=[]
for i in range(1,len(negative)):
    if negative[i]==0:
        if negative[i-1]==0:
            continue
        else:
            if negative[i-1]==1:
                odd1.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])
            elif negative[i-1]==2:
                odd2.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])
            elif negative[i-1]==3:
                odd3.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])
            elif negative[i-1]==4:
                odd4.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])
            elif negative[i-1]==5:
                odd5.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])
            elif negative[i-1]==6:
                odd6.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])
            else:
                odd8.append(data1d['delta'][i]*100/data1d['open'][i])
                c.append(negative[i-1])

    else:
        continue

# plt.figure()
# plt.plot(odd1)
# plt.figure()
# plt.plot(odd2)
# plt.figure()
# plt.plot(odd3)
# plt.figure()
# plt.plot(odd4)
# plt.figure()
# plt.plot(odd5)
# plt.figure()
# plt.plot(odd6)
# plt.figure()
# plt.plot(odd8)

odd=[]

mmn=0
for i in range(len(odd1)):
    mmn=mmn+odd1[i]
averg1=mmn/len(odd1)
odd.append(averg1)
print(averg1)


mmn=0
for i in range(len(odd2)):
    mmn=mmn+odd2[i]
averg2=mmn/len(odd2)
print(averg2)
odd.append(averg2)

mmn=0
for i in range(len(odd3)):
    mmn=mmn+odd3[i]
averg3=mmn/len(odd3)
print(averg3)
odd.append(averg3)

mmn=0
for i in range(len(odd4)):
    mmn=mmn+odd4[i]
averg4=mmn/len(odd4)
print(averg4)
odd.append(averg4)

mmn=0
for i in range(len(odd5)):
    mmn=mmn+odd5[i]
averg5=mmn/len(odd5)
print(averg5)
odd.append(averg5)

mmn=0
for i in range(len(odd6)):
    mmn=mmn+odd6[i]
averg6=mmn/len(odd6)
print(averg6)
odd.append(averg6)

mmn=0
for i in range(len(odd8)):
    mmn=mmn+odd8[i]
averg8=mmn/len(odd8)
print(averg8)
odd.append(averg8)






print(set(c))
print(c.count(1)/len(data1d['delta'])*100)
print(c.count(2)/len(data1d['delta'])*100)
print(c.count(3)/len(data1d['delta'])*100)
print(c.count(4)/len(data1d['delta'])*100)
print(c.count(5)/len(data1d['delta'])*100)
print(c.count(6)/len(data1d['delta'])*100)
print(c.count(8)/len(data1d['delta'])*100)



p1=[]
seq=0
for i in [1,2,3,4,5,6,8]:
    seq=seq+c.count(i)
con=0
for i in [1,2,3,4,5,6,8]:
    con=con+c.count(i)
    print(con/seq)
    p1.append(con/seq)


x=[1,2,3,4,5,6,8]
y=[c.count(1),c.count(2),c.count(3),c.count(4),c.count(5),c.count(6),c.count(8)]

plt.figure()
plt.plot(x,y)
plt.figure()
plt.plot(x,p1)

kelly=[]
bet=0
for i in range(7):
    kelly.append((p1[i]*(odd[i]+1)-1)/odd[i])

print(kelly)





#1hr

data1d=pd.read_csv('/Users/edisonalbert/Documents/data4h1day/ETHUSDT_UPERP_1h.csv',parse_dates=True)

data1d['delta']=data1d['close']-data1d['open']


negative=[]
cc=0
for i in range(len(data1d['delta'])):
    
    if data1d['delta'][i]<0:
        cc=cc+1
        negative.append(cc)
    else:
        negative.append(0)
        cc=0





c=[]
for i in range(1,len(negative)):
    if negative[i]==0:
        if negative[i-1]==0:
            continue
        else:

            c.append(negative[i-1])
    else:
        continue




print(set(c))
print(c.count(1))
print(c.count(2))
print(c.count(3))
print(c.count(4))
print(c.count(5))
print(c.count(6))
print(c.count(7))
print(c.count(8))
print(c.count(9))


j=[1,2,3,4,5,6,7,8,9]
k=[c.count(1),c.count(2),c.count(3),c.count(4),c.count(5),c.count(6),c.count(7),c.count(8),c.count(9)]
plt.figure()
plt.plot(j,k)




#4hday
data1d=pd.read_csv('/Users/edisonalbert/Documents/data4h1day/ETHUSDT_UPERP_4h.csv',parse_dates=True)
data1d['delta']=data1d['close']-data1d['open']
negative=[]
cc=0
for i in range(len(data1d['delta'])):
    
    if data1d['delta'][i]<0:
        cc=cc+1
        negative.append(cc)
    else:
        negative.append(0)
        cc=0





c=[]
for i in range(1,len(negative)):
    if negative[i]==0:
        if negative[i-1]==0:
            continue
        else:

            c.append(negative[i-1])
    else:
        continue

print(c)


print(set(c))
print(c.count(1))
print(c.count(2))
print(c.count(3))
print(c.count(4))
print(c.count(5))
print(c.count(6))
print(c.count(7))
print(c.count(8))
print(c.count(9))


x=[1,2,3,4,5,6,7,8,9]
y=[c.count(1),c.count(2),c.count(3),c.count(4),c.count(5),c.count(6),c.count(7),c.count(8),c.count(9)]
plt.figure()
plt.plot(x,y)
plt.show()







