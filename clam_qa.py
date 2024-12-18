# -*- coding: utf-8 -*-
"""
// aolabs.ai software >ao_core/hello_world_clamapp.py (C) 2024 Animo Omnis Corporation. All Rights Reserved.
@author: aolabs.ai
"""


from ao_core import ao_core as ao
import numpy as np
import streamlit as st  # used for the frontend, see https://streamlit.io/

from arch__clam import Arch

#%% # Constructing a clam Agent
if 'agent' not in st.session_state:

    # Creating an agent
    bc = ao.Agent( Arch, "first attempt, basic clam", save_meta=True)

    # Training agent to be closed (output=0) given 0 stimulus    

    # Storing Agent in session
    st.session_state.agent = bc
    st.session_state.agent_trials = 1

    # Storing Agent's performance in session, to display in the frontend
    # agent_results[0, :] = ["Trial #0", [0, 0, 0], 3, "LABEL", "0%", "All 0s"]
    st.session_state.agent_results = np.zeros( (200,  6), dtype='O')

# Running an Agent
def run_agent():

    # running the Agent                    
    response_array = []
    for x in np.arange(user_STATES):
        agent_response = st.session_state.agent.next_state( clam_INPUT, LABEL, DD=True, Hamming=False, INSTINCTS=instincts_ONOFF, unsequenced=True, print_result = True)   # core method to run Agents
        if agent_response == [1]:
            response_array.append(agent_response)
    
    percentage_results_totals = len(response_array)/ user_STATES * 100
    
    if labels_ONOFF == True:
        Label_Insti = "LABEL"
    elif instincts_ONOFF == True:
        Label_Insti = "INSTI"
    
    else: Label_Insti ="NONE"
    st.session_state.agent_results[st.session_state.agent_trials, :] = ["Trial #"+str(st.session_state.agent_trials), clam_INPUT, user_STATES, Label_Insti, str(percentage_results_totals)+"%", len(response_array)]
    st.session_state.agent_trials += 1

# App Front End
st.set_page_config(
    page_title="AO Labs Demo App",
    page_icon="https://i.imgur.com/j3jalQE.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and www.docs.aolabs.ai for more. Thank you!"
    }
)

st.title('Hello, World! A Clam-Level General Intelligence')
st.write("### *a toy problem demo by [aolabs.ai](https://www.aolabs.ai/)*")
# with st.expander("About & Context", expanded=False):

#     st.markdown("""
#     """)    
    
left_big_bottom, right_big_bottom = st.columns([0.6, 0.4])

with right_big_bottom:

    st.image("https://i.imgur.com/MjI8OCM.png")

with left_big_bottom:

    st.write("")
    st.write("")
    st.write("STEP 0) Activate learning:")
    instincts_ONOFF = st.checkbox('Instincts On')
    labels_ONOFF = st.checkbox('Labels On')
    if labels_ONOFF & instincts_ONOFF is True:
        st.write('Note: the presence of labels overrides any instinctual learning.')
    LABEL = []
    if labels_ONOFF is True:
        labels_CHOICE = st.radio('Pick one', ['OPEN the Clam', 'CLOSE the Clam'])
        if labels_CHOICE == 'OPEN the Clam':
            LABEL = 1
        if labels_CHOICE == 'CLOSE the Clam':
            LABEL = 0
    
    st.write("")
    st.write("")
    user_INPUT = st.multiselect("STEP 1) Show the Clam this input:", ['FOOD', 'A-CHEMICAL', 'B-CHEMICAL'])
    user_STATES = st.slider('This many times', 1, 100)
    clam_INPUT = np.zeros(3) 
    if 'FOOD'       in user_INPUT: clam_INPUT[0] = 1
    if 'A-CHEMICAL' in user_INPUT: clam_INPUT[1] = 1
    if 'B-CHEMICAL' in user_INPUT: clam_INPUT[2] = 1

    st.write("")
    st.write("")
    st.write("STEP 2) Run Trial: "+str(st.session_state.agent_trials))
    if user_STATES == 1: button_text= 'Expose Clam ONCE'
    if user_STATES > 1: button_text= 'Expose Clam '+str(user_STATES)+' times'
    st.button(button_text, on_click=run_agent)

# Displaying results of running the clam Agent

trial = st.session_state.agent_trials - 1
if st.session_state.agent_trials == 1: pass
else:
    st.write(str(st.session_state.agent_results[trial, 0])+" RESULTS: You exposed the clam to "+str(st.session_state.agent_results[trial, 1])+' as input for '+str(st.session_state.agent_results[trial, 2])+'   times with learning mode '+str(st.session_state.agent_results[trial, 3])+'.')
    if st.session_state.agent_results[trial, -1] == 0:
        st.session_state.agent_results[trial, -2] = "0%"
        if LABEL == 0: st.write("As you commanded, the Clam remained CLOSED, and learned to do so for the input you set.")
        else: st.write("The Clam didn't open at all. :(  Give it some food with this chemical and see how its behavior changes.")
    else:
        if LABEL == 1: st.write("As you ordered, the Clam was OPEN, and learned to do so for the input you set.")
        else: st.write('The Clam OPENED  '+str(st.session_state.agent_results[trial, -2]+' of the time.'))

st.write('')
st.write('## Results Log')
st.text("Displayed as: Trial #, Input Pattern, Steps, Labels or Instincts, Output %, Output #")
st.text(str(st.session_state.agent_results[1:st.session_state.agent_trials, :]))  