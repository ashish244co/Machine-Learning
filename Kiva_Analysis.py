#!/usr/bin/env python
# coding: utf-8

# In[114]:


import pandas as pd
loans=pd.read_csv('kiva_loans.csv')
locations=pd.read_csv('kiva_mpi_region_locations.csv')
theme=pd.read_csv('loan_theme_ids.csv')
themesByRegions=pd.read_csv('loan_themes_by_region.csv')


# In[2]:


loans.info()


# In[3]:


loans['funded_timeDT'] = pd.to_datetime(loans['funded_time'], errors='coerce')
loans['posted_timeinDT'] = pd.to_datetime(loans['posted_time'], errors='coerce')
loans['disbursed_timeDT'] = pd.to_datetime(loans['disbursed_time'], errors='coerce')
loans['PostedToFunded']=(loans['funded_timeDT'].subtract(loans['posted_timeinDT']))
loans['PostedToFunded']=loans['PostedToFunded'].apply(lambda x: x.days)
loans['FundedToDisbursed']=(loans['disbursed_timeDT'].subtract(loans['posted_timeinDT']))
loans['FundedToDisbursed']=loans['FundedToDisbursed'].apply(lambda x: x.days)


# In[4]:


loans[loans['FundedToDisbursed']>0]['FundedToDisbursed'].count()


# In[5]:


loans[loans['FundedToDisbursed']<0]['FundedToDisbursed'].count()


# In[15]:


import seaborn as sns
sns.lineplot(x=loans['funded_amount'],y=loans['loan_amount'])


# In[16]:


import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px


# In[17]:


countryCount=loans.groupby('country')['id'].count().reset_index()


# In[31]:


data = [ dict(
        type = 'choropleth',
        locations = countryCount['country'],
        locationmode = 'country names',
        z = countryCount['id'],
        text = countryCount['country'],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(56, 142, 60)']],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(220, 83, 67)']],
        colorscale = [[0.8,"rgb(5, 10, 172)"],[0.85,"rgb(40, 60, 190)"],[0.9,"rgb(70, 100, 245)"],\
            [0.8,"rgb(90, 120, 245)"],[0.8,"rgb(106, 137, 247)"],[0.8,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Number of Loans'),
      ) ]

layout = dict(
    title = 'No of loans by Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[19]:


countryLoansMean=loans.groupby('country')['loan_amount'].mean().reset_index()


# In[20]:


data = [ dict(
        type = 'choropleth',
        locations = countryLoansMean['country'],
        locationmode = 'country names',
        z = countryLoansMean['loan_amount'],
        text = countryLoansMean['country'],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(56, 142, 60)']],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(220, 83, 67)']],
        colorscale = [[1,"rgb(5, 10, 172)"],[0.85,"rgb(40, 60, 190)"],[0.9,"rgb(70, 100, 245)"],\
            [1,"rgb(90, 120, 245)"],[1,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Loan amount mean by Country'),
      ) ]

layout = dict(
    title = 'Loan amount mean by Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[32]:


countryLoansSum=loans.groupby('country')['loan_amount'].sum().reset_index()


# In[33]:


data = [ dict(
        type = 'choropleth',
        locations = countryLoansSum['country'],
        locationmode = 'country names',
        z = countryLoansSum['loan_amount'],
        text = countryLoansSum['country'],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(56, 142, 60)']],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(220, 83, 67)']],
        colorscale = [[0.8,"rgb(5, 10, 172)"],[0.85,"rgb(40, 60, 190)"],[0.9,"rgb(70, 100, 245)"],\
            [0.8,"rgb(90, 120, 245)"],[0.8,"rgb(106, 137, 247)"],[0.8,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Loan amount sum'),
      ) ]

layout = dict(
    title = 'Loan amount sum by Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[9]:


loans.groupby('country').agg('count')['id'].plot(kind='barh', figsize=(10,30))


# In[10]:


loans['sector'].value_counts().plot(kind='barh', figsize=(10,10))


# In[11]:


loans['repayment_interval'].value_counts().plot(kind='bar', figsize=(10,10))


# In[12]:


loans['country'].value_counts().plot(kind='barh', figsize=(10,40))


# In[13]:


pd.DataFrame(loans.groupby('repayment_interval')[['repayment_interval','funded_amount']].agg('mean'))


# In[14]:


pd.DataFrame(loans.groupby('repayment_interval')[['repayment_interval','funded_amount']].agg('sum'))


# In[21]:


fig = px.box(loans, x="sector", y="loan_amount",pointpos=-1.8)
py.iplot(fig)


# In[23]:


loans['count_of_dependents']=loans['borrower_genders'].str.split(',')
loans['count_of_dependents']=loans['borrower_genders'].str.len()


# In[24]:


fig4 = px.histogram(loans, x="count_of_dependents")
py.iplot(fig4)


# In[25]:


fig5 = px.histogram(loans, x="lender_count")
fig5.show()


# In[78]:


loans.info()


# In[79]:


fig10 = px.histogram(loans, x="PostedToFunded")
fig10.show()


# In[26]:


loans.info()


# In[115]:


loans['useCleaned']=loans['use'].str.strip()


# In[116]:


uses=loans.groupby('useCleaned')['id'].count().reset_index()


# In[97]:


pd.options.display.max_colwidth = 200


# In[117]:


uses.sort_values(by='id',axis=0,ascending=False).head(50)


# In[118]:


uses['id'].sum()


# In[29]:


locations.head()


# In[30]:


locations.sort_values('MPI',axis=0,ascending=False)[['country','region','MPI']]


# In[28]:


locations.head()


# In[34]:


fig = go.Figure(data=go.Scattergeo(
        lon = locations['lon'],
        lat = locations['lat'],
        text = locations['LocationName'],
        mode = 'markers',
        marker_color = locations['MPI'],
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(180, 180, 180)'
            ),
            colorscale = 'Blues',
            cmin = 0,
            color = locations['MPI'],
            cmax = locations['MPI'].max(),
            colorbar_title="MPI"
        )
        ))

fig.update_layout(
        title = 'MPI',
        geo_scope='world',
    )
fig.show()


# In[36]:


mpiAverage=locations.groupby('country')['MPI'].mean().reset_index()


# In[37]:


data = [ dict(
        type = 'choropleth',
        locations = mpiAverage['country'],
        locationmode = 'country names',
        z = mpiAverage['MPI'],
        text = mpiAverage['country'],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(56, 142, 60)']],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(220, 83, 67)']],
        colorscale = [[0.8,"rgb(5, 10, 172)"],[0.85,"rgb(40, 60, 190)"],[0.9,"rgb(70, 100, 245)"],\
            [0.8,"rgb(90, 120, 245)"],[0.8,"rgb(106, 137, 247)"],[0.8,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'MPI by Country'),
      ) ]

