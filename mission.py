from ast import Break
import os
import math
import subprocess
import time
import sys
import clr
import MissionPlanner 
import MAVLink


clr.AddReference("MissionPlanner.Utilities")    # includes the Utilities class
clr.AddReference("MAVLink")  # includes the Utilities class

velocities=[0]
Script.Sleep(1000)
def outputs():
    x=cs.timeInAir
    average_energy=(Total_batteries_inicial-total_batery())/x
    dist_traveled=cs.distTraveled
    avr_speed=dist_traveled/x


    velocities.append(0)
    velocities_list = [velocities]

    outfile = open('outputs.txt', 'w')
    for number in velocities_list:
        outfile.write(str(number))
    outfile.close()
    desired_outputs=[]

    
    desired_outputs.append('Total mission duration: {min} min {seg} sec\n'.format(min=int(x//60), seg=int(x%60)))
    desired_outputs.append('Average energy spent: {ener} %/min\n'.format(ener=round(100*60*average_energy/Total_batteries_inicial, 2)))
    desired_outputs.append('Total distance travelled: {d} m\n'.format(d=round(dist_traveled, 2)))
    desired_outputs.append('Average speed: {speed} m/s\n'.format(speed=round(avr_speed, 2)))
    desired_outputs.append('Waypoints visited: {vis}/{tot}\n'.format(vis=n_wp, tot=len(Wp)))
    if returned:
        diference_dist=(dist_total-dist_traveled)
        desired_outputs.append('Remaining distance: {d} m\n'.format(d=round(diference_dist, 2)))
    outfile = open('Results.txt', 'w')
    for entry in desired_outputs:
        outfile.write((entry))
    outfile.close()
    os.system("python output.py")
    os.remove('outputs.txt')
    os.remove('waypoints.txt')



def goto_wp(position, n, total):
    """
    Sends the drone to a waypoint at the given coordinates.
    """

    item = MissionPlanner.Utilities.Locationwp() # creating waypoint
    MissionPlanner.Utilities.Locationwp.lat.SetValue(item,position[0]) # sets latitude
    MissionPlanner.Utilities.Locationwp.lng.SetValue(item,position[1]) # sets longitude
    MissionPlanner.Utilities.Locationwp.alt.SetValue(item,position[2]) # sets altitude
    MAV.setGuidedModeWP(item) # tells UAV “go to” the set lat/long @ alt
    print ('WP {number}/{final}'.format(number = n, final = total))
    times_run=0  #because the first cs.wp_dist is 0 we garantee that it is calculated a few times before determining arrival distance
    
    while True:
        if cs.wp_dist <1 and times_run>1:
            velocities.append(cs.vlen)
            Script.Sleep(1000)
            break
        times_run+=1
        velocities.append(cs.vlen)
        Script.Sleep(1000)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    time.sleep(5)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    Script.ChangeMode("Guided")   
    MAV.doCommand(MAVLink.MAV_CMD.COMPONENT_ARM_DISARM, 1, 0, 0, 0, 0, 0, 0)
    start=time.time()
    while not cs.armed:      
        now=time.time()-start
        print(" Waiting for arming...")
        Script.Sleep(1000)
        if now>5:
            print('Error ocurred while arming')
            print('Please try again')
            sys.exit()
    print("Taking off!")
    MAV.doCommand(MAVLink.MAV_CMD.TAKEOFF, 0, 0, 0, 0, 0, 0, aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        if cs.alt>=aTargetAltitude*0.98: #Trigger just below target alt.
            print("Reached target altitude")
            velocities.append(cs.vlen)
            break
        velocities.append(cs.vlen)
        Script.Sleep(1000)

def loiter(t):
    #Script.ChangeMode("Loiter")
    MAV.doCommand(MAVLink.MAV_CMD.LOITER_TIME, t, 0, 0, 0, 0, 0, 0)     #Sends a loiter command with the specified time=t
    print('Capturing image...')
    for i in range (t):
        Script.Sleep(1000)
        velocities.append(cs.vlen)

def total_batery():
    x=0
    if cs.battery_cell1 > 0:
        x+=cs.battery_remaining
    if cs.battery_cell2 > 0:
        x+=cs.battery_remaining2
    if cs.battery_cell3 > 0:
        x+=cs.battery_remaining3
    if cs.battery_cell4 > 0:
        x+=cs.battery_remaining4
    if cs.battery_cell5 > 0:
        x+=cs.battery_remaining5
    if cs.battery_cell6 > 0:
        x+=cs.battery_remaining6
    if cs.battery_cell7 > 0:
        x+=cs.battery_remaining7
    if cs.battery_cell8 > 0:
        x+=cs.battery_remaining8
    if cs.battery_cell9 > 0:
        x+=cs.battery_remaining9
    if cs.battery_cell10 > 0:
        x+=cs.battery_remaining10
    if cs.battery_cell11 > 0:
        x+=cs.battery_remaining11
    if cs.battery_cell12 > 0:
        x+=cs.battery_remaining12
    if cs.battery_cell13 > 0:
        x+=cs.battery_remaining13
    if cs.battery_cell14 > 0:
        x+=cs.battery_remaining14
    return x

def organizer(Wps,x, totalLat):
    lat1=[Wps[0][0]]
    if x==3 and totalLat%2==0 or x==4 and totalLat%2==1 or x==1:
        Counter_lat=0
    if x==3 and totalLat%2==1 or x==4 and totalLat%2==0 or x==2:
        Counter_lat=1
    Lat_start=0
    for j in range (len(Wps)):
        if Wps[j][0]!=lat1:
            Counter_lat+=1
            lat1=Wps[j][0]
            if Counter_lat%2 == 1:
                total_length=j-(Lat_start-1)
                for k in range (total_length//2):
                    Wps[Lat_start+k], Wps[j-1-k]=Wps[j-1-k], Wps[Lat_start+k] 
            else:
                Lat_start=j
        if j == len(Wps)-1 and Counter_lat%2 == 0:
            total_length=j-(Lat_start-1)
            for k in range (total_length//2):
                Wps[Lat_start+k], Wps[j-k]=Wps[j-k], Wps[Lat_start+k] 
    if x==3 or x==4:
        for j in range (len(Wps)//2):
            Wps[j], Wps[(len(Wps)-1)-j]= Wps[(len(Wps)-1)-j], Wps[j]
    return(Wps)

def Corners(Wps):
    '''
    Picks the closest corner to home positions, given a set of waypoints.
    '''
    if len(Wps)>3:
        lat1=0
        Lat_start=0
        Counter_lat=0
        corner1=Wps[0]
        corner4=Wps[-1]
        for j in range (len(Wps)):
            if Wps[j][0]!=lat1 and Counter_lat==1:
                corner2=Wps[j-1]
            if Wps[j][0]!=lat1:
                lat1=Wps[j][0]
                Lat_start=j
                Counter_lat+=1
            if j == len(Wps)-1:
                corner3=Wps[Lat_start]
        try:
            if corner2 not in locals():
                corner2=corner1
        except TypeError:
            corner2=corner2
        try:
            if corner3 not in locals():
                corner3=corner4
        except TypeError:
            corner3=corner3

        dist1=math.sqrt((corner1[0]-cs.lat)**2+(corner1[1]*math.cos(corner1[0]*math.pi/180)-cs.lng*math.cos(cs.lat*math.pi/180))**2)
        dist2=math.sqrt((corner2[0]-cs.lat)**2+(corner2[1]*math.cos(corner2[0]*math.pi/180)-cs.lng*math.cos(cs.lat*math.pi/180))**2)
        dist3=math.sqrt((corner3[0]-cs.lat)**2+(corner3[1]*math.cos(corner3[0]*math.pi/180)-cs.lng*math.cos(cs.lat*math.pi/180))**2)
        dist4=math.sqrt((corner4[0]-cs.lat)**2+(corner4[1]*math.cos(corner4[0]*math.pi/180)-cs.lng*math.cos(cs.lat*math.pi/180))**2)
        x=min([dist1,dist2,dist3,dist4])
        if x==dist1:
            x=1
        elif x==dist2:
            x=2
        elif x==dist3:
            x=3
        else:
            x=4
    else:
        x=1
        Counter_lat=1
    return(x,Counter_lat)

def RTL():
    item = MissionPlanner.Utilities.Locationwp() # creating waypoint
    MissionPlanner.Utilities.Locationwp.lat.SetValue(item,Home[0]) # sets latitude
    MissionPlanner.Utilities.Locationwp.lng.SetValue(item,Home[1]) # sets longitude
    MissionPlanner.Utilities.Locationwp.alt.SetValue(item,Home[2]) # sets altitude
    MAV.setGuidedModeWP(item) # tells UAV “go to” the set lat/long @ alt
    times_run=0  #because the first cs.wp_dist is 0 we garantee that it is calculated a few times before determining arrival distance
    while True:
        if cs.wp_dist <1 and times_run>2:
            velocities.append(cs.vlen)
            Script.Sleep(1000)
            break
        times_run+=1
        velocities.append(cs.vlen)
        Script.Sleep(1000)
    print 'Landing...'
    MAV.doCommand(MAVLink.MAV_CMD.LAND, 0, 0, 0, 0, cs.lat, cs.lng, 0)


output=subprocess.check_output("python create_waypoints.py", shell=True)
print(output)


infile=open('waypoints.txt', 'r')                     ##These commands open
f=infile.readlines()                                  ##the file where
c=f[0]                                                ##the waypoint
lista=c.split(",")                                    ##locations were stored
infile.close()

Total_batteries_inicial=total_batery()

Wp=[]
for i in range (len(lista)//2-1):
    Wp.append([float(lista[2*i+1]),float(lista[2*i+2])])
print('Number of waypoints: {}'.format(len(Wp)))

x,y=Corners(Wp)
Wps=organizer(Wp,x,y)

altitude=20
dist_total=0
for i in range (len(Wps)):
    Wps[i].append(altitude)
    if i>0:
        dist_total+=111139*math.hypot(Wps[i-1][0]-Wps[i][0], (Wps[i-1][1]*math.cos(Wps[i-1][0]*math.pi/180)-Wps[i][1]*math.cos(Wps[i][0]*math.pi/180)))


if not cs.connected:
    print 'No drone detected'
    print 'Waypoints defined saved at waypoints.txt'
    sys.exit()

print 'Starting Mission'
Script.Sleep(1000)      
returned=False
arm_and_takeoff(altitude)

Home=[cs.lat, cs.lng, altitude]
distance_home=0
Takeoff_energy=4*(Total_batteries_inicial-total_batery())    
dist_total+=111139*math.hypot(Home[0]-Wps[-1][0], (Home[1]*math.cos(Home[0]*math.pi/180)-Wps[-1][1]*math.cos(Wps[-1][0]*math.pi/180)))

n_wp=0
spending=0
for i in range (len(Wps)):
    rtl_energy=spending*distance_home+Takeoff_energy
    battery_remainig=total_batery()
    if battery_remainig > 10 + rtl_energy:
        n_wp+=1
        goto_wp(Wps[i], n_wp, len(Wp))
        loiter(2)
    else:
        print'Low Battery'
        returned=True
        print 'Mission Aborted'
        print 'Returning to Launch'
        RTL() 
        while True:
            if cs.landed:
                print 'Mission Complete'
                break
            velocities.append(cs.vlen)
            Script.Sleep(1000)
        break
    location=[cs.lat, cs.lng, cs.alt]
    distance_home=math.hypot(Home[0]-location[0], (Home[1]*math.cos(Home[0]*math.pi/180)-location[1]*math.cos(location[0]*math.pi/180)))
    if n_wp==1:
        ## spending is the energy spent per distance travelled, and we give a safety factor of 2.5
        dist_total+=distance_home*111139
        spending=2.5*((Total_batteries_inicial-Takeoff_energy)-total_batery())/distance_home

if not returned:
    print 'Returning to Launch'
    RTL()     # Return to Launch point
    while True:
        if cs.landed:
            print 'Mission Complete'
            break
        velocities.append(cs.vlen)
        Script.Sleep(1000)

outputs()
