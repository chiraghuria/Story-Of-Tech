#!/usr/bin/env python
# coding: utf-8

# In[43]:


import math
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import streamlit as st
import urllib.request
from PIL import Image
import wget


# # Using Data to Tell Stories

# This tutorial has been created to give a walkthrough of the various possibilities of telling stories using Python's data visualization capabilities.

# Before we get into the data visualization, data, and the storytelling, let us take a step back and understand the primary objective of this tutorial

# ## Objective
# 
# Data Storytelling has the following components -
# 
# - **1. Data Understanding and Exploration**
# > _NOTE: While this step is one of the most critical ones in real-world, I think it is fair to assume that the intended audience for this tutorial will have a far amount of experience in data exploration. In order to keep the tutorial focused and instructive, we will move quickly through this section just enough to build an understand to hypothesize a few questions and curate our story._
# - **2. Data Modelling**
# - **3. Data Visualization** (Visuals created here are curated according to the story and questions that the data can answer)
# 
# Using Streamlit -
# - **4. Dashboarding**
# - **5. Local Deployment**

# ### What are data stories used for?
# 
# Across the industry, several roles like Business Intelligence Engineers, Reporting Analysts, Product Analysts, Business Analysts, Data Analysts, Technology Consultants, are actively working to deliver specially curated data-driven stories to their clients.
# 
# In my opinion, stories are used to communicate fact in a digestible form that enable the leaders and business teams to take decisions. Storytelling is a highly effective form of persuassion and can be extremely useful as we grow into becoming data scientists. Most of the insights and predictive analysis answers business questions that need to be communicated across.
# 
# Largely, I have seen data-driven stories take the following two forms: they either respond to a business question or are reporting the historic trends for the leadership to understand their organization better.
# > __In both cases, the requirements and business questions are fuzzy and broad but require actionable decisions nonetheless.__ 
# 
# __Example Problem:__ How can I make my organizations technology infrastructure more secure?
# 
# __Example Storyline:__ The story will have to breakdown and deliver the data views responding to lower level questions like what infrastructure assets are available, what are the current security benchmarks, how are security benchmarks defined, which technology assets are not meeting the benchmark, what is the reason for non-compliance, etc. These questions in conjunction with a narrative description will help the leader take decision

# ### What is the differtence between data visualization and data storytelling?

# __Data__ Visualization = Visual representation of the __Information__
# 
# __And what is information? or data?__
# 
# Data is representative of raw form whereas Information is a distilled and synthesized down version of the data. Data lacks coherence and Information is made relevant with coherence.
# 
# Similarly,
# Data Visualization is just a visual representation of the data. These are standalone visuals that respond to one or more __low-level questions__. However, data storytelling consists of a collection of these visuals responding to one __high-level question__. It is called storytelling because it is the visuals in conjunction with the narrative that together tell impactful data stories
# 
# __And what are these high-level and low-level questions?__
# 
# __High-level questions__ - These are the macro level questions that are asked usually by the business leaders wanting to have an overall assessment across their organization/data assets. It has a broader scope of concern. These questions are mostly subjective in nature if not broken down. Example - How is my team performing? You cannot respond to this using data unless you break it down to some low-level questions.
# 
# __Low-level questions__ - These are micro level questions that are asked usually by team leaders which generally require a quick snapshot of just their few organization/data assets. It has a narrower scope of concern. These questions are mostly quantifiable or factual. Example - How many people in my team got a promotion? How many R&D projects were succesfful vs failed? How have the employee satisfaction ratings changed over time? Responses to such low-level questions can help disambiguate and respond effectively (and reasonably objectively) to the high-level question of how a team is performing.
# 

# ## Now that we have the vocabulary covered, let's begin the learning!

