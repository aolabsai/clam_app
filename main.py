# -*- coding: utf-8 -*-
"""
// aolabs.ai software >ao_core/hello_world_clamapp.py (C) 2024 Animo Omnis Corporation. All Rights Reserved.
@author: aolabs.ai
"""

import numpy as np
import streamlit as st  # used for the frontend, see https://streamlit.io/

import ao_core as ao


# setting the Agent's Architecture, or neural configuration
description = "Basic Clam"
arch_i = [1, 1, 1]     # 3 neurons, 1 in each of 3 channels, corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = [1]           # adding 1 control neuron which we'll define with the instinct control function below
connector_function = "full_conn"

# Adding 1 Instinct Control Neuron corresponding to pleasure from eating Food
def c0_instinct_rule(INPUT, Agent):
    if INPUT[0] == 1    and    Agent.buffer[0,  Agent.arch.Z__flat[0]] == 1:     # i.e. if Input contains Food and Clam was in Output state "open," eating Food    
        print("c0 triggered")
        instinct_response = [1, "c0 instinct triggered"]
    else:
        print("c pass")
        instinct_response = [0, "c0 pass"]    
    return instinct_response            

arch = ao.Arch(arch_i, arch_z, arch_c, connector_function, description=description)
arch.datamatrix[4, arch.C[1][0]] = c0_instinct_rule # Saving the custom control function to the Arch so the Agent can access it


# Constructing a clam Agent
if 'agent' not in st.session_state:

    # Creating an agent
    st.session_state.agent = ao.Agent(arch, "first attempt, basic clam")
    st.session_state.agent_trials = 1
    st.session_state.agent_results = np.zeros( (200,  6), dtype='O')

# Setting the agent to be non-reactive when there is no stimuli
def pretrain_agent(steps=10):
    st.session_state.agent.reset_state()
    for s in range(steps):
        st.session_state.agent.next_state(INPUT=[0,0,0], LABEL=[0])
        st.session_state.agent.reset_state()
    
# Running an Agent
def run_agent(user_STATES, clam_INPUT, LABEL, DD=True, Hamming=False, INSTINCTS=False):

    responses = 0
    st.session_state.agent.reset_state() # adding a random state since inputs are non-contiguous (each input is independent, no sequence)
    for x in np.arange(user_STATES):
        # print(type(LABEL))
        print("INSTINCTS: "+str(INSTINCTS))
        agent_response = st.session_state.agent.next_state(clam_INPUT, LABEL=LABEL, DD=DD, Hamming=Hamming, INSTINCTS=INSTINCTS, unsequenced=True, print_result = True)   # core method to run Agents
        st.session_state.agent.reset_state()
        if agent_response == [1]:
            responses += 1
    
    percentage_results_totals = responses / user_STATES * 100
    
    # saving results to session state
    if labels_ONOFF == True:
        Label_Insti = "LABEL"
    elif instincts_ONOFF == True:
        Label_Insti = "INSTINCT"
    else:
        Label_Insti ="NONE"
    st.session_state.agent_results[st.session_state.agent_trials, :] = ["Trial #"+str(st.session_state.agent_trials), clam_INPUT, user_STATES, Label_Insti, str(percentage_results_totals)+"%", responses]
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

st.title('Hello, World! A Clam-Level AGI')
st.write("### *a toy problem demo by [aolabs.ai](https://www.aolabs.ai/)* -- [refer to this walk-through](https://docs.aolabs.ai/docs/basic-clam)")    

left_big_bottom, right_big_bottom = st.columns([0.6, 0.4])

with right_big_bottom:
    st.image("https://i.imgur.com/MjI8OCM.png")

with left_big_bottom:
    st.write("")
    st.write("")
    
    st.write("STEP 0) Activate learning type:")

    st.button('Pretrain on INPUT=[0,0,0], LABEL=0', on_click=pretrain_agent)
    instincts_ONOFF = st.checkbox('Instincts On')
    labels_ONOFF = st.checkbox('Labels On')
    if labels_ONOFF & instincts_ONOFF: st.write('Note: the presence of labels overrides any instinctual learning.') 
    LABEL = []
    if labels_ONOFF is True:
        labels_CHOICE = st.radio('Pick one', ['OPEN the Clam', 'CLOSE the Clam'])
        if labels_CHOICE == 'OPEN the Clam':  LABEL = [1]
        if labels_CHOICE == 'CLOSE the Clam': LABEL = [0]
    
    st.write("")
    st.write("")

    user_INPUT = st.multiselect("STEP 1) Show the Clam this input:", ['FOOD', 'A-CHEMICAL', 'B-CHEMICAL'])
    user_STATES = st.slider('This many times:', 1, 100)
    clam_INPUT = np.zeros(3) 
    if 'FOOD'       in user_INPUT: clam_INPUT[0] = 1
    if 'A-CHEMICAL' in user_INPUT: clam_INPUT[1] = 1
    if 'B-CHEMICAL' in user_INPUT: clam_INPUT[2] = 1

    st.write("")
    st.write("")

    st.write("STEP 2) Run Trial: "+str(st.session_state.agent_trials))
    DD = st.checkbox('Discrimination distance (weighted) lookup', value=True)
    Hamming = st.checkbox('Hamming (binary) lookup', value=True)
    if user_STATES == 1: button_text= 'Expose Clam ONCE'
    if user_STATES > 1: button_text= 'Expose Clam '+str(user_STATES)+' times'
    st.button(button_text, on_click=run_agent, args=[user_STATES, clam_INPUT, LABEL, DD, Hamming, instincts_ONOFF], type="primary")

# Displaying results of running the clam Agent
trial = st.session_state.agent_trials - 1
if st.session_state.agent_trials == 1: pass
else:
    st.write(str(st.session_state.agent_results[trial, 0])+" RESULTS: You exposed the clam to "+str(st.session_state.agent_results[trial, 1])+' as input for '+str(st.session_state.agent_results[trial, 2])+'   times with learning mode '+str(st.session_state.agent_results[trial, 3])+'.')
    if st.session_state.agent_results[trial, -1] == 0:
        st.session_state.agent_results[trial, -2] = "0%"
        if LABEL == [0]: st.write("As you commanded, the Clam remained CLOSED, and learned to do so for the input you set.")
        else: st.write("The Clam didn't open at all. :(  Give it some food with this chemical and see how its behavior changes.")
    else:
        if LABEL == [1]: st.write("As you ordered, the Clam OPENED, and learned to do so for the input you set.")
        else: st.write('The Clam OPENED  '+str(st.session_state.agent_results[trial, -2]+' of the time.'))

st.write('')
st.write('## Results Log')
st.text("Displayed as: Trial #, Input Pattern, Steps, Labels or Instincts, Output %, Output #")
st.text(str(st.session_state.agent_results[1:st.session_state.agent_trials, :]))  