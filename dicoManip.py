graphe2 = {  
            "DC-A": { "R1": 20, "R2": 30},
            "R1" : {"R3" : 6, "Zonex":20},
            "R2" : {"R3" : 9, "Zonex":10},
            "R3" : {"Zonex": 14 }          
        }



DCA = { "R1": 35, "R2": 78}
R1 = {"R3" : 58, "Zonex":20}
R2 = {"R3" : 20, "Zonex":5}    
R3 = {"Zonex": 40 }
master = {"DC-A": dict(DCA), "R1": dict(R1), "R2": dict(R2), "R3": dict(R3)}

dicoCible = {}
for key, values in master.items():
    t={}
    #print(key, values)
    for key2, value2 in values.items():
        print(key2, value2)
        t[key2]=  value2 + 20
    dicoCible[key] = t

print("dicoCible: " + str(dicoCible))


def handleResiduel(increments, master):
    dicoCible = {
    key: {key2: value2 + increments for key2, value2 in values.items()}
    for key, values in master.items()  }
    return dicoCible

print("residuel: " + str(handleResiduel(20, master)))