# ## Motivation
# 
# Quick personal anecdote (I hope this resonates with you!) - 
# Back in 2017 when I started working with data, I was also doing dramatics in parallel. Around the same time, I saw a __TED talk by Hans Rosling (see below)__ and I was amused how one single visual brought so much of insight. I found a sweet spot between my love for expression through dramatics, and technology using data. Hans Rosling's TED talk truly inspired me and motivated me to reflecting upon it. I left with a few realizations and a learning -
# 1. I realized that the real power was in asking the right questions
# 2. I learnt that a powerful narrative is an equally important part of data stories
# 3. I realized that a visual can only give a limnited amount of insight on its own. Human intelligence with all its context, data and domain understanding can form deeper connection and draw more insightful inferences.

# ##### Video Playing Instructions
# 
# Please watch the below video __from 3:14 through 5:02__ for the visualization discussed above. Feel free to watch the entire video for getting inspired by Hans Rosling :)

# In[2]:


from IPython.display import YouTubeVideo

YouTubeVideo('hVimVzgtD6w', start=194, end=302, width=900, height=500)


# ## Objective
# 
# Data Storytelling has the following components -
# 
# - **1. Data Understanding and Exploration**
# > _NOTE: While this step is one of the most critical ones in real-world, I think it is fair to assume that the intended audience for this tutorial will have a far amount of experience in data exploration. In order to keep the tutorial focused and instructive, we will move quickly through this section just enough to build an understand to hypothesize a few questions and curate our story._
# - **2. Data Modelling**
# - **3. Data Visualization** (Visuals created here are curated according to the story and questions that the data can answer)
# 
# Using Streamlit -
# - **4. Dashboarding**
# - **5. Local Deployment**

# 
# Following are a few questions that I aim to answer using our Stack Overflow Survey Data (introduced in the following section) -
# 1. What are the top must have skills for developers in today's day and age. Are there any emerging new technologies?
# 2. Are high salaries correlated with the satisfaction rate? Do coders with high salaries have a high job satisfaction rate?
# 3. What are the skills that can drive maximum growth in upcoming 2-3 years after Master's?
# 4. Which countries offer a combination of job satisfaction and skills?

# ## 1. Data Understanding and Exploration

# 2018 Developer Survey results is being used from Kaggle. Below is the link. The schema file in the link explains what various columns mean
# 
# __Dataset:__ https://www.kaggle.com/stackoverflow/stack-overflow-2018-developer-survey
# 
# > __surveyresultspublic:__ Contains the main survey results, one respondent per row and one column per question. 
# 
# > __surveyresultsschema:__ Contains each column name from the main results along with the question text corresponding to that column.
# 
# There are 98,855 responses (rows) with 129 fields (columns) per entry in this public data release with attributes like : EmploymentType, FormalEducation level, UndergradMajor, Salary, YearsCoding, Job Satisfaction, LanguageWorkedWith, PlatformWorkedWith, Age, Gender, etc. 

# ##### Data Understanding

# In[3]:
import os.path
if not os.path.exists("survey_results_public.csv"):
  data = wget.download("https://akshaybl.blob.core.windows.net/tutorial/survey_results_public.csv")

if not os.path.exists("survey_results_schema.csv"):
  schema = wget.download("https://akshaybl.blob.core.windows.net/tutorial/survey_results_schema.csv")

df = pd.read_csv('survey_results_public.csv')


# In[4]:


# print("Stack Overflow 2018 Developer Survey data -  rows:",df.shape[0]," columns:", df.shape[1])


# In[5]:


# df.head()


# > Each row in the dataset represents the survey response of one respondent

# ##### Understanding the schema

# In[6]:


df_schema = pd.read_csv('survey_results_schema.csv')
pd.set_option('display.max_rows', 150)
pd.set_option('display.max_colwidth', 0)
# df_schema


# ##### Removing missing values for ease of data processing and visualization
# 
# We are retaining all rows and columns from the sample, assuming that if a value is missing it was intended to be missing by the respondent. This assumption has been made since the survey doesn't mandate a responder to answer to all the questions.
# 
# While in the real world this approach may not be ideal due to loss of potentially important information and some missing values may be important depending on the domain

