
import numpy as np

import ao_core as ao
import ao_arch as ar

number_qa_neurons = 5

description = "Basic Clam"
arch_i = [1, 1, 1]     # 3 neurons, 1 in each of 3 channels, corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = [2]           # adding 1 control neuron which we'll define with the instinct control function below
arch_qa = [number_qa_neurons]
connector_function = "full_conn"



# To maintain compatibility with our API, do not change the variable name "Arch" or the constructor class "ar.Arch" in the line below
Arch = ar.Arch(arch_i, arch_z, arch_c, connector_function, arch_qa=arch_qa, qa_conn="full", description=description)

# Adding Instinct Control Neuron

def c0_instinct_rule(INPUT, Agent):
    if INPUT[0] == 1    and    Agent.story[Agent.state-1,  Agent.arch.Z__flat[0]] == 1:    
        print("c0 triggered")
        instinct_response = [1, "c0 instinct triggered"]
    else:
        print("c pass")
        instinct_response = [0, "c0 pass"]    
    return instinct_response            
# Saving the function to the Arch so the Agent can access it
Arch.datamatrix[4, Arch.C[1][0]] = c0_instinct_rule


c1=4
def c1_instinct_rule(INPUT, Agent):
    if INPUT[0] == 0 and Agent.story[Agent.state-1,  Agent.arch.Z__flat[0]] == 1:
        if Agent.counter ==0:
            instinct_response = [1, "c1 instinct triggered"]
        else:
            print("c1 pass")
            instinct_response = [0, "c1 pass"]
    else:
        print("c1 pass")
        instinct_response = [0, "c1 pass"]
    return instinct_response  
Arch.C__flat_pain = np.append(Arch.C__flat_pain, Arch.C__flat[c1])
Arch.datamatrix[4, Arch.C[1][1]] = c1_instinct_rule 

print(Arch.datamatrix[3, Arch.C__flat])

Arch.datamatrix[3, Arch.C__flat[4]] = np.array([]) #Decoupling the C1 neuron from all other neurons
Arch.datamatrix[3, Arch.C__flat[4]] = list(np.array([5, 6])) #Connecting the C1 neuron to the Z neuron


print(Arch.datamatrix[3, Arch.C__flat])


#Adding Aux Action
def qa0_firing_rule(INPUT, Agent): 
    if not hasattr(Agent, 'counter'):
        Agent.__setattr__("counter", 0)

    if Agent.counter < (number_qa_neurons+1) and INPUT[0] == 1    and Agent.story[ Agent.state-1,  Agent.arch.Z__flat[0]] == 1: #If the agent ate food 
        Agent.counter += 1
        group_response = np.zeros(number_qa_neurons)
        group_response[0 : Agent.counter] = 1
        print(group_response)
        
        print("increment")
    elif INPUT[0] == 0    and Agent.story[Agent.state-1,  Agent.arch.Z__flat[0]] == 1:   
        if Agent.counter == 0:
            group_response = np.ones(number_qa_neurons)
            group_response[0 : Agent.counter] = 1
            print(group_response)
            print("reset q aux")
        else:
            if Agent.counter >= 1:
                Agent.counter -= 1
            group_response = np.zeros(number_qa_neurons)
            group_response[0 : Agent.counter] = 1
        
            print(group_response)
            print("de increment")

    else:    #If the agent did not react then dont touch the counter
        group_response = np.zeros(number_qa_neurons)
        group_response[0 : Agent.counter] = 1
        print(group_response)
        print("nothing")
     

    group_meta = np.ones(number_qa_neurons, dtype="O")
    group_meta[:] = "qa0"
    return group_response, group_meta
# Saving the function to the Arch so the Agent can access it
Arch.datamatrix_aux[2] = qa0_firing_rule


#Connecting QA neurons to the Q Neurons
for i in range(len(arch_i)):
    Arch.datamatrix[1, Arch.Q__flat]+=Arch.datamatrix_aux[1]

#Connecting QA neurons to the Z Neurons
Arch.datamatrix[1, Arch.Z__flat] += Arch.datamatrix_aux[1]

