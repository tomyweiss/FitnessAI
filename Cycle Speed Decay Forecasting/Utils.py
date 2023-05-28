
import numpy as np
from datetime import datetime
from datetime import timedelta




def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


# Old Version Of "calculate_decay_rate()"
def calculate_decay_rate(df):
    decay = []
    #average decay rate
    for i in range(1,len(df) -1 ):
        x1 = df["spike/deep"][i]
        x2 = df["spike/deep"][i+1]
        if (x1 == 1) and (x2 == 0):
            x1_index = i
        elif (x1 == 0)  and (x2 == 1):
            decay.append(x1_index/i)
    decay.append(1)
    return decay

#insert empty (only dates) rows to the data
def insert_missing_rows(df,lead):
    for i in range(lead):
        d = datetime.strptime(df["dates"][-1], "%H:%M:%S:%f")
        sum = d + timedelta(seconds=1)
        df["dates"].append(datetime.strftime(sum,"%H:%M:%S:%f"))
        df["values"].append(0)
    return df


#New Verson Of calculate_decay_rate()
#Calculates the decay insert the results to the dictionary 'decay'.
def calculate_decay_rate(df,Exercise):
    
    decay = {"dates" : [],
            "values" : []
        }
    try:
        if Exercise == 'deadlift':
            for i in range(1,len(df) -1 ):
                x1 = df["spike/deep"][i]
                x2 = df["spike/deep"][i+1]
                if (x1 == -1) and (x2 == 0):
                    x1_index = i
                elif (x1 == 0)  and (x2 == -1):
                    if len(decay["dates"]) == 0:
                        decay["dates"].append(datetime.today().strftime("%H:%M:%S:%f"))
                        decay["values"].append((len(df) -1) / (i-x1_index))
                    else:
                        d = datetime.strptime(decay["dates"][-1], "%H:%M:%S:%f")
                        sum = d + timedelta(seconds=1)
                        decay["dates"].append(datetime.strftime(sum,"%H:%M:%S:%f"))
                        decay["values"].append((len(df) -1) / (i-x1_index))
        else:            
            #average decay rate
            for i in range(1,len(df) -1 ):
                x1 = df["spike/deep"][i]
                x2 = df["spike/deep"][i+1]
                if (x1 == 1) and (x2 == 0):
                    x1_index = i
                elif (x1 == 0)  and (x2 == 1):
                    if len(decay["dates"]) == 0:
                        decay["dates"].append(datetime.today().strftime("%H:%M:%S:%f"))
                        decay["values"].append((len(df) -1) / (i-x1_index))
                    else:
                        d = datetime.strptime(decay["dates"][-1], "%H:%M:%S:%f")
                        sum = d + timedelta(seconds=1)
                        decay["dates"].append(datetime.strftime(sum,"%H:%M:%S:%f"))
                        decay["values"].append((len(df) -1) / (i-x1_index))

    except UnboundLocalError as e:
        print("Error: Variable 'x1_index' referenced before assignment.")
        print(f"Exception: {e}")
        

    return decay


#Add one second
def add_sec(date):
    d = datetime.strptime(date, "%H:%M:%S:%f")
    return d + timedelta(seconds=1)


#Adding 3 points between every two points
def add_points(df,lead):

    new = {"dates" : [],
            "values" : []
        }
    for i in range(len(df)-1):
        x1 = df[i]      #left
        x2 = df[i+1]    #right
        m = (x1+x2)/2   #middle
        lm = (x1+m)/2   #left_middle
        rm = (m+x2)/2   #right_middle
        if len(new["dates"]) == 0:
            new["dates"].append(datetime.today().strftime("%H:%M:%S:%f"))
            new["values"].append(x1)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(lm)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(m)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(rm)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(x2)
        else:
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(lm)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(m)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(rm)
            new["dates"].append(datetime.strftime(add_sec(new["dates"][-1]),"%H:%M:%S:%f"))
            new["values"].append(x2)

            

    #Returning the dict populated with the original points + new additional points + forecast points
    return insert_missing_rows(new,lead)