# In[7]:


# current dataset

# df.shape


# In[8]:


# percentage of missing values in columns
total=df.isnull().sum().sort_values(ascending=False)
percent=(df.isnull().sum()/df.isnull().count()*100).sort_values(ascending = False)
tmp = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
# tmp

# In[9]:


# plotting the missing value data

def plot_missing_data(start, end, text):
    tmp1 = tmp[start:end]
    plt.figure(figsize = (16,4))
    plt.title('Missing data - percents of missing data (part %s)' % text)
    s = sns.barplot(x=tmp1.index,y=tmp1['Percent'])
    s.set_xticklabels(s.get_xticklabels(),rotation=90)
    plt.show()
    
# plot_missing_data(1,65,'1')
# plot_missing_data(65,130,'2')


# We can observe that we have a few columns that have a high percentage of missing values. However, since we are not sure why this is null. For instance, MilitaryUS, a boolean column with Yes/No/NA as data has over 83% null (NA) values. Nulls could mean that the respondent of the survey was not in the military or it could also mean that the respondent missed filling in the value.
# 
# Similarly, other missing data will also have to be dealt on a case-to-case basis based on a deeper domain understanding. 
# 
# 
# In the real world, expectation would be to remove most of these columns or impute the data. Currently, because we are yet to form a visualize the data and explore the story, we will retain all the columns.

# To make things consistent and accurate -
# 
# __NOTE:__ We will not use columns with high number of missing values so that our story doesn't communicate inaccurate insights

# In[10]:


# df.shape


# In[11]:


# df.info()


# ##### Data Slicing

# Slicing the data and working on a subset of 23 columns that I found interesting to help us tell a story!

# In[12]:


# selecting the columns

column_list=['Respondent','OpenSource','Hobby','Country','Employment','Student','FormalEducation','YearsCoding',
             'DevType','JobSearchStatus','UndergradMajor','LastNewJob','LanguageWorkedWith','YearsCodingProf',
            'StackOverflowVisit','CareerSatisfaction','LanguageDesireNextYear','CheckInCode','Salary','Gender','Currency',
            'ConvertedSalary','UpdateCV']
df_new=df[column_list]
# df_new.head()


# In[13]:


# df_new.shape


# In[14]:


# df_new.info()


# ##### Data Exploration and Standardization

# Existing columns will be retained and new columns that are added will be suffixed with `_derived` to help distinguish it from other columns

# #### Gender Column

# In[15]:


# Gender column has many unique values

# df_new["Gender"].unique()


# In[16]:


# creating a new derived column from Gender column with only three values - Male, Female, Non-Binary

def gender_condition(s):
    if s['Gender'] =='Female':
        return 'Female'
    elif s['Gender']=='Male':
        return 'Male'
    else:
        return 'Other'

df_new['Gender_derived']=df_new.apply(gender_condition,axis=1)
# df_new['Gender_derived'].unique()


# #### UnderGrad Major Column

# In[17]:


# undergrad major column has a lot of noise

#df_new.UndergradMajor.unique()


# In[18]:


# standardizing the undergrad major column

def undergradmajor_conditions(df):
    if df['UndergradMajor']=='Mathematics or statistics':
        return 'Maths/Statistics'
    elif df['UndergradMajor']=='A natural science (ex. biology, chemistry, physics)':
        return 'Biology/Chem/Physics'
    elif df['UndergradMajor']=='Computer science, computer engineering, or software engineering':
        return 'CS'
    elif df['UndergradMajor']=='Fine arts or performing arts (ex. graphic design, music, studio art)':
        return 'FineArts'
    elif df['UndergradMajor']=='Information systems, information technology, or system administration':
        return 'Information Systems'
    elif df['UndergradMajor']=='Another engineering discipline (ex. civil, electrical, mechanical)':
        return 'Other Engineering'
    elif df['UndergradMajor']=='A business discipline (ex. accounting, finance, marketing)':
        return 'Business/Accounts/Finance'
    elif df['UndergradMajor']=='A social science (ex. anthropology, psychology, political science)':
        return 'SocialSciences'
    elif df['UndergradMajor']=='Web development or web design':
        return 'WebDevelopment'
    elif df['UndergradMajor']=='A humanities discipline (ex. literature, history, philosophy)':
        return 'Humanities'
    elif df['UndergradMajor']=='A health science (ex. nursing, pharmacy, radiology)':
        return 'Nursing/Pharma'
    elif df['UndergradMajor']=='I never declared a major':
        return 'Unknown'
    
