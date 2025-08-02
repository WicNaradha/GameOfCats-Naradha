#
# Student ID: 20469160
# Student Name: W.M.Naradha
#
# cat.py - contains the object classes related to cat in the game of cats.
#

import random
import numpy as np

class Cat():
    myclass = 'Cat'             #Class Variable: Defining object type.
    fpd = [4,3,2]               #Class Variable: Defines the amount of food per day for a kitten, adult and old cat.
    dpd = [4,6,5]               #Class Variable: Defines the amount of drinks per day for a kitten, adult and old cat.
    rpd = [4,2,3]               #Class Variable: Defines the amount of rest per day for a kitten, adult and old cat.
    ls = [320,3650,5475]        #Class Variable: The age zones of a kitten < 320 days, cat in prime < 3650 and old cat when > 3650. The highest life expectancies are around 5475.
    heatspan = [25,35]          #Class Variable: Female cats sexual scent intensity change increases for 25 days and after 35 the scent will reset.
    e_time = 15                 #Class Variable: Time taken to eat food in minutes
    d_time = 3                  #Class Variable: Time taken to drink water in minutes
    def __init__(self,name,gender,dob,r=0,c=0, hunger=0.0, thirst=0.0, tired=0.0,stress=0.0 , scent=0.0, dc=0.0, eat=False, drink=False, reset=False, ms=False, conc=False, conct=0, ibt='',req='',fight=False, f_obj=None, rloc=0, cloc=0, cps=False, pop=0, cps_val=0.0):
        self.name = name            #Instance variable: Provides an identifier to the respective cat.
        self.gender = gender        #Instance variable: Provides the gender of the Cat.
        self.dob = int(dob)         #Instance variable: Provides the dob relative to the start of the program.
        self.c_age = 0              #Instance variable: Inorder to make sure the cat updated has not already been updated.
        self.loc = [r,c]            #Instance variable: Defines the current location of the cat.
        self.hunger = hunger        #Instance variable: Defines the hunger of the cat during the given time step.
        self.thirst = thirst        #Instance variable: Defines the thirst of the cat during the given time step.
        self.tired = tired          #Instance variable: Defines the fatigue of the cat during the given time step.
        self.stress = stress        #Instance variable: Defines the stress of the cat during the given time step.
        self.scent = scent          #Instance variable: Defines the sexual scent of the cat during the given time step.
        self.dc = 0.1               #Instance variable: Defines the chance of death of the cat during the given time step. (needs further development not implemented entirely)
        self.eat = eat              #Instance variable: True when the cat is interacting with food.
        self.drink = drink          #Instance variable: True when the cat is interacting with drink.
        self.rest = reset           #Instance variable: True when the cat is interacting with bed and boxes.
        self.ms = ms                #Instance variable: True when the cat is mating with another cat.
        self.conc = conc            #Instance variable: True when a female cat has conceived.
        self.conct = conct          #Instance variable: Describes how long for the female cat to give birth to a litter of kittens.
        self.ibt = ibt              #Instance variable: Describes the interacting landmark/bucket type.
        self.req = req              #Instance variable: Defines the requirment at the moment for the Cat.
        self.fight = fight          #Instance variable: True if the cat is in a fight.
        self.f_obj = f_obj          #Instance variable: Assigned with the fight object the cat is the advantage cat of.
        self.lloc = [rloc,cloc]     #Instance variable: Provides the location of the litter box after giving birth to the litter.
        self.boxpop = pop           #Instance variable: The population of kittens in the litter box.
        self.cps = cps              #Instance variable: True if the female cat is a parent.
        self.cps_val = cps_val      #Instance variable: Defines when the female cat should check on the kittens in the litter box again.

    def update_cat(self,stepsperday,timestep,neighbour_buckets,simtype,sim): #The function called by the bucket to update the cat for the current time step.
        self.ibt = ''
        win = ''
        if simtype=='Moore': #Depending on the simulation type the position of the cat in the neighbour hood changes. It is in bucket 4 in Moore and 2 in Neuman.
            pos = 4
        elif simtype =='Neuman':
            pos = 2
        if self.u_age(timestep,stepsperday)!=self.c_age: #Checking if the cat was already updated, to make sure the cat is not updated twice.
            self.c_age = self.u_age(timestep,stepsperday)
            #print(self.name,self.c_age)
            if self.death(neighbour_buckets[pos],timestep,stepsperday) == True: #Simulating the death of the cat under the given conditions. 
                pass
            else:
                in_box = False
                self_bucket = neighbour_buckets[pos] #current bicket
                if len(self_bucket.landmarks) > 0:
                    if self_bucket.occupiedby()[1].ltype == 'box':  #checking if it is a box.
                        in_box = True
                #print(timestep/stepsperday,self.name,self.hunger,self.thirst,self.tired)
                if self.fight == True: #If in a fight and is the advantage cat to start the fight.
                    if self.f_obj != None: #If is the advantage cat
                        if self.f_obj.cat_adv.name == self.name: #Implemented to stop adversive effects due to ghosting and cramming effects in cat fight simulations.
                            win = self.f_obj.cats_fight(stepsperday,timestep,sim)
                        else:
                            self.fight = False
                            self.f_obj = None
                    else: #If not an advantage cat.
                        win = 'F'
                else: #If not in fight mode.
                    self.CIBS(neighbour_buckets,stepsperday,timestep)           #Cat Interest/Requirment Based on stress.
                    self.CIncO(neighbour_buckets,stepsperday,timestep,simtype)  #Cat Interaction with non-cat objects in the neighbourhood.
                if self.conc == True:   #If the cat has conceived
                    self.conc_update(neighbour_buckets,simtype,stepsperday,timestep,sim)    #Update the conct and conc status 
                if self.cps == True:    #If the cat is a parent
                    self.cps_update(timestep,stepsperday,neighbour_buckets[pos],sim)    #Update cps_val and cps status
                if self.ibt != 'water': #Update based on whether the cat is interacting with water.
                    self.thirst_calc(stepsperday,timestep,in_box)
                if self.ibt != 'food':  #Update based on whether the cat is interacting with food.
                    self.hunger_calc(stepsperday,timestep,in_box)
                self.tired_calc(stepsperday,timestep)   #Update the fatigue level of the cat
                self.scent_calc(stepsperday,timestep)   #Update the intesity of the sexual scent of the cat
                self.stress_calc(stepsperday)           #Update the stress of the cat
                self.death_chance(stepsperday,timestep) #Update the death chance of the cat
                if (self.eat==False and self.rest==False and self.drink==False and self.ms==False) and (win!='F' and win!='W' and win!='L'): #Conditions to check for before moving to a new cell.
                    self.move_cat(neighbour_buckets,simtype,stepsperday,timestep,win,pos,sim)
        
    def u_age(self,timestep,stepsperday):
        return(float(timestep/stepsperday)-self.dob) #Calculating current age in float (used to ensure cat is already upadated or not)

    def age(self,timestep,stepsperday):
        return(int(timestep/stepsperday)-self.dob)  #Calculated age in days.

    def jump(self,timestep,stepsperday):    #Jump height of the cat based on age.
        jump = 1
        if self.c_age < self.ls[0]: #if a kitten
            jump = 1
        elif self.c_age < self.ls[1]: #if in the prime
            jump = 3
        elif self.c_age < self.ls[2]: #old cat
            jump = 2.75
        elif self.c_age > self.ls[2]: #at end of life
            jump = 2.5
        return(jump)

    def hunger_calc(self,stepsperday,timestep,in_box): #Updating the hunger attribute of the cat.
        if self.hunger <= 0.5:  #Hunger level (It is as if the cats stomach is empty at 0.5)
            self.hunger += 2*(1/stepsperday)
        elif self.hunger > 0.5: #Hunger level when the cat is burning mustle to survive.
            hc = 0
            if self.c_age < self.ls[0]:# and in_box == False: #Hunger function for kittens.
                hc = (((6**0.5)/self.ls[0])*self.c_age**2)+3 #original model
                #hc = 1/7
            elif self.c_age < self.ls[1] and self.c_age > self.ls[0]: #Hunger for cats in their prime.
                hc = 9-(3/(3650-self.c_age))
            elif self.c_age == self.ls[1]:  #At the boundry.
                hc = 9
            elif self.c_age > self.ls[2]:   #During end of life stages.
                hc = 6-(2/(self.c_age-5475))
            elif self.c_age > self.ls[1]:   #During old age.
                hc = 9-(3/(self.c_age-3650))
            if hc > 0:
                self.hunger += (0.5/(hc-0.25))*(1/stepsperday)
            elif hc == 0:
                self.hunger = 0.5
        if self.hunger > 1: #making sure it does not go negative.
            self.hunger = 1
        return(self.hunger)


    def thirst_calc(self,stepsperday,timestep,in_box): #Updating the thirst attribute of the cat - same logic as of hunger.
        if self.thirst <= 0.5:
            self.thirst += (2.5)*(1/stepsperday)
        elif self.thirst > 0.5:
            tc = 0
            if self.c_age < self.ls[0]:# and in_box == False: #Hunger function for kittens.
                tc = (((6**0.5)/self.ls[0])*self.c_age**2)+2.5 #original model
                #tc = 1/7
            elif self.c_age < self.ls[1] and self.c_age > self.ls[0]:
                tc = 5-(1/(3650-self.c_age))
            elif self.c_age == self.ls[1]:
                tc = 5
            elif self.c_age > self.ls[2]:
                tc = 4-(0.5/(self.c_age-5475))
            elif self.c_age > self.ls[1]:
                tc = 5-(1/(self.c_age-3650))
            if tc > 0:
                self.thirst += (0.5/(tc-0.20))*(1/stepsperday)
            elif tc == 0:
                self.thirst = 0.5
        if self.thirst > 1: #making sure it does not go negative.
            self.thirst = 1
        return(self.thirst)


    def tired_calc(self,stepsperday,timestep): #Updating the fatigue attribute of the cat - same logic as of hunger (But the attribute is also updated when the cat is in rest).
        if self.rest == False: #Increasing fatigue if the cat is not in rest.
            if self.tired <= 0.5:   #Initial limit per day.
                self.tired += (2/3)*(1/stepsperday)
            elif self.tired > 0.5:  #Tolerance before reaching maximum fatigue level
                if self.c_age < self.ls[0]: # for kitten
                    tiredc = (((6**0.5)/self.ls[0])*self.c_age**2)+2 #old model
                    #print(tiredc)
                    #tiredc = 1/7
                elif self.c_age < self.ls[1]: # for adult cat in prime
                    tiredc = 3-(1/(3650-self.c_age))
                elif self.c_age == self.ls[1]: # for cat at prime
                    tiredc = 3
                elif self.c_age > self.ls[2]: # for cat at end of life
                    tiredc = 2.5-(0.5/(self.c_age-5475))
                elif self.c_age > self.ls[1]: # for cat in old age
                    tiredc = 3-(1/(self.c_age-3650))
                self.tired += (0.5/(tiredc-0.75))*(1/stepsperday)
            if self.tired > 1:
                self.tired = 1
            return(self.tired)
        elif self.rest == True: #Decreasing fatigue if cat is in rest.
            tired = 2*(1/stepsperday)
            if (self.tired - tired) < 0: #making sure it does not go negative.
                self.tired = 0
                self.rest = False
            else:
                self.tired += -tired
            return(self.tired)

    def scent_calc(self,stepsperday,timestep):  #Updates the intesity of the cats sexual scent.
        if self.gender == 'Female': #if female
            if self.scent>1.4: #checking if the cat is in the heatspan period before going out of heat
                self.scent = 0 #if out of heat
            else: 
                sc = 1/(self.heatspan[0]*stepsperday) #if in heat
                self.scent += sc
        elif self.gender == 'Male': #if male unlike the female cat the scent will not reset at given heat spans.
            sc = 1/(self.heatspan[0]*stepsperday)
            self.scent += sc
            if self.scent>1.4:
                self.scent = 1.4
            else:
                self.scent = self.scent
        if self.conc == True:
            self.scent = 0
        if self.cps == True:
            self.scent = 0
        if self.c_age < self.ls[0]:
            self.scent = 0
        return(self.scent)

    def stress_calc(self,stepsperday):  #cat stress is modeled based on hunger, thirst and fatigue; while if the cat is in a fight or a parent also effect the stress.
        if self.fight == True: #in a fight amplified stress.
            st = ((self.hunger)+(self.thirst)+(self.tired))/3 #Real stress value
        elif self.cps == True: #as a parent amplified stress.
            st = 2*((self.hunger)+(self.thirst)+(self.tired))/3 #Real stress value
        else: #In other cases
            st = ((self.hunger**2)+(self.thirst**2)+(self.tired**2))/3 #in normal circumstances (very low stress)
        if self.stress < st: #Modulation of apparent stress to real stress. (The apparent stress is how the cat perceives the stress, while the real stress is the actual stress induced at that moment)
            if (self.stress + st*(5/stepsperday)) > 1:
                self.stress = 1
            elif (self.stress + st*(5/stepsperday)) < 1:
                self.stress += st
        return(st)

    def dom_score(self,stepsperday,timestep):   #Provides the cats dominance score based on the age of the cat
        age = self.c_age
        if age <= 2190: #The prime age of the cat is taken as 2190 days.
            ds=((2190**2)-((age-2190)**2))/(2190**2)
        elif age > 2190: #The after the prime age
            ds=1-(4/29565)*age
        return(ds)
    
    def death_chance(self,stepsperday,timestep): #death chance modulation (only used to simulate death of end of life cats, as otherwise would kill all the cats.)
        if self.c_age < self.ls[0]:
            self.dc = 0.0005
        elif self.c_age < self.ls[1]:
            self.dc = 0.002
        elif self.c_age > self.ls[2]:
            self.dc = 0.002 + ((self.c_age-self.ls[2])**2)
        if self.hunger >= 0.9:
            self.dc += (0.038/(5*stepsperday))
        if self.thirst >= 0.9:
            self.dc += (0.038/(5*stepsperday))
        return(self.dc)

    def death(self,bucket,timestep,stepsperday): #Occuring of death based on death chance, starvatio or fatigue.
        death = random.random()
        if (self.hunger == 1 or self.thirst == 1 or self.tired == 1):# and (self.age(timestep,stepsperday) > self.ls[0]):
            bucket.remove(self)
            print(self.hunger,self.tired,self.thirst)
            print(self.name,' ',timestep,' ',self.c_age,' died due to natural causes.')
            return(True)
        if self.dc < death and self.c_age > self.ls[2]:
            bucket.remove(self)
            print(self.name,self.dc,' died due to old age.')
            return(True)
        #if self.dc < death and self.age(timestep,stepsperday) < self.ls[1]/3:
        #    bucket.remove(self)
        #    print(self.name,self.dc,' died due as a kitten age.')
        #    return(True)

    def directional_checker(self,simtype,bucket,lt): #Checking the direction of approach to directional landmarks
        if simtype=='Moore': #Assigning the bucket numbers of the directions depending on Moore.
            pos = 4
            N = 1
            NE = 0
            NW = 2
            E = 3
            W = 5
            S = 7
            SE = 6
            SW = 8
        elif simtype =='Neuman': #Assigning the bucket numbers of the directions depending on Neuman.
            pos = 2
            N = 0
            E = 1
            W = 3
            S = 4
        Dir = []
        if bucket.occupiedby()[0] == True:
            if bucket.occupiedby()[1].myclass == 'Landmark': #Checking if the bucket is occupied and wht is the type of the landmark it is occupied by.
                if bucket.occupiedby()[1].ltype == lt:
                    Dir = []
                    Dir_l = bucket.occupiedby()[1].direction
                    for i in range(len(Dir_l)): #Conditions to identify the direction for the landmark. If the landmark direction is North for the cat it should be on the South.
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
        return (Dir)


    def CIncO(self,neighbour_buckets,stepsperday,timestep,simtype): #Cat Interaction non cat Object
        self.ibt = ''
        if simtype == 'Moore':  #Assigning the current bucket of the cat based on the simualtion type.
            self_bucket = neighbour_buckets[4]
        elif simtype == 'Neuman':
            self_bucket = neighbour_buckets[2]
        for i,bucket in enumerate(neighbour_buckets):   #Going through all the neighbouring buckets to identify objects to interact with.
            fDir = self.directional_checker(simtype, bucket, 'food')    #Identifying if the cat is in the correct direction.
            dDir = self.directional_checker(simtype, bucket, 'water')   #Identifying if the cat is in the correct direction.
            bDir = self.directional_checker(simtype, bucket, 'bed')     #Identifying if the cat is in the correct direction.
            boxDir = self.directional_checker(simtype, bucket, 'box')   #Identifying if the cat is in the correct direction.
            if bucket.occupiedby()[0] == True:
                if bucket.occupiedby()[1].myclass == 'Landmark':    #Checking if the bucket is occupied by a landmark.
                    #Check conditions to interact with food.
                    if (self.req == 'food' and bucket.occupiedby()[1].ltype=='food' and bucket.occupiedby()[1].remaining()>0 and (i in fDir)) or (self.hunger > 0 and bucket.occupiedby()[1].ltype=='food' and self.eat==True and (i in fDir)):
                        self.eat = True
                        self.eat_drink_sim(bucket.occupiedby()[1],stepsperday,timestep,self_bucket)
                        self.ibt = bucket.occupiedby()[1].ltype
                    #Check conditions to interact with water.
                    elif (self.req == 'water' and bucket.occupiedby()[1].ltype=='water' and bucket.occupiedby()[1].remaining()>0 and (i in dDir)) or (self.thirst > 0 and bucket.occupiedby()[1].ltype=='water' and self.drink==True and (i in dDir)):
                        self.drink = True
                        self.eat_drink_sim(bucket.occupiedby()[1],stepsperday,timestep,self_bucket)
                        self.ibt = bucket.occupiedby()[1].ltype
                #In the scenaroi of mating with a cat.
                elif self.req=='cs' and bucket.occupiedby()[1].myclass == 'Cat':
                    if bucket.occupiedby()[1].name!=self.name:
                        if bucket.occupiedby()[1].scent > 0.7 and self.ms != True:  #Inorder to initiate a possible mating opportunity.
                            if simtype == 'Moore':
                                curr_bucket=neighbour_buckets[4]
                            else:
                                curr_bucket=neighbour_buckets[2]
                            cat_bucket=bucket
                            cat=cat_bucket.occupiedby()[1]
                            self.m_chall(cat,stepsperday,timestep,cat_bucket,curr_bucket)   #Sending a mating request.
                            self.ibt = bucket.occupiedby()[1].myclass
                        if self.ms==True and bucket.occupiedby()[1].ms == True: #Commiting to mate if the above mating request sent in previous time step was accpeted.
                            if simtype == 'Moore':
                                curr_bucket=neighbour_buckets[4]
                            else:
                                curr_bucket=neighbour_buckets[2]
                            cat_bucket=bucket
                            cat=cat_bucket.occupiedby()[1]
                            self.mate_w(cat,stepsperday,timestep,cat_bucket,curr_bucket)    #Where the magic happens! - The function that simulates the interaction.
            if self.cps != True:    #Reseting hunger and thirst if the parent cat is back in the box.
                if self_bucket.occupiedby()[0] == True:
                    if self_bucket.occupiedby()[1].myclass=='Landmark':
                        if self_bucket.occupiedby()[1].ltype == 'box':
                            #print(self.name)
                            for cat in self_bucket.cats:
                                #print(cat.cps == True and self.name!=cat.name)# and self.age(timestep,stepsperday) < self.ls[0])
                                if cat.cps == True and self.name!=cat.name:# and self.age(timestep,stepsperday) < self.ls[0]: # Conditional to reset kitten hunger,thirst and fatigue
                                    self.hunger = 0
                                    self.thirst = 0
                                    self.tired = 0
                                    self.rest = True
                                #elif self.age(timestep,stepsperday) > self.ls[0]:
                                #    print(self.name)
                                #    #self.req = ''
                                #    self.rest = False

    def CIBS(self,neighbour_buckets,stepsperday,timestep): #Cat Interest Based On Stress
        st = random.random() #Value taken in random to reset the requirment.
        wup = True
        fup = True
        dup = True
        if self.rest == True and self.tired > 0.05: #Giving a buffer region for a cat to wake up.
            wup = False
        if self.eat == True and self.hunger > 0.025: #Giving a buffer for the hunger level. 
            fup = False
        if self.drink == True and self.thirst > 0.025: #Giving a buffer for th thirst level.
            dup = False
        if (self.req!='box')and ((st < self.stress and wup==True and dup==True and fup==True) or (st < self.stress and self.eat==False and self.drink==False and self.rest==False)):
            if self.thirst >= 0.65: #thirst level is too high setting req to thirst.
                self.req = 'water'
            elif self.hunger >= 0.65: #hunger level is too high setting req to food
                self.req = 'food'
            elif self.tired >= 0.65:  #fatigue level is too high setting req to fatigue
                self.req = 'bed'
            else:
                req = random.random()
                if req < (self.thirst/3):   #randomly set the req to water
                    self.req = 'water'
                elif req < ((self.thirst+self.hunger)/3):   #randomly set the req to food
                    self.req = 'food'
                elif req < ((self.thirst+self.hunger+self.tired)/3):    #randomly set the req to rest
                    self.req = 'bed'
                elif req < 1 and ((self.scent > 0.7 and self.gender=='Male') or (self.scent > 0.7 and self.gender=='Female')): #setting the req to cats mating req
                    self.req = 'cs'
            if wup == True: #resting the req based on the commitment being fullfilled.
                self.rest = False
                if self.req == 'bed':
                    self.stress = 0
            if fup == True:
                self.eat = False
                if self.req == 'food':
                    self.stress = 0
            if dup == True:
                self.drink = False
                if self.req == 'drink':
                    self.stress = 0
            if self.stress == self.stress_calc:
                self.stress = 0.1
            return(True)
        else:
            return(False)

    def eat_drink_sim(self,landmark,stepsperday,timestep,bucket):
        #Interaction with food.
        if landmark.ltype == 'food' and self.hunger >= 0:
            ec = 0.5*(self.e_time/(24*60))*stepsperday  #Decrease in hunger based on stepsperday
            if (self.hunger-ec) > 0:
                fec = landmark.eat_drink_sim(ec,self.c_age,stepsperday) #Checking quantity in landmark
            elif (self.hunger-ec) < 0:
                fec = landmark.eat_drink_sim((self.hunger),self.c_age,stepsperday)  #Checking quantity in landmark
            if (self.hunger-fec) <= 0:  #If completed meal received
                self.hunger = 0
            elif (self.hunger-fec) > 0: #If still more to eat
                self.hunger += -fec 
        if landmark.ltype == 'water' and self.thirst >= 0:  #Follows same logic as the food section above
            ec = 0.5*(self.d_time/(24*60))*stepsperday
            if (self.thirst-ec) > 0:
                fec = landmark.eat_drink_sim(ec,self.c_age,stepsperday)
            elif (self.thirst-ec) < 0:
                fec = landmark.eat_drink_sim(self.hunger,self.c_age,stepsperday)
            if (self.thirst-fec) <= 0:
                self.thirst = 0
            elif (self.thirst-fec) > 0:
                self.thirst += -fec
        if self.hunger == 0:    #Updating eat status
            self.eat = False
        #else:
        #    self.eat = False
        if self.thirst == 0:    #Updating drink status
            self.drink = False
        #else:
        #    self.drink = False
        if landmark.ltype == 'food':    #Updating requirment and stress level
            if landmark.remaining()==0:
                self.eat = False
                if self.req == 'food':
                    self.stress = 0
        elif landmark.ltype == 'water': #Updating requirment and stress level
            if landmark.remaining()==0:
                self.drink = False
                if self.req == 'water':
                    self.stress = 0
        if self.age(timestep,stepsperday) < self.ls[0]: #For kittens (This code is implemented else where)
            for cat in bucket.cats:
                if cat.cps == True:
                    self.hunger = 0
                    self.thirst = 0

    def move_to(self,new_loc,old_loc,stepsperday,timestep):
        move = True #Condition for movement is taken as True
        
        #Conditions to check if the block occupied is a box and in that cas change certain attributes
        if old_loc.occupiedby()[0] == True:
            if old_loc.occupiedby()[1].myclass == 'Landmark':
                if old_loc.occupiedby()[1].ltype == 'box':
                    if old_loc.occupiedby()[1].access(self,stepsperday,timestep) == False:
                        move = False
                        #print(self.name,self.rest,self.req,self.tired,self.u_age(stepsperday,timestep))
                        #print('cant_move')
                        self.rest = True
                    else:
                        self.rest = False
                        if self.cps == True:
                            old_loc.occupiedby()[1].cat_in = False
        if new_loc.occupiedby()[0] == True:
            if new_loc.occupiedby()[1].myclass == 'Landmark':
                if new_loc.occupiedby()[1].ltype == 'box':
                    if new_loc.occupiedby()[1].access(self,stepsperday,timestep) == False:
                        move = False
                    else:
                        self.rest = True
                        if self.cps == True:
                            new_loc.occupiedby()[1].cat_in = True

        #Conditions to check if the block occupied is a bed and in that cas change certain attributes
        if old_loc.occupiedby()[0] == True:
            if old_loc.occupiedby()[1].myclass == 'Landmark':
                if old_loc.occupiedby()[1].ltype == 'bed':
                    old_loc.occupiedby()[1].leave(self,stepsperday,timestep)
                    self.rest = False
        if new_loc.occupiedby()[0] == True:
            if new_loc.occupiedby()[1].myclass == 'Landmark':
                if new_loc.occupiedby()[1].ltype == 'bed':
                    new_loc.occupiedby()[1].occupy(self,stepsperday,timestep)
                    self.rest = True

        if move == True: #Based on the above two unique cases allow the movement or stoping it.
            self.loc = [new_loc.row,new_loc.col]
            old_loc.remove(self)
            new_loc.add(self)
            #print('Cat Moved:',self.name)
            return (True)
        else:
            return (False)

    def move_cat(self,neighbour_buckets,simtype,stepsperday,timestep,win,pos,sim):  #Cats motion for every timesetp
        fscent = 0
        dscent = 0
        bedscent = 0
        boxscent = 0
        cscent = 0
        lscent = 0
        fbucket = None
        fcat = None
        dbucket = None
        dcat = None
        bedbucket = None
        bcat = None
        boxbucket = None
        boxcat = None
        cbucket = None
        ccat = None
        lbucket = None
        
        n_buckets = neighbour_buckets.copy()
        n_size = len(neighbour_buckets)
        for n in range(n_size):     #Identifying the neighbour bucket that is of value for food, water,bed and boxes.
            can_move = True
            rn = random.randint(0,n_size-1) #taking a random bucket of the neighbours
            bucket=n_buckets[rn]    #To make the motion non linear
            height = abs(bucket.height-neighbour_buckets[pos].height)   #Taking the height different between buckets
            if height >= self.jump(timestep,stepsperday):   #Checking if the cat can jump into the box
                can_move = False
            else:
                can_move = True
            if fscent < bucket.scents[0] and can_move == True:  #Identifying the bucket for food
                if bucket.occupiedby()[0] == True:
                    if bucket.occupiedby()[1].myclass == 'Cat':
                        if bucket.occupiedby()[1].name != self.name:
                            fscent = bucket.scents[0]
                            fbucket = bucket
                            fcat = bucket.occupiedby()[1]
                        elif bucket.occupiedby()[1].name == self.name:
                            fscent = bucket.scents[1]
                            fbucket = bucket
                else:
                    fscent = bucket.scents[0]
                    fbucket = bucket
            if dscent < bucket.scents[1] and can_move == True:  #Identifying the bucket for water
                if bucket.occupiedby()[0]==True:
                    if bucket.occupiedby()[1].myclass == 'Cat':
                        if bucket.occupiedby()[1].name != self.name:
                            dscent = bucket.scents[1]
                            dbucket = bucket
                            dcat = bucket.occupiedby()[1]
                        elif bucket.occupiedby()[1].name == self.name:
                            dscent = bucket.scents[1]
                            dbucket = bucket
                else:
                    dscent = bucket.scents[1]
                    dbucket = bucket
            if bedscent < bucket.scents[3] and can_move == True:    #Identifying the bucket for beds
                if bucket.occupiedby()[0]==True:
                    if bucket.occupiedby()[1].myclass == 'Landmark':
                        if bucket.occupiedby()[1].ltype == 'bed':
                            if len(bucket.cats) == 0:
                                bedscent = bucket.scents[3]
                                bedbucket = bucket
                            elif len(bucket.cats) == 1:
                                bedscent = bucket.scents[1]
                                bedbucket = bucket
                                if bucket.cats[0].name == self.name:
                                    pass
                                else:
                                    bcat = bucket.cats[0]
                else:
                    bedscent = bucket.scents[3]
                    bedbucket = bucket

            if boxscent < bucket.scents[2] and can_move == True:    #Identifying the bucket for boxes
                if bucket.occupiedby()[0] == True:
                    if bucket.occupiedby()[1].myclass == 'Landmark':
                        if bucket.occupiedby()[1].ltype == 'box':
                            if bucket.occupiedby()[1].access(self,stepsperday,timestep) == True:
                                boxscent = bucket.scents[2]
                                boxbucket = bucket
                else:
                    boxscent = bucket.scents[2]
                    boxbucket = bucket

            if self.gender == 'Male' and can_move == True:  #Identifying the bucket for mating
                if cscent < bucket.scents[5][1] and bucket.occupiedby()[0]==False and boxscent>0:
                    csent = bucket.scents[5][1]
                    cbucket = bucket
            elif self.gender == 'Female' and can_move == True:
                if cscent < bucket.scents[4][1] and bucket.occupiedby()[0]==False and boxscent>0:
                    csent = bucket.scents[4][1]
                    cbucket = bucket

            n_size += -1    #Removing checked bucket from the neighbout bucket list
            n_buckets.remove(bucket)
            #print(type(boxbucket))

        if self.req == 'water' and dbucket != None: #Initiating the motion towards the water source if that is the requirment
            if dbucket.occupiedby()[0] == True:
                if dbucket.occupiedby()[1].myclass == 'Cat':
                    if dbucket.occupiedby()[1].name != self.name:
                        self.chall(dcat,stepsperday,timestep,neighbour_buckets[pos],dbucket,sim)
                    elif dbucket.occupiedby()[1].name == self.name:
                        return (self.move_to(dbucket, neighbour_buckets[pos],stepsperday,timestep))
            else:
                return (self.move_to(dbucket, neighbour_buckets[pos],stepsperday,timestep))
        elif self.req == 'food' and fbucket != None: #Initiating the motion towards the food source if that is the requirment
            if fbucket.occupiedby()[0] == True:
                if fbucket.occupiedby()[1].myclass == 'Cat':
                    if fbucket.occupiedby()[1].name != self.name:
                        self.chall(fcat,stepsperday,timestep,neighbour_buckets[pos],fbucket,sim)
                    elif fbucket.occupiedby()[1].name == self.name:
                        return (self.move_to(fbucket, neighbour_buckets[pos],stepsperday,timestep))
            else:
                return (self.move_to(fbucket, neighbour_buckets[pos],stepsperday,timestep))
        elif self.req == 'bed' and bedbucket != None and self.cps!=True: #Initiating the motion towards the bed source if that is the requirment
            if bedbucket.occupiedby()[0]==True:
                if bedbucket.occupiedby()[1].myclass == 'Landmark':
                    if bedbucket.occupiedby()[1].ltype == 'bed':
                        if len(bedbucket.cats)==0:
                            return (self.move_to(bedbucket, neighbour_buckets[pos],stepsperday,timestep))
                        elif len(bedbucket.cats)>0 and bcat != None:
                            self.chall(bcat,stepsperday,timestep,neighbour_buckets[pos],bedbucket,sim)
            else:
                return (self.move_to(bedbucket, neighbour_buckets[pos],stepsperday,timestep))
        elif self.req == 'box' and boxbucket != None: #Initiating the motion towards the box source if that is the requirment
            if self.cps == True:    #This is to navigate the parent cat using its memory map.
                r = neighbour_buckets[pos].row
                c = neighbour_buckets[pos].col
                if simtype == 'Moore':
                    p = 4
                    if r > self.lloc[0] and c > self.lloc[1]:
                        p = 0
                    elif r < self.lloc[0] and c > self.lloc[1]:
                        p = 6
                    elif r > self.lloc[0] and c < self.lloc[1]:
                        p = 2
                    elif r < self.lloc[0] and c < self.lloc[1]:
                        p = 8
                    elif r == self.lloc[0] and c < self.lloc[1]:
                        p = 5
                    elif r == self.lloc[0] and c > self.lloc[1]:
                        p = 3
                    elif r < self.lloc[0] and c == self.lloc[1]:
                        p = 7
                    elif r > self.lloc[0] and c == self.lloc[1]:
                        p = 1
                else:
                    p = 2
                    if r > self.lloc[0]:
                        p = 0
                    elif r < self.lloc[0]:
                        p = 4
                    elif c > self.lloc[1]:
                        p = 1
                    elif c < self.lloc[1]:
                        p = 3
                return (self.move_to(neighbour_buckets[p], neighbour_buckets[pos],stepsperday,timestep))
            elif self.conc==True and self.conct>=62:    #When the cat is about to give birth to the litter moving towards the box scent
                return (self.move_to(boxbucket, neighbour_buckets[pos],stepsperday,timestep))
        elif self.req == 'cs' and cbucket != None:  #Move towards the cat of interest identified to mate.
            return(self.move_to(cbucket, neighbour_buckets[pos],stepsperday,timestep))

    def chall(self,cat,stepsperday,timestep,curr_bucket,cat_bucket,sim):
        fc = random.random()    # fight coefficient taken in random
        sc = random.random()    # stress coefficient taken in random
        # Check whether the cats fc and sc of the instance induce the cat to challenge the advantage cat
        if (fc<(self.dom_score(stepsperday,timestep)-cat.dom_score(stepsperday,timestep)) or (self.stress)>sc) and self.c_age>self.ls[0] and cat.c_age>self.ls[0]:
            ch = cat.rec_chall(self,stepsperday,timestep,cat_bucket,curr_bucket) # Response from advantage cat
            if (ch==True):  # Going into a fight or making a new fight
                if cat.fight == True:   #Going into a fight
                    if cat.f_obj != None:   
                        cat_l = []
                        for cat_loc in cat.f_obj.cats:  
                            cat_l.append(cat_loc[0])
                        if self not in cat_l:
                            #print(cat.name,' is in a fight and ',self.name,' joined against ', cat.name)
                            cat.f_obj.cat_join(self,curr_bucket)
                            self.fight = True
                    else:   # Making a new fight
                        #print(self.name,' wants to fight for position and ',cat.name,' wants to hold position.')
                        temfight = Fight(str(cat.name),cat,cat_bucket)
                        temfight.cat_join(self,curr_bucket)
                        sim.add_fight(temfight)
                        self.fight = True
                        cat.f_obj = temfight
                        cat.fight = True
                else:   #Making a new fight
                    #print(self.name,' wants to fight for position and ',cat.name,' wants to hold position.')
                    temfight = Fight(str(cat.name),cat,cat_bucket)
                    temfight.cat_join(self,curr_bucket)
                    sim.add_fight(temfight)
                    self.fight = True
                    cat.f_obj = temfight
                    cat.fight = True
            elif (ch==False):
                self.stress=0

    def rec_chall(self,cat,stepsperday,timestep,self_bucket,cat_bucket):
        fc = random.random()    # fight coefficient taken in random
        sc = random.random()    # stress coefficient taken in random
        if fc<(self.dom_score(stepsperday,timestep)-cat.dom_score(stepsperday,timestep)) or (self.stress)>sc:   
            return(True)    #Respons to hold position and fight
        elif (self.stress)<sc:
            #print('Position given away as challenge is not worth it.')
            cat.move_to(self_bucket,cat_bucket,stepsperday,timestep)
            self.move_to(cat_bucket,self_bucket,stepsperday,timestep)
            self.eat = False
            self.drink = False
            return(False)   #Response to not hold position but give it away.
        else:
            pass
            #print(self.name,' cat stands ground')  #Response to ignore challenger.

    def m_chall(self,cat,stepsperday,timestep,cat_bucket,self_bucket):
        mc = random.random()    #mating chance
        sc = random.random()    #scent chance
        if mc < (self.scent/1.4) and self.ms != True: #checking mating chance and scent intensity
            #print('Mating Call by: ',self.name)
            ch = cat.mrec_chall(self,stepsperday,timestep,self_bucket,cat_bucket)   #response from mate cat
            if ch == True:  #If accepted
                self.ms=True
                self.move_to(cat_bucket,self_bucket,stepsperday,timestep)
            elif ch == False:   #If denied
                pass
                #print('Failed Mating Call')

    def mrec_chall(self,cat,stepsperday,timestep,cat_bucket,self_bucket):
        mc = random.random()    #mating chance
        sc = random.random()    #scent chance
        #generating a response
        if mc < (self.scent/1.4) and sc > (self.dom_score(stepsperday,timestep)-cat.dom_score(stepsperday,timestep)) and self.ms != True: 
            #print('Accepted Mating Call by: ',self.name)
            self.ms=True    #accepted mating challenge
            return(True)
        else:
            #print('This is not your lucky moment!')
            return(False)   #denied mating challenge

    def mate_w(self,cat,stepsperday,timestep,cat_bucket,self_bucket):
        #print('Success')
        sc = random.random()    #chance to conceive
        if sc > (self.dom_score(stepsperday,timestep)-cat.dom_score(stepsperday,timestep)) and (self.conct!=True or cat.conct!=True) and (self.ms==True and cat.ms==True): #Succesfullty mated
            #print('S')
            if self.gender == 'Female':
                self.conc = True
                self.conct = 0
            else:
                cat.conc = True
                cat.conct = 0
            #self.ms = False <- Caused an error
            #cat.ms = False <- Caused an error
            self.scent = 0.0
            cat.scent = 0.0
        if self.conc==True or cat.conc==True:
            #print('F')
            self.ms = False
            cat.ms = False
            self.move_to(self_bucket,cat_bucket,stepsperday,timestep) # <- Required to stop ghosting
        else:   #If the mating was unsuccesfull
            #print('Not Entirely Succesfull')
            #print(True)
            self.ms = False
            cat.ms = False
            self.stress = 1
            self.req = ''
            cat.req = ''

    def conc_update(self,neighbour_buckets,simtype,stepsperday,timestep,sim):
        ct = 62
        #print(self.conct)
        if simtype == 'Moore': #Self_bucket based on simulation type
            self_bucket = neighbour_buckets[4]
        elif simtype == 'Neuman':
            self_bucket = neighbour_buckets[2]
        if self_bucket.scents[2] < 0:   #If there is no box in the map no litter.
            self.conc = False
            self.conct = 0
        if self.conc == True:   #Updating the conct value.
            self.conct += (1/stepsperday)
        if self.conc == True and self.conct >= ct: #When conct has acheived steps for 62 days the cat will give birth to litter
            self.req = 'box'
        if self_bucket.occupiedby()[0] == True: #GIving birth to litter after reaching the box
            if self_bucket.occupiedby()[1].myclass=='Landmark': #checking if the cell is a box
                if self_bucket.occupiedby()[1].ltype == 'box':
                    print(True,timestep)
                    n = random.randint(1,9)
                    g = ['Male','Female']
                    a = len(sim.cats)
                    self.lloc = [self_bucket.row,self_bucket.col]
                    for i in range(n):  #Generating random kittens in the box
                        name = 'c'+str(a+i+1)
                        gender = random.choice(g)
                        dob = timestep/stepsperday
                        kitten = Cat(name,gender,dob)
                        kitten.rest = True
                        sim.add_cat(cat=kitten)
                        sim.add_grid(self.lloc[0],self.lloc[1],kitten.name,con=True)
                        sim.grid[self.lloc[0],self.lloc[1]].occupiedby()[1].cat_in = True
                    self.conc = False
                    self.conct = 0
                    self.cps = True #Parent mode activated.
                    self.boxpop = n
                    self.req=''

    def cps_update(self,timestep,stepsperday,self_bucket,sim):
        #print(self.cps_val)
        if self.boxpop == 0:    #Update the CPS if boxpop is zero
            self.lloc = [0,0]
            self.cps = False
            return(0)
        if self.cps == True and self.cps_val<1: #Update the cps_val accordingly if not in box
            self.cps_val += (20/(4*stepsperday))
            if self.cps_val > 1:
                self.cps_val = 1
        if self.cps == True and self.cps_val == 1:  #Changing req if cps_val == 1
            self.req = 'box'
        if self_bucket.occupiedby()[0] == True:
            if self_bucket.occupiedby()[1].myclass=='Landmark': #Interacting with box bucket after getting in box
                if self_bucket.occupiedby()[1].ltype == 'box':
                    self.boxpop = len(self_bucket.cats)-1
                    if self.boxpop > 0:
                        sim.grid[self.lloc[0],self.lloc[1]].occupiedby()[1].cat_in = True
                    else:
                        self.cps = False
                        self.cps_val = 0
                    if self.cps_val > 0:
                        self.cps_val = 0
                    if self.req == 'box':
                        self.req=''

    def cat_log(self,sim):  #Generating the cat log.
        profile = ['CAT',('name: '+str(self.name)),('dob: '+str(self.dob)),('age: '+str(self.c_age)),('gender: '+str(self.gender)),('hunger: '+str(self.hunger)),('thirst: '+str(self.thirst)),('tired: '+str(self.tired)),('stress:'+str(self.stress)),('scent: '+str(self.scent)),('conct: '+str(self.conct)),('cps_val: '+str(self.cps_val)),('box pop: '+str(self.boxpop))]
        if self.hunger==1 or self.thirst == 1 or self.tired == 1:
            profile.append('Self log: Passed away RIP')
        elif self.eat == True:
            profile.append(str('Self log: Eating food to a neighbouring source at row:'+str(self.loc[0])+' col: '+str(self.loc[1])))
        elif self.drink == True:
            profile.append(str('Self log: Drinking water to a neighbouring source at row:'+str(self.loc[0])+' col: '+str(self.loc[1])))
        elif self.rest == True:
            profile.append('Self log: Sleeping on the bed at row:'+str(self.loc[0])+' col: '+str(self.loc[1]))
        elif self.fight == True:
            if self.f_obj == None:
                profile.append('Self log: Fighting with a neighbouring cat at row:'+str(self.loc[0])+' col: '+str(self.loc[1]))
            elif self.f_obj != None:
                if self.name == self.f_obj.cat_adv.name:
                    fs = ('Self log: Holding a position of value contested by: ',len(self.f_obj.cats),'. The cats contesting are : ')
                    #for i,cat_loc in enumerate(self.f_obj.cats):
                        #cat = cat_loc[0]
                        #if i == 0:
                        #    fs += str(cat.name)
                        #else:
                        #    fs += ' ,'+str(cat.name)
                    #   profile.append(fs)
                else:
                    profile.append('Self log: In a confusing situation, annoyed and angry!')
        elif self.ms == True:
            cats = sim.grid[self.loc[0],self.loc[1]].cats
            name = ''
            for cat in cats:
                if cat.name != self.name:
                    name = cat.name
            profile.append('Self log: Mating with '+name)
        elif self.conc == True:
            if self.conct == 0:
                profile.append('Self log: Mated Succesfully and conceived!')
            elif self.conct == 61:
                profile.append('Self log: One more day togo!')
            elif self.conct > 0:
                profile.append('Self log: '+str(int(62-self.conct))+' '+'more days togo before giving birth.')
        elif self.cps == True:
            if self.cps_val == 0:
                profile.append('Self log: Kittens in the box are provided necessary nutrition, Kittens in Box: '+str(self.boxpop))
            elif self.cps_val == 1:
                profile.append('Self log: Going back to the box to feed kittens!')
        elif self.boxpop == 0 and len(sim.grid[self.loc[0],self.loc[1]].landmarks)>0:
            if sim.grid[self.loc[0],self.loc[1]].landmarks[0].ltype == 'box':
                profile.append('Self log: All kittens have turned into adults!-Parenting is Complete')
        else:
            profile.append('Self log: Just licking my fur and waiting unitl there is a need for something')
        return(profile)



