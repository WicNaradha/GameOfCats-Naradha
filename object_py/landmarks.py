#
# Student ID: 20469160
# Student Name: W.M.Naradha
#
# landmarks.py - contains the object classes related to landmarks in the game of cats.
#

class Landmark():
    myclass = 'Landmark'
    def __init__(self,name,ltype,quantity,reset,r=None,c=None,direction=['all'],cat_in=False, control_reset=1.0, consume=0.0):
        self.name = name                #Instance variable identifier for specific landmark
        self.ltype = ltype              #Instance variable defines type of landmark
        self.quantity = quantity        #Instance variable defines quantity in landmark
        self.reset = reset              #Instance variable to replenish the landmark
        self.loc = [r,c]                #Instance varibale with location of landmark
        self.direction = direction      #Default 'all' or N-North W-West S-South E-East
        self.cat_in = cat_in            #Instance variable showing whether a cat has occupied the landmark (for beds and boxes)
        self.control_reset = control_reset  #Instance variable in replenishing the quantity
        self.consume = consume          #Instance variable having the consumed amount of the food/water source

    def scent(self):    #returns the scent of the landmark based on its quantity
        if self.ltype == 'bed' or self.ltype == 'box':
            return(1)
        else:
            return((self.quantity-self.consume)/self.quantity)

    def remaining(self):    #returns the remaining amount of source left in the landmark
        return(self.quantity-self.consume)

    def update_landmark(self,stepsperday):  #update the landmark attributes
        self.scent()
        self.resetlandmark(stepsperday)

    def eat_drink_sim(self,ec,cat_age,stepsperday): #Simulating change in quantity based on weight of cat
        if cat_age <= 365:  #For kittens age based weight of cat
            weight = (9/730)*cat_age+0.5
        else:
            weight = 5
        if self.ltype == 'food':    #Food quantity consumed based on weight of cat
            consumptionperstep = weight*(4/15)*((24*60)/stepsperday)
        elif self.ltype == 'water': #Water quantity consumed based on weight of cat
            consumptionperstep = weight*(2.875/3)*((24*60)/stepsperday)
        if (self.remaining()-consumptionperstep) >= 0:  #Consumption adjusted based on above value
            self.consume += consumptionperstep
            return(ec)
        elif (self.remaining()-consumptionperstep) < 0:
            ec = ((self.quantity-self.remaining())/consumptionperstep)*ec
            self.consume = self.quantity
            return(ec)
       
    def resetlandmark(self,stepsperday):    #replenishing the landmarks resources every reset times a day
        c = 1
        reset = False
        #print(True,ec,self.control_reset-ec)
        if self.reset > 0:
            if (self.control_reset+c)/(stepsperday/self.reset) >= 1:    #checking for reset
                reset = True
            elif (self.control_reset+c)/(stepsperday/self.reset) < 1:   
                self.control_reset += c #accounts for the timestep to be reset when self.contorl_reset >= 1 to make the reset possible.
            if reset == True:   #actual reset of the resource
                self.consume = 0
                self.control_reset = 0

    def occupy(self,cat,stepsperday,timestep):  #occupy beds by cats
        if cat.jump(stepsperday,timestep) > self.quantity:
            self.cat_in = True
            return(True)
        else:
            return(False)

    def leave(self,cat,stepsperday,timestep):   #leave beds by cats
        if cat.jump(stepsperday,timestep) > self.quantity:
            self.cat_in = False
            return(True)
        else:
            return(False)

    def access(self,cat,stepsperday,timestep):  #whether the cat can access the bed or box as quantity sets the height of the bed/box.
        if self.ltype == 'bed' or self.ltype == 'box':
            if cat.jump(stepsperday,timestep) > self.quantity:
                return(True)
            else:
                return(False)
        else:
            return(False)

    def loccupiedby(self):  #whether the bed or box is occupied
        if self.cat_in == True:
            return([self.ltype,True])
        elif self.cat_in == False:
            return([self.ltype,False])
    
    def lm_log(self,sim):   #generating landmark logs
        profile = [('LANDMARK'),('name: '+str(self.name)),('type: '+str(self.ltype)),('quantity: '+str(self.quantity)),('remaining: '+str(self.remaining())),('location: '+str(self.loc)),('reset: '+str(self.reset)),('control_reset: '+str(self.control_reset))]
        return(profile)
