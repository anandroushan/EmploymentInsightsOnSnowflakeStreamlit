# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from sklearn.tree import DecisionTreeRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


# Report Title
st.title("India Employment Insight \U0001F4BC")
session = get_active_session()
st.subheader("1. Insights on Job Seekers: ")
ratio=0;

# REPORT ON JOBSEEKERS IN INDIA

# SELECT THE GROUP TO GET JOSEEKERS DISTRIBUTION ON THAT GROUP
sel_group = st.selectbox("Select any group to get insights on Job Seekers",options=['View By States', 'View By Age Groups', 'View By Qualifications'])

# IF SELECT GROUP IS - VIEW BY STATES
if sel_group == "View By States" :
    st.write("A dashboard to explore employment trends across Indian states.")
    try:
        # IMPORT THE DATA
        df=pd.DataFrame()
        try: 
            created_dataframe = session.sql("select * FROM STATEWISEJOBSEEKERS2022 where states <> 'Grand Total'")
            df = created_dataframe.to_pandas()
        except Exception as e:
            print("error loading the data from STATEWISEJOBSEEKERS2022 table.")
        # Execute the query and convert it into a Pandas dataframe
    
        #REPLACE THE COMMAS AND CONVERT TO FLOAT TYPE
        try:
            df[['TOTAL']]=df[['TOTAL']].replace(',','', regex=True).astype(float)
            ratio=sum(df['TOTAL'])
        except Exception as e:
            print("TOTAL column not found in STATEWISEJOBSEEKERS2022 table")
    
        #CREATE THE CHART
        try:
            st.subheader("Total Jobseekers by Indian States")
            st.line_chart(data=df, x="STATES", y="TOTAL")
        except Exception as e:
            print("Error Loading the line chart.")
    
        # PRINT THE TOTAL COUNT OF JOBSEEKERS
        st.markdown(f"<p style='text-align: center;'> Total Count: {ratio}</p>", unsafe_allow_html=True)

        try:
            # SELECT DIFFERENT VALUES ON THE DISTRIBUTION TO GET MORE INSIGHTS
            state = st.multiselect("Select state for more insights",options=sorted(df['STATES'].tolist()))
            st.write("Underlying data")
            dfs=df[df['STATES'].isin(state)]
            st.dataframe(dfs, use_container_width=True)
        except Exception as e:
            print('Error loading the data. States column not found in dataframe.')
    except Exception as e:
        print(e)


elif sel_group=='View By Age Groups':
    st.write("A dashboard to explore employment trends in India by all age groups")
    try:
        df=pd.DataFrame()
        try: 
            # IMPORT THE DATA
            created_dataframe = session.sql("select agegroup , TOTALJOBSEEKERREGISTRATION AS TOTAL, UPTO FROM agewisejobseeker2023")
            df = created_dataframe.to_pandas()
            # Execute the query and convert it into a Pandas dataframe
        except Exception as e:
                print("error loading the data from STATEWISEJOBSEEKERS2022 table.")
    
        try:
            # REMOVE THE COMMAS AND CONVERT INTO INTEGER
            df[['TOTAL']]=df[['TOTAL']].replace(',','', regex=True).astype(float)
        except Exception as e:
            print("TOTAL coulmn not found")
    
        try:
            # CREATE THE REPORT
            st.subheader("Total Jobseekers by various age groups in India")
            st.line_chart(data=df, x="AGEGROUP", y="TOTAL")
        except Exception as e:
            print("error loading line chart.")
    
        try:
            # TOTAL JOBSEEKERS COUNT
            st.markdown(f"<p style='text-align: center;'> Total Count: {sum(df['TOTAL'])}</p>", unsafe_allow_html=True)
        except Exception as e:
            print("TOTAL coulmn not found in dataframe")
    
        try:
            # SELECT ANY DISTRIBUTION TO GET MORE DETAILS
            state = st.multiselect("Select Age Group for more insights",options=sorted(df['AGEGROUP'].tolist()))
            st.write("Underlying data")
            dfs=df[df['AGEGROUP'].isin(state)]
            st.dataframe(dfs, use_container_width=True)
        except Exception as e:
            print("AGEGROUP column not found")
    except Exception as e:
        print(e)
