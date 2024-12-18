
import numpy as np

import ao_core as ao
import ao_arch as ar


description = "Basic Clam"
arch_i = [1, 1, 1]     # 3 neurons, 1 in each of 3 channels, corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = [1]           # adding 1 control neuron which we'll define with the instinct control function below

connector_function = "full_conn"

# To maintain compatibility with our API, do not change the variable name "Arch" or the constructor class "ar.Arch" in the line below
Arch = ar.Arch(arch_i, arch_z, arch_c, connector_function, description=description)

# Adding Instinct Control Neuron

def c0_instinct_rule(INPUT, Agent):
    if INPUT[0] == 1 and Agent.story[Agent.state-1,  Agent.arch.Z__flat[0]] == 1:        # self.Z__flat[0] needs to be adjusted as per the agent, which output the designer wants the agent to repeat while learning postively or negatively
        print("c0")
        instinct_response = [1, "c0 instinct triggered"]
    else:
        print("c pass")
        instinct_response = [0, "c0 pass"]    
    return instinct_response            
# Saving the function to the Arch so the Agent can access it
Arch.datamatrix[4, Arch.C[1][0]] = c0_instinct_rule

a = ao.Agent(Arch, save_meta=True)


while True:
    i1 = int(input())
    i2 = int(input())
    i3 = int(input())
    
    response_array = []
    for i in range(1):
        response = a.next_state([i1,i2,i3], DD = False, INSTINCTS=True, unsequenced=True, print_result=True)
        if response == [1]:
            response_array.append(1)
    print(response_array)
    percentage = len(response_array)/1


    print("response: ", percentage)





    
