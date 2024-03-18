import streamlit as st
from streamlit_calendar import calendar
from st_supabase_connection import SupabaseConnection
import datetime as dt
import pandas as pd

#with st.spinner('Inserting Report into Database...'):

conn = st.connection("supabase",type=SupabaseConnection)
rows = conn.query("*", table="pitches", ttl="0").execute().data
to_download = rows

for row in rows:
    row['title'] = row['person']
    row['start'] = row['datetime']

calendar = calendar(events=rows)
if 'eventClick' in calendar.keys():
    pitch_selected = calendar['eventClick']['event']['extendedProps']
    pitch_df = pd.DataFrame(pitch_selected).drop(columns=['created_at', 'feedback', 'link'])
    pitch_df.index.name = None
    st.dataframe(pitch_df, hide_index=True)

    st.write('Feedback: ')
    st.write(pitch_selected['feedback'])

    try:
        st.page_link(pitch_selected['link'], label="Drive Link", icon="💾")
    except:
        st.write("No Valid Link Provided")

    with st.expander("Update Data"):
        with st.form("new_pitch", border=False):
            status = st.selectbox(
            'Update Pitch Status',
            ('TBD', 'In Progress', 'Completed'))
            count = st.number_input("Update Audience Count", value=0, step=1, min_value=0)
            feedback = st.text_area("Update Feedback")
            link = st.text_input("Update Documentation Link")
            submitted = st.form_submit_button("Submit")
            if submitted:
                with st.spinner('Inserting Report into Database'):
                    data, count = conn.table("pitches").update({'status':status, 'count':count, 'feedback':feedback, 'link':link}).eq('id', calendar['eventClick']['event']['id']).execute()

