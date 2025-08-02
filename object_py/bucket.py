#
# Student ID: 20469160
# Student Name: W.M.Naradha
#
# cat.py - contains the object classes related to cat in the game of cats.
#

class Bucket():
    myclass = 'Bucket'
    def __init__(self,row,col,height=0.0):
        self.col = col              #Instance variable defines bucket column 
        self.row = row              #Instance variable defines bucket row 
        self.height = height        #Instance variable defines bucket height
        self.cats = []              #Instance variable defines cats in bucket
        self.landmarks = []         #Instance variable defines landmarks in buckets
        self.scents = [0,0,0,0,[False,0],[False,0]]     #Instance variable holds scent in the bucket each position holds a scent of a differen object type

    def add(self,obj):  #adding objects into the bucker.
        if obj.myclass == 'Cat':    #adding cats
            #if len(self.landmarks) > 0:
                #print(self.landmarks[0].ltype,self.landmarks[0].cat_in)
            self.cats.append(obj)
            if obj.gender=='Male':
                self.scents[4][1]=obj.scent #updating scents
            elif obj.gender == 'Female':
                self.scents[5][1]=obj.scent #updating scents
        elif obj.myclass == 'Landmark': #adding landmarks
            if obj.ltype == 'water':    #adding the landmark and updating that specific scent
                self.landmarks.append(obj)
                self.scents[1]=obj.scent()
            elif obj.ltype == 'food':
                self.landmarks.append(obj)
                self.scents[0]=obj.scent()
            elif obj.ltype == 'box':
                self.landmarks.append(obj)
                self.scents[2]=obj.scent()
            elif obj.ltype == 'bed':
                self.landmarks.append(obj)
                self.scents[3]=obj.scent()


    def remove(self,obj):   #removing an object from the bucket
        if obj.myclass=='Cat':
            self.cats.remove(obj)
            return(True)
        elif obj.myclass=='Landmark':
            self.landmarks.remove(obj)
        else:
            return(False)

    def scent(self):    #returning the scents as a function
        return(self.scents)

    def update_scents(self,old_buckets,simtype,simcon): #Updating scents based on the scent propagation model for the objects
        grid_fscent = 0
        grid_dscent = 0
        grid_boxscent = 0
        grid_bedscent = 0
        grid_mcscent = 0
        grid_fcscent = 0
        no_water_source = False
        no_food_source = False
        cant_move = False
        if sum(simcon[1])==0:      #Idnetifiying if the sources are there
            no_water_source = True
        else:
            no_water_source = False
        if sum(simcon[0])==0:
            no_food_source = True
        else:
            no_food_source = False
        for r in range(len(old_buckets)):   #checking the intensity of the scents on the previous step
            cant_move = False
            bucket = old_buckets[r]
            if abs(self.height - bucket.height) > 3:
                cant_move = True
            else:
                cant_move = False
            fDir = self.directional_checker(simtype,old_buckets,'food')
            dDir = self.directional_checker(simtype,old_buckets,'water')
            bDir = self.directional_checker(simtype,old_buckets,'bed')
            boxDir = self.directional_checker(simtype,old_buckets,'box')
            #print('Food: ',fDir,' Water: ',dDir,' Bed: ',bDir,' Box: ',boxDir)
            if old_buckets[r].scents[0] > grid_fscent and cant_move==False:  #update scent for food
                if old_buckets[r].occupiedby()[0] == True:
                    if old_buckets[r].occupiedby()[1].myclass == 'Landmark':
                        if old_buckets[r].occupiedby()[1].ltype == 'food':
                            if r in fDir[0]:
                                grid_fscent = 0.95 * fDir[1]
                            elif r not in fDir[0]:
                                grid_fscent = grid_fscent
                else:
                    grid_fscent = 0.7*old_buckets[r].scents[0]
                if no_food_source == True:
                    grid_fscent = 0
            if old_buckets[r].scents[1] > grid_dscent and cant_move==False:  #update scent for water
                if old_buckets[r].occupiedby()[0] == True:
                    if old_buckets[r].occupiedby()[1].myclass == 'Landmark':
                        if old_buckets[r].occupiedby()[1].ltype == 'water':
                            if r in dDir[0]:
                                grid_dscent = 0.95 * dDir[1]
                            elif r not in dDir[0]:
                                grid_dscent = grid_dscent
                else:
                    grid_dscent = 0.7 * old_buckets[r].scents[1]
                if no_water_source == True:
                    grid_dscent = 0
            if old_buckets[r].scents[2] > grid_boxscent and cant_move==False:    #update scent for box
                if old_buckets[r].occupiedby()[0] == True:
                    if old_buckets[r].occupiedby()[1].myclass == 'Landmark':
                        if old_buckets[r].occupiedby()[1].ltype == 'box':
                            if r in boxDir[0]:
                                grid_boxscent = 0.95 * boxDir[1]
                            elif r not in boxDir[0]:
                                grid_boxscent = grid_boxscent
                else:
                    grid_boxscent = 0.7 * old_buckets[r].scents[2]
            if old_buckets[r].scents[3] > grid_bedscent and cant_move==False:
                if old_buckets[r].occupiedby()[0] == True:  #update scent for bed
                    if old_buckets[r].occupiedby()[1].myclass == 'Landmark':
                        if old_buckets[r].occupiedby()[1].ltype == 'bed':
                            if r in bDir[0]:
                                grid_bedscent = 0.95 * bDir[1]
                            elif r not in bDir[0]:
                                grid_bedscent = grid_bedscent
                else:
                    grid_bedscent = 0.7 * old_buckets[r].scents[3]
            if simtype == 'Moore' and cant_move==False:  #updating the new bucket cat scents based on the simulation type.
                if r == 4:
                    if self.scents[4][0] == True:
                        grid_mcscent = 0.95*old_buckets[r].scents[4][1]
                        if grid_mcscent < 0.05:
                            grid_mcscent = 0.2*old_buckets[r].scents[4][1]
                            self.scents[4][0] = False
                    else:
                        if grid_mcscent/0.2 < old_buckets[r].scents[4][1]:
                            grid_mcscent = 0.2*old_buckets[r].scents[4][1]
                    if self.scents[5][0] == True:
                        grid_fcscent = 0.95*old_buckets[r].scents[5][1]
                        if grid_fcscent < 0.05:
                            grid_fcscent = 0.2*old_buckets[r].scents[5][1]
                            self.scents[5][0] = False
                    else:
                        if grid_fcscent < old_buckets[r].scents[4][1]:
                            grid_fcscent = 0.2*old_buckets[r].scents[5][1]
                else:
                    if grid_mcscent/0.2 < old_buckets[r].scents[4][1]:
                            grid_mcscent = 0.2*old_buckets[r].scents[4][1]
                    if grid_fcscent/0.2 < old_buckets[r].scents[5][1]:
                            grid_fcscent = 0.2*old_buckets[r].scents[5][1]
            elif cant_move==False:
                if r == 2:
                    if self.scents[4][0] == True:
                        grid_mcscent = 0.9*old_buckets[r].scents[4][1]
                        if grid_mcscent < 0.05:
                            grid_mcscent = 0.2*old_buckets[r].scents[4][1]
                            self.scents[4][0] = False
                    else:
                        if grid_mcscent/0.2 < old_buckets[r].scents[4][1]:
                            grid_mcscent = 0.2*old_buckets[r].scents[4][1]
                    if self.scents[5][0] == True:
                        grid_fcscent = 0.9*old_buckets[r].scents[5][1]
                        if grid_fcscent < 0.05:
                            grid_fcscent = 0.2*old_buckets[r].scents[5][1]
                            self.scents[5][0] = False
                    else:
                        if grid_fcscent/0.2 < old_buckets[r].scents[4][1]:
                            grid_fcscent = 0.2*old_buckets[r].scents[5][1]
                else:
                    if grid_mcscent/0.2 < old_buckets[r].scents[4][1]:
                            grid_mcscent = 0.2*old_buckets[r].scents[4][1]
                    if grid_fcscent/0.2 < old_buckets[r].scents[5][1]:
                            grid_fcscent = 0.2*old_buckets[r].scents[5][1]
            self.scents[0] = (grid_fscent)
            self.scents[1] = (grid_dscent)
            self.scents[2] = (grid_boxscent)
            self.scents[3] = (grid_bedscent)
            if grid_mcscent < 0.05:
                self.scents[4][1] = 0
            else:
                self.scents[4][1] = (grid_mcscent)
            if grid_fcscent < 0.05:
                self.scents[5][1] = 0
            else:
                    self.scents[5][1] = (grid_fcscent)
        if self.occupiedby()[0]==True and self.occupiedby()[1].myclass=='Landmark': #setting scent to sourec scent if source is in bucket
            if self.occupiedby()[1].ltype=='food':
                self.scents[0] = self.occupiedby()[1].scent()
            elif self.occupiedby()[1].ltype=='water':
                self.scents[1] = self.occupiedby()[1].scent()
            elif self.occupiedby()[1].ltype=='box':
                self.scents[2] = self.occupiedby()[1].scent()
            elif self.occupiedby()[1].ltype=='bed':
                self.scents[3] = self.occupiedby()[1].scent()
                if self.occupiedby()[1].cat_in == True:
                    if self.occupiedby()[2].gender == 'Male':
                        self.scents[4][1] = self.occupiedby()[2].scent
                        self.scents[4][0] = True
                    elif self.occupiedby()[2].gender == 'Female':
                        self.scents[5][1] = self.occupiedby()[2].scent
                        self.scents[5][0] = True
        if self.occupiedby()[0]==True and self.occupiedby()[1].myclass=='Cat':  #setting scent to sourec scent if source is in bucket
            if self.occupiedby()[1].gender == 'Male':
                self.scents[4][0] = True
                self.scents[4][1] = self.occupiedby()[1].scent
            elif self.occupiedby()[1].gender == 'Female':
                self.scents[5][0] = True
                self.scents[5][1] = self.occupiedby()[1].scent


    def directional_checker(self,simtype,old_buckets,lt):   #Used in the cat object as well and same setup just modifieied to provide for the scent propagation.
        if simtype=='Moore':
            pos = 4
            N = 1
            NE = 0
            NW = 2
            E = 3
            W = 5
            S = 7
            SE = 6
            SW = 8
        elif simtype =='Neuman':
            pos = 2
            N = 0
            E = 1
            W = 3
            S = 4
        Dir = []
        sc = 0
        for bucket in old_buckets:
            if bucket.occupiedby()[0] == True:
                if bucket.occupiedby()[1].myclass == 'Landmark':
                    if bucket.occupiedby()[1].ltype == lt:
                        sc = bucket.occupiedby()[1].scent()
                        Dir_l = bucket.occupiedby()[1].direction
                        for i in range(len(Dir_l)):
                            if Dir_l[i] == 'all':
                                if simtype == 'Moore':
                                    Dir = [N, S, W, E, NE, NW, SE, SW]
                                elif simtype == 'Neuman':
                                    Dir = [N, S, W, E]
                            if Dir_l[i] == 'N':
                                Dir.append(S)
                            if Dir_l[i] == 'E':
                                Dir.append(W)
                            if Dir_l[i] == 'W':
                                Dir.append(E)
                            if Dir_l[i] == 'S':
                                Dir.append(N)
                            if simtype == 'Moore':
                                if Dir_l[i] == 'NW':
                                    Dir.append(SE)
                                if Dir_l[i] == 'NE':
                                    Dir.append(SW)
                                if Dir_l[i] == 'SW':
                                    Dir.append(NE)
                                if Dir_l[i] == 'SE':
                                    Dir.append(NW)
                    else:
                        Dir_l = []
        return ([Dir,sc])
    
    def update_object(self,stepsperday,timestep,neighbour_buckets,simtype,sim):
        for c in self.cats:
            c.update_cat(stepsperday,timestep,neighbour_buckets,simtype,sim)
        for l in self.landmarks:
            l.update_landmark(stepsperday)

    def occupiedby(self):
        if len(self.landmarks) > 0:
            if (self.landmarks[0].ltype == 'bed'):
                if self.landmarks[0].cat_in == True:
                    return([True,self.landmarks[0],self.cats[0]])
                else:
                    return([True,self.landmarks[0],None])
            elif self.landmarks[0].ltype == 'box':
                if len(self.cats)>0:
                    for cat in self.cats:
                        if cat.cps == True:
                            ct = cat
                            return([True,self.landmarks[0],ct])
                        else:
                            return([True,self.landmarks[0],None])
                else:
                    return([True,self.landmarks[0]])
            else:
                return([True,self.landmarks[0]])
        elif len(self.cats) > 0:
            return([True,self.cats[0]])
        else:
            return([False,None])


