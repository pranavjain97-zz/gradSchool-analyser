from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import tkinter
import matplotlib.pyplot as plt
from matplotlib import style

# uniNames=pd.read_html("https://www.timeshighereducation.com/features/wikipedia-ranking-world-universities-top-100")  #can just get any tables from websites like this

#This is a Dataframe
#

# uniNames[0].set_index('Institution',inplace=True)

# print (uniNames[0][1])


uniData=pd.read_html("http://blog.collegetuitioncompare.com/2013/01/us-top-100-college-tuition-comparison.html")
# print (uniData[2])
uniFees=(uniData[2][['Unnamed: 0','2017 Estimated Tuition & Fees','In-State','Out-of-State']])
uniFees.replace("-","0",inplace=True)
uniFees['2017 Estimated Tuition & Fees']=uniFees['2017 Estimated Tuition & Fees'].str.replace('$','')
uniFees['2017 Estimated Tuition & Fees']=uniFees['2017 Estimated Tuition & Fees'].str.replace(',','').astype(float)

uniFees['In-State']=uniFees['In-State'].str.replace('$','')
uniFees['In-State']=uniFees['In-State'].str.replace(',','').astype(float)

uniFees['Out-of-State']=uniFees['Out-of-State'].str.replace('$','')
uniFees['Out-of-State']=uniFees['Out-of-State'].str.replace(',','').astype(float)


# print (uniFees.dtypes)



# ********************ALTER LIVING COSTS*****************
uniLivingCost=(uniData[3][['Unnamed: 0','On-Campus','Off-campus']])

uniLivingCost.replace("-","0",inplace=True)
# uniLivingCost.replace('[!-&]','',regex=True,inplace=True)

# print(pd.to_numeric(uniLivingCost['Off-campus'], errors='coerce'))

uniLivingCost['On-Campus']=uniLivingCost['On-Campus'].str.replace('$','')
uniLivingCost['On-Campus']=uniLivingCost['On-Campus'].str.replace(',','').astype(float)

uniLivingCost['Off-campus']=uniLivingCost['Off-campus'].str.replace('$','')
uniLivingCost['Off-campus']=uniLivingCost['Off-campus'].str.replace(',','').astype(float)



# uniLivingCost['Off-campus']=(uniLivingCost['Off-campus'])+2
uniLivingCost.loc[uniLivingCost['Off-campus'] == 0, '2017 Estimated Living Costs'] = (uniLivingCost['On-Campus']+uniLivingCost['Off-campus'])
uniLivingCost.loc[uniLivingCost['Off-campus'] > 0, '2017 Estimated Living Costs'] = (uniLivingCost['On-Campus']+uniLivingCost['Off-campus'])/2
# else:
#     uniLivingCost['2017 Estimated Living Costs'] = (uniLivingCost['On-Campus'] + uniLivingCost['Off-campus'])/2
# print (uniLivingCost.head(20))
# print (uniLivingCost.dtypes)

# uniLivingCost['On-Campus'].str.replace('$','')
# print (uniLivingCost)
# print (uniLivingCost.dtypes)
# uniLivingCost['TestingC']=uniLivingCost['On-Campus'].astype(float)
# print (uniLivingCost.dtypes)


# ******************xxxxx************

uniAcceptanceRate=(uniData[0][['Rank','Acceptance Rates']])
# print (uniAcceptanceRate.head())



totalCost= pd.merge(uniFees,uniLivingCost)
# print (totalCost.head())
# totalCost.set_index('Unnamed: 0',inplace=True)

overallStats=totalCost.join(uniAcceptanceRate)
overallStats.set_index('Unnamed: 0',inplace=True)
print (overallStats)
plots=overallStats.head(20)

#Can apply concepts of pickling for students

fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))

plots.plot(ax=ax1)
# minuteData['tx'].plot(color='k',ax=ax1,label='Minute Data')
# hourlyData['tx'].plot(color='k',ax=ax1,label='Hourly Data')

plt.legend()
plt.show()

#
# orders=pd.read_table('http://bit.ly/chiporders')
# orders['item_price']=orders['item_price'].str.replace('$','').astype(float)
# print (orders.head())
# print (orders.dtypes)
