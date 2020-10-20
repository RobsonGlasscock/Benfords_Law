%reset -f
import pandas as pd
import numpy as np

df = pd.read_pickle('crsp_step1.pickle')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.5f}'.format

len(df)

df[['permno', 'date', 'ticker', 'comnam', 'prc']].head(200)

df['prc'].describe()

df['bool']= df['prc'] < 0
df['bool'].value_counts()
len(df)
df[(df['bool']== False) & (df['prc'] >1)]['prc'].describe()
df[df['prc'] >1]['prc'].describe()

# Note that these return the same summary because bool was set to be 1 when price is <0, so that's the same as just filtering for price >1.
len(df)
#df.loc[df['prc']== df['prc'].max()]
df[['ticker', 'prc']].loc[df['prc'] == df['prc'].max()]

df['date'].describe()
df['date'].min()
df['date'].max()

df['lead'] = df['prc'].astype(str).str[0]
df[['permno', 'date', 'ticker', 'comnam', 'prc', 'lead']].head(20)

# See if the first digit of stock prices follows Benford's Law
df['lead'].value_counts() /len(df)
# Stock prices follow Benford's Law

.value_counts()/ len(df[df['prc'] >1])
len(df[df['prc'] >1])
df['prc'][df['prc'] >1].describe()

df_lead_stock_prc= pd.DataFrame({'percent observed': df[df['prc'] >1]['lead'].value_counts() / len(df)})

df_lead_stock_prc

df_lead_stock_prc.reset_index(drop= False, inplace= True)
df_lead_stock_prc
df_lead_stock_prc.rename(columns= {'index': 'first digit'}, inplace= True)
df_lead_stock_prc['first digit']= df_lead_stock_prc['first digit'].astype(int)

def benfords(x):
    return np.log10(1 + 1/x)

df_lead_stock_prc['percent expected']= df_lead_stock_prc['first digit'].apply(benfords)
df_lead_stock_prc


df_lead_stock_prc.to_excel('c:\\users\\robso\\onedrive\\c\\xbanalytics\\benfords_anomaly\\auditing\\df_lead_stock_prc.xlsx', index=False)

# Next, use COMPUSTAT data to see if financial statement variables appear to follow Benford's Law.

df2= pd.read_csv('cstat.csv')

# Look at all variables/columns in the dataset.
df2.columns

df2[['datadate', 'tic', 'conm', 'at', 'cogs', 'epspx', 'revt', 'lt']].head(100)

df2['datadate'].describe()
df2['datadate'].min()
df2['datadate'].max()

len(df2)
# Check and see if total assets follows Benford's Law
df2['lead'] = df2['at'].astype(str).str[0]
df2['lead'].value_counts()
df2[df2['at'].notnull()]['lead'].value_counts() /len(df2[df2['at'].notnull()])
# Total assets monotonically decreases per Benford's Law, but the frequency buckets are smaller.

# Check and see if revenue follows Benford's Law
df2['lead'] = df2['revt'].astype(str).str[0]
df2['lead'].value_counts() /len(df)
df2[(df2['revt'].notnull()) & (df2['revt'] > 0)]['lead'].value_counts() /len(df2[df2['revt'].notnull()])
# Revenue monotonically decreases per Benford's Law, but the frequency buckets are smaller.

# Check total liabilities against Benford's Law.
df2['lead'] = df2['lt'].astype(str).str[0]
df2[(df2['lt'].notnull()) & (df2['lt'] > 0)]['lead'].value_counts()/len(df2[df2['lt'].notnull()])
# Total liabilities montonically decreaes, but with smaller frequency buckets compared to Benford's law.
