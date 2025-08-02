import file_manager
from cat import *
from landmarks import *
from bucket import *
import numpy as np
from file_manager import *
import os

def save_log(self): #Saving the log generated in the simulation
    for i,line in enumerate(self.log):
        if i == 0:
            write_csv_profile(line,(str(self.name)+'log'+'.csv'),s='w+')
        else:
            write_csv_profile(line,(str(self.name)+'log'+'.csv'),s='a')

def save_sim(self): #Saving a simulation by taking individual objects and saving their profiles
    mp_path = ''
    if self.map_path != '':
        mp_path = self.name+'terrain.csv'
    profile = [str(self.myclass), str(self.name), str(self.simtype), str(self.stepsperday), str(self.maxrowcol[0]), str(self.maxrowcol[1]), str(self.timestep),mp_path, str(self.sattribute)]
    file_manager.write_csv_profile(profile, (str(self.name)+'.csv'), s='w+')
    if self.map_path != '':
        source = str(self.name)+'terrain.csv'
        file_manager.write_csv(self.map,source,s='w+')
    for cat in self.cats:
        if cat.fight == True:
            profile = [str(cat.myclass), str(cat.name), str(cat.gender), str(cat.dob), str(cat.loc[0]), str(cat.loc[1]), str(cat.hunger), str(cat.thirst),str(cat.tired), str(cat.stress), str(cat.scent), str(cat.dc), str(cat.eat), str(cat.drink), str(cat.rest), str(cat.ms), str(cat.conc), str(cat.conct), str(cat.ibt), str(cat.req), str(cat.fight), str(None), str(cat.lloc[0]), str(cat.lloc[1]), str(cat.cps), str(cat.cps_val), str(cat.boxpop)]
        else:
            profile = [str(cat.myclass), str(cat.name), str(cat.gender), str(cat.dob), str(cat.loc[0]), str(cat.loc[1]), str(cat.hunger), str(cat.thirst),str(cat.tired), str(cat.stress), str(cat.scent), str(cat.dc), str(cat.eat), str(cat.drink), str(cat.rest), str(cat.ms), str(cat.conc), str(cat.conct), str(cat.ibt), str(cat.req), str(cat.fight), str(None), str(cat.lloc[0]), str(cat.lloc[1]), str(cat.cps), str(cat.cps_val), str(cat.boxpop)]
        file_manager.write_csv_profile(profile, (str(self.name)+'.csv'), s='a')
    for lm in self.landmarks:
        profile = [str(lm.myclass),str(lm.name), str(lm.ltype), str(lm.quantity), str(lm.reset), str(lm.direction), str(lm.cat_in),str(lm.control_reset),str(lm.consume),str(lm.loc[0]),str(lm.loc[1])]
        file_manager.write_csv_profile(profile, (str(self.name)+'.csv'), s='a')
    for fight in self.fights:
        profile = ['Fight',str(fight.name),str(fight.cat_adv.name),str(fight.loc_adv.row),str(fight.loc_adv.col)]
        for cat in fight.cats:
            profile.append(cat[0].name)
        file_manager.write_csv_profile(profile, (str(self.name)+'.csv'), s='a')

def load_sim(name): #Loading a simulation by reading the saved csv profile.
    lines = read_csv_profile(name, s = 'r')
    for line in lines:
        if line[0] == 'Sim':
            mp = ''
            if line[7] != '':
                mp = line[1]+'terrain.csv'
            s = Sim(simname=line[1],simtype=line[2],stepsperday=int(line[3]),rows=int(line[4]),cols=int(line[5]),timestep=int(line[6]),map=mp,sattribute=line[8])
        if line[0] == 'Cat':
            e = False
            d = False
            r = False
            m = False
            cn = False
            fg = False
            cp = True
            if line[12] == 'True':  #Checking for the boolean type assigning varibales for them.
                e = True
            if line[13] == 'True':
                d = True
            if line[14] == 'True':
                r = True
            if line[15] == 'True':
                m = True
            if line[16] == 'True':
                cn = True
            if line[20] == 'True':
                fg = True
            if line[24] == 'True':
                cp = True
            c = Cat(name=line[1],gender=line[2],dob=float(line[3]),r=int(line[4]),c=int(line[5]), hunger=float(line[6]), thirst=float(line[7]), tired=float(line[8]),stress=float(line[9]), scent=float(line[10]), dc=float(line[11]), eat=e, drink=d, reset=r, ms=m, conc=cn, conct=float(line[17]), ibt=line[18],req=line[19],fight=fg, f_obj=None, rloc=int(line[22]), cloc=int(line[23]), cps=cp, cps_val=float(line[25]), pop=int(line[26]))
            s.add_cat(cat=c)
            s.add_grid(int(line[4]),int(line[5]),line[1],con=True)
        if line[0] == 'Fight':
            for cat in s.cats:
                if line[2] == cat.name:
                    f = Fight(line[1],cat,s.grid[int(line[3]),int(line[4])])
                    cat.f_obj = f
                    s.add_fight(f)
            for cat in s.cats:
                for i in range(5,len(line)-1):
                    if line[i] == cat.name:
                        f.cat_join(cat,s.grid[cat.loc[0],cat.loc[1]])
                        cat.fight = True
        if line[0] == 'Landmark':
            ci = False
            dr = []
            if line[5] == "['all']":
                dr = ['all']
            else:
                dirl = line[5].strip('[').strip(']').split(',')
                for d in dirl:
                    dr.append(d.strip("'"))
            if line[6] == 'True':
                ci = True
            try:
                lm = Landmark(name=line[1], ltype=line[2], quantity=float(line[3]), reset=int(line[4]), direction=dr, cat_in=ci, control_reset=float(line[7]), consume=float(line[8]),r=line[9],c=line[10])
            except exception as e:
                print('Exception Here')
            s.add_landmark(landmark=lm)
            s.add_grid(int(line[9]), int(line[10]),line[1],con=True)
    return(s)

