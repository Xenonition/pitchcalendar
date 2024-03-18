import streamlit as st
from st_supabase_connection import SupabaseConnection
import datetime as dt

with st.form("new_pitch"):
   pitch_date = st.date_input("What Date Was The Pitch?")
   pitch_time = st.time_input("What Time Did it Happen?")
   audience = st.text_input("Who's the Audience?")
   categories = st.multiselect("Which Groups Were There?", ['Bobotoh','VVIP','Investors'])
   format = st.selectbox(
    'How Did The Pitch Happen?',
    ('Offline', 'Online'))
   status = st.selectbox(
    'What Is The Status of The Pitch?',
    ('TBD', 'In Progress', 'Completed'))
   person = st.text_input("Who is in Charge?")
   count = st.number_input("How Many Were There?", value=0, step=1, min_value=0)
   feedback = st.text_area("Was There Feedback?")
   link = st.text_input("Insert Documentation Link")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        with st.spinner('Inserting Report into Database'):
            conn = st.connection("supabase",type=SupabaseConnection)
            conn.table("pitches").insert([{
                'datetime':str(dt.datetime.combine(pitch_date, pitch_time)),
                'audience':audience,
                'categories':{"categories":categories},
                'format':format,
                'status':status,
                'person':person,
                'feedback':feedback,
                'link':link,
                'count':count
            }]).execute()