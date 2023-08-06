import os
import pandas as pd
import csv
import json





def calcul_survey_area(xmin,xmax,ymin,ymax,shape_screen):
    return([xmin/shape_screen[0],ymin/shape_screen[1],xmax/shape_screen[0],ymax/shape_screen[1]]) # a calculer en pourcentage (xmin,ymin,xmax,ymax)

def calcul_pos_relative(survey_area,x_pos,y_pos):
    if x_pos > survey_area[0] and x_pos < survey_area[2]:  
        if y_pos > survey_area[1] and y_pos < survey_area[3]:
            x_relatif = (x_pos-survey_area[0])/(survey_area[2]-survey_area[0])
            y_relatif = (y_pos-survey_area[1])/(survey_area[3]-survey_area[1])
            return x_relatif,y_relatif
        else:
            return None,None
    else:
        return None,None
    
def state_screen(timestamp,result,offset,geolocalisation=False,export_argument=False):
    time= 0
    other =[]
    if geolocalisation == False:
        for t in range(len(result)):
            
            if (timestamp+offset)*1000 >= result["time"][t]:
                other =[]
                time = result["time"][t]
                if export_argument != False:
                    for k in range(len(export_argument)):
                        other.append(result[export_argument[k]][t])
    
                
                continue
            else:
                break
        return time,other
 
    else:
        box = [0,0,0,0]
        time =0
        for t in range(len(result)):
            
            if (timestamp+offset)*1000 >= result["time"][t]:
                other =[]
                box = [float(result["xmin"][t]),float(result["ymin"][t]),float(result["xmax"][t]),float(result["ymax"][t])]
                time = result["time"][t]
                if export_argument != False:
                    for k in range(len(export_argument)):
                        other.append(result[export_argument[k]][t])
                continue
            else:
                break
        return box,time,other 

def calcul_loc(x_rel,y_rel,coord_carte):
    x_coord = coord_carte[0] + x_rel*(coord_carte[2]-coord_carte[0] )
    y_coord = coord_carte[1] + y_rel*(coord_carte[3]-coord_carte[1] )
    return [x_coord,y_coord] 

def eye_tracker_to_fixation(path_to_fixation,survey_area,path_info,path_to_result=None,geolocalisation=False,export_argument_on_result=False,export_argument_on_fixation=False,name_export='coord_fixation_on_map.csv'):
    
    try :
        f = open(path_info,)
    except:
        print("Failed to load json")
    try :
        fixation = pd.read_csv(path_to_fixation)
    except:
        print("Failed to load fixation")  
   
    if "norm_pos_x" and "norm_pos_y" and "world_timestamp" and "fixation_id" and "world_index" and "dispersion" not in fixation.columns:
        raise KeyError("wrong format of the fixation file")
    if export_argument_on_fixation != False:
        for i in range(len(export_argument_on_fixation)):
            if export_argument_on_fixation[i] not in fixation.columns:
                raise KeyError("the argument "+ export_argument_on_fixation[i]+" is not in the fixation file")
   

    json_time = json.load(f)
    start_time_system = float(json_time["start_time_system_s"]) # System Time at recording start
    start_time_synced = float(json_time["start_time_synced_s"])
    offset = start_time_system - start_time_synced 

    if path_to_result != None:
        assert os.path.exists(path_to_result)
        result = pd.read_csv(path_to_result) 
        if export_argument_on_result != False :
            for i in range(len(export_argument_on_result)):
                if export_argument_on_result[i] not in result.columns:
                    raise KeyError("the argument "+ export_argument_on_result[i]+" is not in the result file")  
    if geolocalisation == True :
        if "xmin" and "ymin" and "xmax" and "ymax" not in result.columns:
            raise KeyError("error data")
    
    
    coord_fixation = []
    for k in range(len(fixation)):
        id = fixation["fixation_id"][k]
        world_index = fixation["world_index"][k]
        if export_argument_on_fixation != False:
            liste_export_fixation =[]
            for k in range(len(export_argument_on_fixation)):
                        liste_export_fixation.append(fixation[export_argument_on_fixation[k]][t])    


        x_rel,y_rel = calcul_pos_relative(survey_area,float(fixation["norm_pos_x"][k]),float(fixation["norm_pos_y"][k]))
        if x_rel != None:
            if path_to_result == None:
                list =[world_index,id,(fixation["world_timestamp"][k]+offset)*1000,x_rel,y_rel,]
                if export_argument_on_fixation != False:
                        for p in range(len(export_argument_on_fixation)):
                            list.append(liste_export_fixation[p])
                coord_fixation.append(list)
            else:
                if geolocalisation == False:
                    time,other =  state_screen(fixation["world_timestamp"][k],result,offset,export_argument=export_argument_on_result)

                    list = [world_index,id,time,x_rel,y_rel]
                    if export_argument_on_fixation != False:
                        for p in range(len(export_argument_on_fixation)):
                            list.append(liste_export_fixation[p])
                    if export_argument_on_result != False:
                        for t in range(len(other)):
                            list.append(other[t])
                    coord_fixation.append(list)

                else:
                    box,time,other = state_screen(fixation["world_timestamp"][k],result,offset,geolocalisation=geolocalisation,export_argument=export_argument_on_result)
                    x_loc,y_loc =calcul_loc(x_rel,y_rel,box)
                    list = [world_index,id,time,x_loc,y_loc]
                    if export_argument_on_fixation != False:
                        for p in range(len(export_argument_on_fixation)):
                            list.append(liste_export_fixation[p])
                    if export_argument_on_result != False:
                        for t in range(len(other)):
                            list.append(other[t])
                    coord_fixation.append(list)


    if path_to_result == None:
        with open(name_export, 'w', newline='') as file:
            writer = csv.writer(file)
            entete = ["world_index","id_fixation","time","x_rel","y_rel"]
            if export_argument_on_fixation != False :
                for t in range(len(export_argument_on_fixation)):
                    entete.append(export_argument_on_fixation[t])
            writer.writerow([entete]) # rajouter le zoom
            for i in range(len(coord_fixation)):
                writer.writerow(coord_fixation[i])
    else:
        if geolocalisation == False:

            with open(name_export, 'w', newline='') as file:
                writer = csv.writer(file)
                entete = ["world_index","id_fixation","time","x_rel","y_rel"]
                if export_argument_on_fixation != False :
                    for t in range(len(export_argument_on_fixation)):
                        entete.append(export_argument_on_fixation[t])
                if export_argument_on_result != False :
                    for t in range(len(export_argument_on_result)):
                        entete.append(export_argument_on_result[t])
                writer.writerow(entete) # rajouter le zoom
                for i in range(len(coord_fixation)):
                    writer.writerow(coord_fixation[i])

        else:

            with open(name_export, 'w', newline='') as file:
                writer = csv.writer(file)
                entete = ["world_index","id_fixation","time","x","y"]
                if export_argument_on_fixation != False :
                    for t in range(len(export_argument_on_fixation)):
                        entete.append(export_argument_on_fixation[t])
                if export_argument_on_result != False :
                    for t in range(len(export_argument_on_result)):
                        entete.append(export_argument_on_result[t])
                writer.writerow(entete) # rajouter le zoom
                for i in range(len(coord_fixation)):
                    writer.writerow(coord_fixation[i])

