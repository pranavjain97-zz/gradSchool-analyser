import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# uniNames=pd.read_html("https://www.timeshighereducation.com/features/wikipedia-ranking-world-universities-top-100")  #can just get any tables from websites like this

#This is a Dataframe
#

# uniNames[0].set_index('Institution',inplace=True)

# print (uniNames[0][1])
from matplotlib import pyplot

uniData=pd.read_html("http://blog.collegetuitioncompare.com/2013/01/us-top-100-college-tuition-comparison.html")

uniFees=(uniData[2][['Unnamed: 0','2016Tuition & Fees','2017 Estimated Tuition & Fees','In-State','Out-of-State']])

# uniExtra=(uniData[2]['2016Tuition & Fees'])
# # print uniExtra
#
# uniExtra.replace("-","0",inplace=True)
# uniExtra=uniExtra.str.replace('$','')
# uniExtra=uniExtra.str.replace(',','').astype(float)
# print uniExtra.head()



uniFees.replace("-","0",inplace=True)
uniFees['2016Tuition & Fees']=uniFees['2016Tuition & Fees'].str.replace('$','')
uniFees['2016Tuition & Fees']=uniFees['2016Tuition & Fees'].str.replace(',','').astype(float)


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

# print uniFees
# *************GETTING MISSING DATA*********

uniFees.loc[uniFees['2017 Estimated Tuition & Fees'] == 0, '2017 Estimated Tuition & Fees'] = (uniFees['2016Tuition & Fees'])+2000

uniLivingCost.loc[uniLivingCost['Off-campus'] == 0, 'Off-campus'] = (uniLivingCost['On-Campus'])-1000
# print uniFees



uniFees.loc[uniFees['In-State'] == 0, 'In-State'] = (uniFees['2017 Estimated Tuition & Fees'])-15000
uniFees.loc[uniFees['Out-of-State'] == 0, 'Out-of-State'] = (uniFees['2017 Estimated Tuition & Fees'])



''' Could not apply SD because data has a lot of variation with fees'''
# *******STANDARD DEVIATION********
# uniFees['STD_fees'] = pd.rolling_std(uniFees['2017 Estimated Tuition & Fees'], 10)
#
# # print uniFees
# uniFees_std = uniFees.describe()['2017 Estimated Tuition & Fees']['std']
#
# print uniFees
# uniFees= uniFees[ (uniFees['STD_fees'] < uniFees_std) *10]
# print uniFees
# ***********xxxxxxxxx**********

# ***********GET INSTATE AND OUTSTATE FILL NA***************
uniFees['In-State'].fillna(value=uniFees['2017 Estimated Tuition & Fees'],inplace=True)
uniFees['Out-of-State'].fillna(value=uniFees['2017 Estimated Tuition & Fees'],inplace=True)


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


# ******************ACCEPTANCE RATES*************
uniAcceptanceRate=(uniData[0][['Rank','Acceptance Rates']])
# print (uniAcceptanceRate)
uniAcceptanceRate['Acceptance Rates'].replace('-',np.NaN,inplace=True)
uniAcceptanceRate['Acceptance Rates'].fillna(method='ffill',inplace=True)
uniAcceptanceRate['Acceptance Rates']=uniAcceptanceRate['Acceptance Rates'].str.replace('%','').astype(float)
# uniAcceptanceRate['Acceptance Rates']/=10



totalCost= pd.merge(uniFees,uniLivingCost)
# print (totalCost)
# totalCost.set_index('Unnamed: 0',inplace=True)

overallStats=totalCost.join(uniAcceptanceRate)
overallStats = overallStats[overallStats['2017 Estimated Tuition & Fees'] >2000]

overallStats.set_index('Unnamed: 0',inplace=True)

overallStats.dropna(inplace=True)
print overallStats
plots=overallStats.head(50)
# print plots
#Can apply concepts of pickling for students





fig = plt.figure()
ax1 = plt.subplot2grid((3,1), (0,0))
plt.ylabel('Tuition')
ax2 = plt.subplot2grid((3,1), (1,0),sharex=ax1)
plt.ylabel('Living')
ax3 = plt.subplot2grid((3,1), (2,0),sharex=ax1)
plt.ylabel('Prestige')


plots[['2016Tuition & Fees','2017 Estimated Tuition & Fees','In-State','Out-of-State']].plot(ax=ax1)
plots[['2017 Estimated Living Costs','On-Campus','Off-campus']].plot(ax=ax2)
plots[['Rank','Acceptance Rates']].plot(ax=ax3)
# minuteData['tx'].plot(color='k',ax=ax1,label='Minute Data')
# hourlyData['tx'].plot(color='k',ax=ax1,label='Hourly Data')

pyplot.locator_params(axis='x', nticks=10)
plt.xticks(rotation=70)
plt.legend()
plt.show()

#
# orders=pd.read_table('http://bit.ly/chiporders')
# orders['item_price']=orders['item_price'].str.replace('$','').astype(float)
# print (orders.head())
# print (orders.dtypes)


'''
1) Get mean deviation max min etc. ( Rolling Statistics)
2.) Using Standard deviation, i can get rid of arounious data. ( comparison, uses rolling)
3.) How to create functions for all this

'''