class Sim():
    myclass = 'Sim'
    def __init__(self,simname,simtype,stepsperday,rows=0,cols=0,map='',timestep=0,sattribute=''):
        self.name=simname               #Instance variable simulation name.
        self.simtype=simtype            #Instance variable simulation type.
        self.stepsperday=stepsperday    #Instance vatiable simulation stepsperday.
        if map == '':                   #Generating the grid/terrain for a flat type map.
            self.map_type = 'Flat'
            self.map_path = map
            self.map = 0
            self.maxrowcol = [rows,cols]
            self.grid = self.gen_grid(self.maxrowcol[0],self.maxrowcol[1])
        else:                           #Generating the grid/terrain for an input terrain file based map.
            try:
                self.map_type = 'Terrain'
                self.map_path = map
                self.grid = self.gen_grid(map=read_csv(map, s='r',outarray=True,dt=float))
                self.map = read_csv(map, s='r',outarray=True,dt=float)
                self.maxrowcol = [self.grid.shape[0],self.grid.shape[1]]
            except Exception as e:
                print('Error in Sim Creation: ',e)
        self.timestep = timestep        #Instance variable providing the number of timesteps
        self.sattribute = sattribute    #Instance variable that has the show type declared for plotting
        self.cats = []                  #Instance variable list of cats in the simulation objects list
        self.landmarks = []             #Instance variable list of landmarks in the simulation objects list
        self.fights = []                #Instance variable list of fights in the simulation objects list
        self.objects = []               #Instance variable objects list of simulaiton.
        self.log = []                   #Instance variable containing simulated session log to be given as output.


    def add_cat(self,name='',gender='',dob=0,cat=None): #Adding cats to the object and cat list
        if cat != None:     #if input is a cat object
            self.cats.append(cat)
            self.objects.append(cat)
        elif cat == None:   #if input is cat atteibutes
            temp = Cat(name,gender,dob)
            self.cats.append(temp)
            self.objects.append(temp)
            return(temp)

    def add_fight(self,fight):  #Adding fights to the fights list
        self.fights.append(fight)

    def remove_fight(self,fight):   #Removing fights from the fight list
        self.fights.remove(fight)

    def add_landmark(self,name='',ltype='',quantity=0,reset=0,landmark=None,direction=['all']): #adding landmarks same as cats
        if landmark != None:
            self.landmarks.append(landmark)
            self.objects.append(landmark)
        elif landmark == None:
            temp = Landmark(name,ltype,quantity,reset,direction=direction)
            self.landmarks.append(temp)
            self.objects.append(temp)
            return(temp)
    
    def gen_grid(self,rows=0,cols=0,map=None):  #generating the grid based on whether an input terrain is given or not
        b = []
        if self.map_type == 'Flat':
            for row in range(rows):
                rl = []
                for col in range(cols):
                    rl.append(Bucket(row, col))
                b.append(rl)
            ba = np.array(b)
            return(ba)
        elif self.map_type == 'Terrain':
            for r,row in enumerate(map):
                rl = []
                for c,height in enumerate(row):
                    rl.append(Bucket(r, c, height=height))
                b.append(rl)
            ba = np.array(b)
            return(ba)

    def add_grid(self,row,col,temp,con=False):  #adding items in object list to map
        if (len(self.grid[row,col].cats) > 0 or len(self.grid[row,col].landmarks) > 0) and con==False:  #user cant input more than 1 item to the same cell
            return(False)
        else:
            for obj in self.objects:    #but the load function can
                if obj.name == temp:
                    self.grid[row,col].add(obj)
                    if obj.myclass == 'Cat':
                        obj.loc = [row,col]
                    elif obj.myclass == 'Landmark':
                        obj.loc = [row,col]
                    return(True)

    def remove_grid(self,row,col,temp): #remove item from grid
        for obj in self.objects:
            if obj.name == temp:
                self.grid[row,col].remove(obj)

    def run_step(self,att,gl):  #running a step of the code
        self.sattribute = att
        if gl == True:
            self.gen_log()
        self.timestep += 1
        self.update_grid_scent()
        self.simulate_step()
        return(self.show_step())

    def neighbour(self,row,col):    #generating the neighbourhood based on simtype:
        if self.simtype == 'Moore': #Moore neighbourhood
            neighbour_buckets = [self.grid[row - 1, col - 1], self.grid[row - 1, col], self.grid[row - 1, col + 1],self.grid[row, col - 1], self.grid[row, col], self.grid[row, col + 1],self.grid[row + 1, col - 1], self.grid[row + 1, col], self.grid[row + 1, col + 1]]
        elif self.simtype == 'Neuman':  #Neuman Neighbourhood
            neighbour_buckets = [self.grid[row - 1, col], self.grid[row, col - 1], self.grid[row, col],self.grid[row, col + 1], self.grid[row + 1, col]]
        return(neighbour_buckets)

    def gen_log(self):
        self.log.append([('########## Timestep :'+str(self.timestep)+' ##########')])
        for obj in self.cats:
            if obj.loc != [0,0]:
                profile = obj.cat_log(self)
                self.log.append(profile)
        for obj in self.landmarks:
            if obj.loc != [0,0]:
                profile = obj.lm_log(self)
                self.log.append(profile)

    def update_grid_scent(self):    #Updating the scents of the grid to the next timestep
        ngrid = self.grid.copy()
        wlist = []
        flist = []
        for obj in self.landmarks:  #landmarks
            if obj.ltype == 'water':
                wlist.append(obj.remaining())
            if obj.ltype == 'food' :
                flist.append(obj.remaining())
        for row in range(1,self.maxrowcol[0]-1):    #making the external boundary - and setting up the new scent
            for col in range(1,self.maxrowcol[1]-1):
                neighbour_buckets = self.neighbour(row,col)
                ngrid[row,col].update_scents(neighbour_buckets,self.simtype,[flist,wlist])  #updating it
        self.grid = ngrid.copy()

    def simulate_bucket(self,row,col):  #updating items in the bucket to the new time step
        ngrid = self.grid.copy()
        neighbour_buckets = self.neighbour(row, col)
        ngrid[row, col].update_object(self.stepsperday, self.timestep, neighbour_buckets, self.simtype,self)    #updating them
        self.grid = ngrid.copy()

    def simulate_step(self):    #calling the simulate_bucket for the entire grid.
        for row in range(1,self.maxrowcol[0]-1):
            for col in range(1,self.maxrowcol[1]-1):
                self.simulate_bucket(row,col)

    def show_step(self):
        sgrid = self.grid.copy()    #getting a copy of the simulation grid
        scent_grid = np.zeros((self.maxrowcol[0],self.maxrowcol[1]),dtype=float)    #grid for scents and terrain
        cell = [0, 0, 0]    
        showlist = [[cell] * self.maxrowcol[1]] * self.maxrowcol[0] #generating a grid of the shape required
        grid = np.array(showlist, dtype=int)    #the grid
        #print(grid.shape)
        if self.sattribute == 'ALL':
            for row in range(self.maxrowcol[0]):
                for col in range(self.maxrowcol[1]):
                    if sgrid[row,col].occupiedby()[0] == True:
                        #print((buckets[row][col].occupiedby()[1])[0].myclass)
                        if (sgrid[row,col].occupiedby()[1]).myclass == 'Cat':   #Assigning rgb colors for a cat
                            b = int(255 * (1 - (sgrid[row,col].occupiedby()[1]).thirst)) #blue rep - thirst
                            g = int(255 * (1 - (sgrid[row,col].occupiedby()[1]).hunger)) #green rep - hunger
                            r = int(255 * (1 - (sgrid[row,col].occupiedby()[1]).tired))  #red rep - fatigue
                            grid[row, col] = np.array([r, g, b], dtype=int)
                            #print('Cat at :', row, ' ,', col, '|', r, ',', g, ',', b, '|')
                        elif (sgrid[row,col].occupiedby()[1]).myclass == 'Landmark':
                            if (sgrid[row,col].occupiedby()[1]).ltype == 'water':
                                b = int(255 * (sgrid[row,col].occupiedby()[1]).scent()) #for water sources
                                grid[row, col] = np.array([0, 0, b], dtype=int)
                                #print('Water at :',row,' ,',col ,'| colour = ',b)
                            elif (sgrid[row,col].occupiedby()[1]).ltype == 'food':
                                g = int(255 * (sgrid[row,col].occupiedby()[1]).scent()) #for food sources
                                grid[row, col] = np.array([0, g, 0], dtype=int)
                                #print('Food at :',row,' ,',col ,'| colour = ',g)
                            elif (sgrid[row,col].occupiedby()[1]).ltype == 'bed':
                                if len(sgrid[row,col].cats) == 0:
                                    r = int(255 * (sgrid[row,col].occupiedby()[1]).scent()) #for a bed
                                    grid[row, col] = np.array([r, 0, 0], dtype=int)
                                    #print('Food at :',row,' ,',col ,'| colour = ',g)
                                elif len(sgrid[row,col].cats) > 0:                          #a bed which is occupied by a cat
                                    b = int(255 * (1 - (sgrid[row, col].cats[0]).thirst))
                                    g = int(255 * (1 - (sgrid[row, col].cats[0]).hunger))
                                    r = int(255 * (1 - (sgrid[row, col].cats[0]).tired))
                                    grid[row, col] = np.array([r, g, b], dtype=int)
                                    #print('Food at :',row,' ,',col ,'| colour = ',g)
                            elif (sgrid[row,col].occupiedby()[1]).ltype == 'box':       #for a box
                                if len(sgrid[row,col].cats) == 0:
                                    r = int(255 * (sgrid[row,col].occupiedby()[1]).scent())
                                    grid[row, col] = np.array([r, r, 0], dtype=int)
                                    #print('Food at :',row,' ,',col ,'| colour = ',g)
                                elif len(sgrid[row,col].cats) > 0:  
                                    ps = False
                                    for cat in sgrid[row,col].cats: #Box occupied by a parent cat.
                                        if cat.cps == True:
                                            ps = True
                                            b = int(255 * (1 - cat.thirst))
                                            g = int(255 * (1 - cat.hunger))
                                            r = int(255 * (1 - cat.tired))
                                            grid[row, col] = np.array([r, g, b], dtype=int)
                                            #print('Food at :',row,' ,',col ,'| colour = ',g)
                                    if ps == False:                 
                                        grid[row, col] = np.array([0, 255, 255], dtype=int)
                    else:
                        grid[row, col] = np.array([0, 0, 0], dtype=int)
            return(grid)
        elif self.sattribute == 'Terrain' and self.map_path != '':  #Providing the terrain map
            mn = self.map.min()
            m = 130/(self.map.max()-self.map.min())
            #print(mn,m)
            for row in range(self.maxrowcol[0]):
                for col in range(self.maxrowcol[1]):
                    b = int(m*(self.map[row,col]-mn))+125
                    scent_grid[row,col] = b
            return(scent_grid)
        #generating the scent maps for the cat
        elif self.sattribute == 'Cat-Scent' or self.sattribute == 'Food-Scent' or self.sattribute == 'Water-Scent' or self.sattribute == 'Bed-Scent' or self.sattribute == 'Box-Scent':
            return(self.show_scent(self.sattribute))
        else:
            return(None)

    def show_scent(self,att):
        scent_grid = np.zeros((self.maxrowcol[0],self.maxrowcol[1]),dtype=float)    #Generating the scent grid
        cell = [0, 0, 0]
        showlist = [[cell] * self.maxrowcol[1]] * self.maxrowcol[0] #For cat scents generating the grid
        cat_scent_grid = np.array(showlist, dtype=int)
        for row in range(self.maxrowcol[0]):
            for col in range(self.maxrowcol[1]):
                if self.sattribute == 'Cat-Scent':
                    b = int(255 * (self.grid[row,col].scents[5][1]/1.4))    #blue for female cats
                    r = int(255 * (self.grid[row,col].scents[4][1]/1.4))    #red for male cats
                    cat_scent_grid[row, col] = np.array([r, 0, b], dtype=int)
                elif self.sattribute == 'Food-Scent':
                    scent_grid[row, col] = float(self.grid[row, col].scents[0]) #Scent of food
                elif self.sattribute == 'Water-Scent':
                    scent_grid[row, col] = float(self.grid[row, col].scents[1]) #Scent of water
                elif self.sattribute == 'Bed-Scent':
                    scent_grid[row, col] = float(self.grid[row, col].scents[3]) #Scent of bed
                elif self.sattribute == 'Box-Scent':
                    scent_grid[row, col] = float(self.grid[row, col].scents[2]) #Scent of box
        if self.sattribute == 'Cat-Scent':  #returning the correct grid
            return(cat_scent_grid)
        else:
            return(scent_grid)