df_new.loc[:,'UndergradMajor_derived']=df_new.apply(undergradmajor_conditions,axis=1)
# df_new.loc[:,'UndergradMajor_derived'].unique()


# In[19]:


df_new.head()


# ##### CS major or not? 
# Deriving whether a respondent is from a CS background or not

# In[20]:


# standardizing UG Major column

df_new.loc[:,'UndergradMajor_CS_derived'] = df_new['UndergradMajor_derived'].map(lambda x : x if x == "CS" else "Non-CS")
# df_new.loc[:,'UndergradMajor_CS_derived'].unique()


# #### Career Satisfaction Column
# 
# CareerSatisfaction column has ordinal data and therefore might be helpful to get it in numeric form

# In[21]:


# CareerSatisfaction column data

# df_new["CareerSatisfaction"].unique()


# In[22]:


# deriving numeric values

values = ['Extremely dissatisfied', 'Moderately dissatisfied', 'Slightly dissatisfied', 'Neither satisfied nor dissatisfied',
          'Extremely satisfied', 'Moderately satisfied','Slightly satisfied']

careersat_map_dict = {x:(i-3) for i,x in enumerate(values)}
print(careersat_map_dict)
df_new['CareerSatisfaction_derived'] = df_new['CareerSatisfaction'].map(careersat_map_dict)
# df_new['CareerSatisfaction_derived'].unique()


# #### Formal Education
# 
# We can bucket the various formal education as ordinal data into numerics to indicate the level of education

# In[23]:


# formaleducation data has a lot of extra information that may not directly help in our story

# df_new["FormalEducation"].unique()


# In[24]:


# bucketing formaleducation information

def formaleducation_condition(df):
    if df['FormalEducation'] in ['Bachelor’s degree (BA, BS, B.Eng., etc.)', 'Associate degree']:
        return 2
    elif df['FormalEducation'] in ['Master’s degree (MA, MS, M.Eng., MBA, etc.)', 'Professional degree (JD, MD, etc.)']:
        return 3
    elif df['FormalEducation']=='Other doctoral degree (Ph.D, Ed.D., etc.)':
        return 4
    elif df['FormalEducation']=='Some college/university study without earning a degree':
        return 1
    else:
        return 0


df_new['FormalEducation_derived']=df_new.apply(formaleducation_condition,axis=1)
# df_new['FormalEducation_derived'].value_counts()


# #### Salary variable
# 
# Converting it to a standard float value

# In[26]:


# salary

df_new.loc[:,'Salary'] = df_new.loc[:,'Salary'].replace("[a-z,]","")
df_new.loc[:,'Salary'] = df_new.loc[:,'Salary'].str.replace(",","")
df_new.loc[:,'Salary']=df_new.loc[:,'Salary'].astype(float)
# df_new['ConvertedSalary']=df_new['ConvertedSalary'].astype(float)


# #### Years of Coding variable
# 
# Converting it to a standard float value

# In[27]:


# df_new['YearsCoding']


# In[28]:


df_new.loc[:,'YearsCoding'] = df_new.loc[:,'YearsCoding'].str.replace("years","")
df_new.loc[:,'YearsCoding'] = df_new.loc[:,'YearsCoding'].str.replace("or","").str.replace("me","")
df_new.loc[:,'YearsCoding'] = df_new.loc[:,'YearsCoding'].apply(lambda x: str(x).strip())
# df_new['YearsCoding'].head()