else:
    try:
        df=pd.DataFrame()
        st.write("A dashboard to explore employment trends in India by Education Qualifications")

        try:
            # IMPORT THE DATA 
            created_dataframe = session.sql("select minimumqualification as QUALIFICATION , TOTALJOBSEEKERREGISTRATION AS TOTAL, UPTO FROM QUALIFICATIONWISEJOBSEEKER2023 order by rank")
            # Execute the query and convert it into a Pandas dataframe
            df = created_dataframe.to_pandas()
        except Exception as e:
            print(e)

        try:
            # REMOVE THE COMMAS AND CONVERT INTO INTEGER
            df[['TOTAL']]=df[['TOTAL']].replace(',','', regex=True).astype(float)
            # GET THE TOTAL JOBSEEKERS COUNT
            ratio=sum(df['TOTAL'])
        except Exception as e:
            print(e)

        try:
            # CREATE THE CHART 
            st.subheader("Total Jobseekers by Minimum Qualifications in India")
            st.line_chart(data=df, x='QUALIFICATION', y='TOTAL')
        except Exception as e:
            print(e)
    
        st.markdown(f"<p style='text-align: center;'> Total Count: {ratio}</p>", unsafe_allow_html=True)

        try: 
            # GET MORE INSGHTS ON VARIOUS DISTRIBUTION
            state = st.multiselect("Select Qualifications for more insights",options=sorted(df['QUALIFICATION'].tolist()))
            st.write("Underlying data")
            dfs=df[df['QUALIFICATION'].isin(state)]
            st.dataframe(dfs, use_container_width=True)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)



# INSIGHTS ON JOB VACANCY MOBILISED
st.subheader("2. Insights on Job Vacancies: ")

# DISTRIUTION OF DATA IN VARIOUS GROUPS
sel_group_emp = st.selectbox("Select any group to get insights on vacancies",options=['View By States', 'View By Employment Sectors', 'View By Qualifications'])

if sel_group_emp == "View By States" :
    try: 
        st.write("A dashboard to explore employment trends across Indian states.")
    
        df=pd.DataFrame()
        try:
            # INPORT THE DATA 
            created_dataframe = session.sql("select states as state, totalvacancy as total, upto FROM STATEWISEvacancy2023 where states <> 'Grand Total'")
            # Execute the query and convert it into a Pandas dataframe
            df = created_dataframe.to_pandas()
        except Exception as e:
            print(e)

        try:
            # REMOVE THE COMMAS AND CONVERT INTO INTEGER
            df[['TOTAL']]=df[['TOTAL']].replace(',','', regex=True).astype(float)
        except Exception as e:
            print(e)

        try:
            # CREATE THE CHART
            st.subheader("Total Vacancies Mobilised by Indian States")
            st.line_chart(data=df, x="STATE", y="TOTAL")
        except Exception as e:
            print(e)
            
        #GET THE TOTAL VACANCY MOBILISED
        ratio2=sum(df['TOTAL'])
        st.markdown(f"<p style='text-align: center;'> Total Count: {ratio2}</p>", unsafe_allow_html=True)
    
        # IF SAME GROUP IS SELECTED IN PART 1 OF THIS REPORT, GET THE OVERALL JOBSEEKERS TO VACANCY RATIO
        if ratio>0 and sel_group=="View By States":
            st.markdown(f"<p style='text-align: center;'> Vacancy to Jobseeker ratio: {round(ratio2/ratio, ndigits=2)}</p>", unsafe_allow_html=True)
        
        # SELECT THE GROUP VALUES TO GET MORE INSIGHTS
        state = st.multiselect("Select state for more insights",options=sorted(df['STATE'].tolist()))
        st.write("Underlying data")
        dfs=df[df['STATE'].isin(state)]
        st.dataframe(dfs, use_container_width=True)
    except Exception as e:
        print(e)