layout = dict(
    title = 'MPI by Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[43]:


themesByRegions


# In[38]:


themesByRegions.groupby('Field Partner Name')[['Loan Theme Type','sector','region','country']].nunique()


# In[67]:


themesByRegions.groupby('country')[['Field Partner Name','sector','region','country']].nunique().sort_values(by='Field Partner Name',axis=0,ascending=False)


# In[75]:


X=themesByRegions.groupby('country')[['Field Partner Name']].nunique().sort_values(by='Field Partner Name',axis=0,ascending=False).reset_index()


# In[ ]:


Y=themesByRegions.groupby('country')[['Field Partner Name']].nunique().sort_values(by='Field Partner Name',axis=0,ascending=False).reset_index()


# In[76]:


X


# In[77]:


data = [ dict(
        type = 'choropleth',
        locations = X['country'],
        locationmode = 'country names',
        z = X['Field Partner Name'],
        text = X['country'],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(56, 142, 60)']],
        #colorscale = [[0,'rgb(255, 255, 255)'],[1,'rgb(220, 83, 67)']],
        colorscale = [[0.8,"rgb(5, 10, 172)"],[0.85,"rgb(40, 60, 190)"],[0.9,"rgb(70, 100, 245)"],\
            [0.8,"rgb(90, 120, 245)"],[0.8,"rgb(106, 137, 247)"],[0.8,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Field Partners Count Country'),
      ) ]

layout = dict(
    title = 'Field Partners Count Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[120]:


loans.info()


# ## Few unique insights :
# ### * Highest amount of MPI is not equal to highest amount of loans given.
# ### * Highest amount of MPI has one or none partners.
# ### * Partners are correlated to loaned amount.
# ### * More money is given to countries with stable economies and less risk have been taken.

# ## Few recommendations:
# ### * Get more partners in critical areas:
# ### * Use hedge fund limit currency risk.
# ### * Manage the tags better to reduce bias.
# ### * Work with starlink.
# ### * Get reliable internet coverage data.
# ### * Update MPI data regularly.

# # POPULARITY RECOMMENDATION ENGINE IDEA USING UNIQUE SCORING METRIC

# In[159]:


dat=pd.DataFrame()


# In[152]:


# dat['id']=loans['id']


# In[160]:


df_frequency_map = loans.useCleaned.value_counts().to_dict()
dat['Usage_Count'] = loans['useCleaned'].map(df_frequency_map)


# In[161]:


df_frequency_map2 = loans.sector.value_counts().to_dict()
dat['Sector_Count'] = loans['sector'].map(df_frequency_map2)


# In[162]:


df_frequency_map3 = loans.country.value_counts().to_dict()
dat['Country_count'] = loans['country'].map(df_frequency_map3)


# In[163]:


df_frequency_map4 = loans.currency.value_counts().to_dict()
dat['Currency_count'] = loans['currency'].map(df_frequency_map4)


# In[164]:


dat.isnull().sum()


# In[165]:


dat.head()


# In[166]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
dat=scaler.fit_transform(dat)


# In[214]:


data=pd.DataFrame(dat)


# In[215]:


data.rename(columns={0: "Usage_Count", 1: "Sector_Count", 2: "Country_count",3:'Currency_count'}, errors="raise",inplace=True)


# In[216]:


data.head()


# In[217]:


data['Score']=(100*data['Usage_Count'] + 50*data['Sector_Count'] + 30*data['Country_count'] + 20*data['Currency_count'])/(200)


# In[218]:


data['id']=loans['id']


# In[219]:


data


# In[222]:


data.rename(columns={'id': "Loan ID"}, errors="raise",inplace=True)


# In[224]:


data.sort_values(by='Score',axis=0,ascending=False)[['Loan ID','Score']].head(10)