class Fight():

    def __init__(self,name,cat_adv,loc_adv,cats=[]):#cat adv | cats asking pos
        self.name=name          #Instance variable Identifier for fight
        self.cat_adv=cat_adv    #Instance variable that identifies the advantage cat
        self.loc_adv=loc_adv    #Instance variable that identifies the advantage bucket
        self.cats=cats          #Instance variable that identifies the cats in the fight

    def cat_join(self,cat,curr_bucket): #for a cat to join the fight
        self.cats.append([cat,curr_bucket])

    def cats_fight(self,stepsperday,timestep,sim):  #Simulating the cat fight
        #print(self.cat_adv.name,self.cats) 
        if self.cats == []: #Checking if the fight is over
            #print(True)
            #print(' Fight Winner : ',self.cat_adv.name)
            self.cat_adv.fight = False
            self.cat_adv.f_obj = None
            sim.remove_fight(self)
            return('W')
        else:
            for i,cat_loc in enumerate(self.cats):  #Fighting with every cat in the cat list
                catadv_dom=self.cat_adv.dom_score(stepsperday,timestep)
                catadv_st=self.cat_adv.stress
                catadv_rst=self.cat_adv.stress_calc(stepsperday)
                cat = cat_loc[0]
                loc = cat_loc[1]
                cat_dom=cat.dom_score(stepsperday,timestep)
                cat_st=cat.stress
                cat_rst=cat.stress_calc(stepsperday)
                cd_prob=abs(catadv_dom-cat_dom)
                cd_rstress=abs(((catadv_rst-catadv_st)+(cat_rst-cat_st))/2)
                cd_stress=abs((catadv_st-cat_st)/2)
                cd_finalized=random.random()
                if cat.fight == True:   #Checking the cat state in case it has not change
                    #print(cd_prob,cd_rstress,cd_stress)
                    if cd_finalized < (cd_prob+cd_rstress-cd_stress):   #The fight concluded or not
                        cd_winner = random.random()
                        if cd_winner > ((cat_dom-cd_rstress)/(catadv_dom+cat_dom)): #Identify the winner of the fight
                            #print('New adv cat : ',cat.name)
                            if loc.occupiedby()[0] == True: #If winner is challenger
                                if loc.occupiedby()[1].myclass == 'Cat':
                                    for c in loc.cats:
                                        if cat.name == c.name:
                                            cat.move_to(self.loc_adv,loc,stepsperday,timestep)
                            else:
                                pass
                            #self.cat_adv.move_to(loc,self.loc_adv,stepsperday,timestep)
                            if cat_loc in self.cats:
                                self.cats.remove(cat_loc)
                            #print(self.cat_adv.name,cat.name)
                            self.cat_adv.stress = 0.0
                            self.cat_adv.eat = False
                            self.cat_adv.drink = False
                            self.cat_adv.rest = False
                            self.cat_adv.fight = False
                            self.cat_adv.ms = False
                            if cat.f_obj == None:
                                cat.f_obj = self.cat_adv.f_obj
                                self.cat_adv.f_obj = None
                            else:
                                #print(True)
                                fight = cat.f_obj
                                cat.f_obj = self.cat_adv.f_obj
                                self.cat_adv.f_obj = fight
                            if self.loc_adv.occupiedby()[0] == True:
                                if self.loc_adv.occupiedby()[1].myclass == 'Cat':
                                    for c in self.loc_adv.cats:
                                        if self.cat_adv.name == c.name:
                                            self.cat_adv.move_to(loc,self.loc_adv,stepsperday,timestep)
                            else:
                                pass
                            self.cat_adv = cat
                            self.name = cat.name
                            return('L')
                        elif cd_winner < ((cat_dom+cd_rstress)/(catadv_dom+cat_dom)):#If winner is advantage cat
                            #print(' Fight Winner : ',self.cat_adv.name)
                            cat.stress = 0.0
                            cat.eat = False
                            cat.drink = False
                            cat.rest = False
                            cat.fight = False
                            cat.f_obj = None
                            cat.ms = False
                            if cat_loc in self.cats:
                                self.cats.remove(cat_loc)
                            #print(self.cats)
                            return('W')
                    else:   #Error regulation as a result of excessive ghosting and cramming.
                        self.cat_adv.fight = True   
                        cat.fight = True
                        #print(self.cat_adv.name,' still fighting with ',cat.name)
                        return('F')
                else:   #Error regulation as a result of excessive ghosting and cramming.
                    #print(' Fight Winner : ',self.cat_adv.name)
                    self.cats = []
        #print(self.cat_adv.fight,self.cat_adv.f_obj,cat.fight,cat.f_obj)

    
