import streamlit as st
from streamlit_calendar import calendar
from st_supabase_connection import SupabaseConnection
import datetime as dt
import pandas as pd

#with st.spinner('Inserting Report into Database...'):

conn = st.connection("supabase",type=SupabaseConnection)
rows = conn.query("*", table="pitches", ttl="10m").execute().data
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