# #### Languages
# 
# Languages used by the respondents have been combined to reflect the possible role they performed

# In[29]:


# df_new.columns


# In[30]:


def languages_condition(df):
    if df['LanguageWorkedWith']=='C#;JavaScript;SQL;HTML;CSS':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='JavaScript;PHP;SQL;HTML;CSS':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='Java':
        return 'Java'
    elif df['LanguageWorkedWith']=='JavaScript;HTML;CSS':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='C#;JavaScript;SQL;TypeScript;HTML;CSS':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='JavaScript;PHP;SQL;HTML;CSS;Bash/Shell':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='JavaScript;PHP;HTML;CSS':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='Java;JavaScript;PHP;HTML;CSS':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='C#':
        return 'C#'
    elif df['LanguageWorkedWith']=='Python':
        return 'Python'
    elif df['LanguageWorkedWith']=='JavaScript;TypeScript;HTML;CSS':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='Java;JavaScript;HTML;CSS':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='JavaScript;Python;HTML;CSS':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='JavaScript;Python;Bash/Shell':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='C#;JavaScript;SQL;TypeScript;HTML;CSS;Bash/Shell':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='C;c++;Java;Matlab;R;SQL;Bash/Shell':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='Java;JavaScript;Python;TypeScript;HTML;CSS':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='C#;SQL':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='Java;JavaScript;PHP;SQL;HTML;CSS':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='C#;JavaScript;HTML;CSS':
        return 'Front-end'
    elif df['LanguageWorkedWith']=='Java;JavaScript;SQL;HTML;CSS;Bash/Shell':
        return 'Full-Stack'
    elif df['LanguageWorkedWith']=='JavaScript;PHP;Python;SQL;HTML;CSS;Bash/Shell':
        return 'Front-end'
    else:
        return 'Other'

df_new.loc[:,'Languages_derived']=df_new.apply(languages_condition,axis=1)
# df_new['Languages_derived'].unique()


# In[31]:


# df_new.head()


# In[32]:


# df_new.shape


# In[33]:


# df_new.info()


# ### Data Modelling and Visualization

# #### Formal Education & Country

# In[36]:


column_list=['Country','FormalEducation']
df_summary1=df_new.groupby(by=column_list,as_index=False).agg({'Respondent':'count'})
# df_summary1


# In[37]:


df_summary2=(df_summary1.sort_values(by=['Respondent'],ascending=False)).head(50)
# df_summary2


# In[38]:


column_list=['Country']
df_country=df_new.groupby(by=column_list,as_index=False).agg({'Respondent':'count'})
# df_country


# In[39]:


df_count2=(df_country.sort_values(by=['Respondent'],ascending=False)).head(50)
# df_count2


# ### Question: Which countries have maximum opportunities for Developers? 

# Visualization using Altair

# In[40]:


from altair import Chart, X, Y
response_by_country = alt.Chart(df_count2).mark_bar().encode(
    alt.X('Country',sort=alt.EncodingSortField(field='Country',op="count", order='descending')),
   alt.Y('Respondent')
)


# ### NOTE: The data is skewed as most respondents are from USA

# In[ ]:

alt.data_transformers.disable_max_rows()

bar = alt.Chart(df_new).mark_bar().encode(
    x='UndergradMajor_derived',
    y='Respondent',
    color='UndergradMajor_CS_derived'
)

bar.properties(width=200)


# ### Dashboarding and Deployment

# #### Using st.image() in streamlit to display a welcome image

# In[45]:


image_url = 'https://cdn.sstatic.net/insights/Img/Survey/2018/FacebookCard.png?v=c9eebbfb73c7'
st.image(image_url, width=800)
st.header("Number of Respondents by Country")
st.altair_chart(response_by_country, use_container_width=False)

st.header("Respondents across Majors")
st.altair_chart(bar, use_container_width=False)
