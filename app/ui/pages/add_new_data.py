import streamlit as st
import plotly.express as px

from utils.api_calls import api_request
from shared.contracts.user_input_contract import UserInput

st.title("CRM System for Advanced Data Analysis with a ChatBot")

sales_agent = st.selectbox('Sales agent name', [
    'Moses Frase', 'Darcel Schlecht', 'Zane Levy', 'Anna Snelling',
    'Vicki Laflamme', 'Markita Hansen', 'Niesha Huffines',
    'Gladys Colclough', 'James Ascencio', 'Maureen Marcano',
    'Hayden Neloms', 'Rosalina Dieter', 'Versie Hillebrand',
    'Daniell Hammack', 'Elease Gluck', 'Violet Mclelland',
    'Kami Bicknell', 'Rosie Papadopoulos', 'Kary Hendrixson',
    'Reed Clapper', 'Wilburn Farren', 'Garret Kinder',
    'Marty Freudenburg', 'Lajuana Vencill', 'Boris Faz',
    'Donn Cantrell', 'Corliss Cosme', 'Cassey Cress',
    'Cecily Lampkin', 'Jonathan Berthelot'])
product = st.selectbox('Select the product that was engaged', [
    'GTX Plus Basic', 'GTX Pro', 'MG Special', 'GTX Basic',
    'GTX Plus Pro', 'MG Advanced', 'GTK 500'])
account = st.selectbox('Select the customer (if known)', [
    'Cancity', 'Isdom', 'Codehow', 'Hatfan', 'Ron-tech',
    'J-Texon', 'Cheers', 'Zumgoity', 'Bioholding',
    'Genco Pura Olive Oil Company', 'Sunnamplex', 'Sonron',
    'Finjob', 'Scotfind', 'Treequote', 'Xx-zobam', 'Rantouch',
    'Fasehatice', 'Vehement Capital Partners', 'Warephase',
    'Zoomit', 'Labdrill', 'Zotware', 'dambase', 'Xx-holding',
    'Acme Corporation', 'Green-Plus', 'The New York Inquirer',
    'Mathtouch', 'Gogozoom', 'Stanredtax', 'Konmatfix',
    'Conecom', 'Golddex', 'Plexzap', 'Rundofase', 'Finhigh',
    'Funholding', 'Opentech', 'Silis', 'Goodsilron', 'Rangreen',
    'Kan-code', 'Nam-zim', 'Y-corporation', 'Bioplex',
    'Plusstrip', 'Toughzap', 'Dalttechnology', 'Ontomedia',
    'Kinnamplus', 'Statholdings', 'Umbrella Corporation',
    'Faxquote', 'Dontechi', 'Konex', 'Betasoloin', 'Domzoom',
    'Donquadtech', 'Globex Corporation', 'Plussunin', 'Condax',
    'Massive Dynamic', 'Doncon', 'Scottech', 'Gekko & Co',
    'Initech', 'Singletechno', 'Yearin', 'Lexiqvolax',
    'Zathunicon', 'Betatech', 'Bubba Gump', 'Blackzim',
    'Hottechi', 'Inity', 'Sumace', 'Zencorporation',
    'Groovestreet', 'Donware', 'Ganjaflex', 'Streethex',
    'Iselectrics', 'Newex', 'Bluth Company', 'Other'])


if account == 'Other':
    unknow_customer = st.text_input('Put the name of the new customer (if the above customers options are not available)')
else:
    unknow_customer = None

deal_stage = st.selectbox('Put the actual deal stage', ['Won', 'Engaging', 'Lost', 'Prospecting'])

engage_date = None
close_date = None
if deal_stage in ['Won', 'Lost', 'Engaging']:
    engage_date = st.date_input('Put the engage date')
    
    if not deal_stage == 'Engaging':
        close_date = st.date_input('Put the close date')

close_value = None
if deal_stage == 'Won':
    close_value = st.number_input('Put the closed value')
elif deal_stage == 'Lost':
    close_value = 0.0


if st.button('Save'):
    try:
        data = {'sales_agent':sales_agent,
                'product':product,
                'account':account,
                'unknow_customer':unknow_customer,
                'deal_stage':deal_stage,
                'engage_date':engage_date,
                'close_date':close_date,
                'close_value':close_value
        }

        deal_data = UserInput(**data)

        st.success("Data successfully saved")
        st.json(deal_data.model_dump(mode="json"))

        # Just won endpoint for now:
        api_request(
            api_url="http://localhost:8200/api/insert-won-stage-data/",
            json=deal_data.model_dump(mode="json")
        )

    except Exception as e:
        st.error(f"Error saving data: {e}")