elif sel_group_emp=='View By Employment Sectors':

    try:
        st.write("A dashboard to explore employment trends in India by various sectors")
    
        df=pd.DataFrame()
        # LOAD THE DATA
        created_dataframe = session.sql("select sector , totalvacancy AS TOTAL, UPTO FROM sectorwisevacancy2023")
        # Execute the query and convert it into a Pandas dataframe
        df = created_dataframe.to_pandas()
    
        # REMOVE THE COMMAS AND CONVERT TO INTEGER
        df[['TOTAL']]=df[['TOTAL']].replace(',','', regex=True).astype(float)
    
        # CREATE THE CHART
        st.subheader("Total vacancy mobilised by various by various sectors in India")
        st.line_chart(data=df, x="SECTOR", y="TOTAL")
    
        # GET THE TOTAL VACANCY MOBILISED
        st.markdown(f"<p style='text-align: center;'> Total Count: {sum(df['TOTAL'])}</p>", unsafe_allow_html=True)
        
        # SELECT DIFFERENT GROUP TO GET MORE INSIGHTS
        state = st.multiselect("Select among differents sectors for more insights",options=sorted(df['SECTOR'].tolist()))
        st.write("Underlying data")
        dfs=df[df['SECTOR'].isin(state)]
        st.dataframe(dfs, use_container_width=True)
    
        # LOAD THE DATA FOR MACHINE LEARNING MODELLING
        dataset=session.sql("select * FROM sectorshare").to_pandas()
    
        # DATA PREPROCESSSING
        X=dataset.iloc[:, :-1].values
        y=dataset.iloc[:, -1].values
    
        # ENCODING THE VALUES
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
        X = np.array(ct.fit_transform(X))
        # st.write(X)
        # IMPORT THE ML LIBRARY
        from sklearn.ensemble import RandomForestRegressor
    
        # INSTACE CREATION OF RANDOM FOREST REGRESSOR
        regressor=RandomForestRegressor(n_estimators=10, random_state=0)
        regressor.fit(X, y)
    
        # PREDICT THE VALUES
        sector=st.selectbox("Select among differents sectors for the predicted share in employments in 2025",options=sorted(dataset['SECTOR'].unique()))
        st.write(f"Predicted share of {sector} in 2025 employments is {float(regressor.predict(np.array(ct.transform([[sector, 2025]]))))}")
        # st.write(regressor.predict(np.array(ct.transform(dataset.iloc[:, :-1]))))
    except Exception as e:
        print(e)

else:
    try:
        st.write("A dashboard to explore employment trends in India by Education Qualifications")
    
        df=pd.DataFrame()
        # IMPORT THE DATA 
        created_dataframe = session.sql("select minimumqualification as QUALIFICATION , TOTALVACANCies AS TOTAL, UPTO FROM QUALIFICATIONWISEVACANCY2023 where minimumqualification<> 'Grand Total'")
        # Execute the query and convert it into a Pandas dataframe
        df = created_dataframe.to_pandas()
    
        # REPLACE THE COMMAS AND CONVERT INTO INTEGER
        df[['TOTAL']]=df[['TOTAL']].replace(',','', regex=True).astype(float)
    
        # CREATE THE CHART 
        st.subheader("Total Vacancy mobilised by Minimum Qualifications in India")
        st.line_chart(data=df, x='QUALIFICATION', y='TOTAL')
    
        # GET THE TOTAL VACANCY MOBILISED FOR THIS GROUP
        ratio2=sum(df['TOTAL'])
        st.markdown(f"<p style='text-align: center;'> Total Count: {ratio2}</p>", unsafe_allow_html=True)
    
        # IF SAME GROUP IS SELECTED IN PART 1 OF THIS REPORT, GET THE OVERALL JOBSEEKERS TO VACANCY RATIO
        if ratio>0 and sel_group=="View By Qualifications":
            st.markdown(f"<p style='text-align: center;'> Vacancy to Jobseeker ratio: {round(ratio2/ratio, ndigits=2)}</p>", unsafe_allow_html=True)
        
    
        # SELECT THE GROUP TO GET MORE INSIGHTS
        state = st.multiselect("Select Qualifications for more insights",options=sorted(df['QUALIFICATION'].tolist()))
        st.write("Underlying data")
        dfs=df[df['QUALIFICATION'].isin(state)]
        st.dataframe(dfs, use_container_width=True)
    except Exception as e:
        print(e)
try:
    st.write("Note: All data is taken from data.gov.in")
except Exception as e:
    print(e)