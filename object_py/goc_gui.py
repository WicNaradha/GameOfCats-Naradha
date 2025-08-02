#!/home/wicnara/anaconda3/bin/python3

#Dependencies all available in Anaconda
import time
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
from threading import *
import math
import sys
import os

#Main Objects
import simulation
from simulation import *

save_path = '../saves/'
input_path = '../inputs/'
close = False

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Game Of Cats - Simulator")
        self.resizable(width=False, height=False)
        
        play_thread = Thread(target=self.play_sim)
        close_thread = Thread(target=self.close_task)
        self.ts = False
        self.sim = None
        self.img = None
        self.img_list = []
        self.p = False
        self.attributes = ''
        self.fps = 2
        self.speed = 1
        self.pf = False
        self.pfor = 10
        self.delay = 1
        self.plystatus = False
        self.loop = False
        self.obl = []
        self.frame = 0
        self.write_log = False
        self.plt_save = False
        self.log = []

        self.framecon()

        self.frameplot()

        term_thread = Thread(target=self.term_in)
        term_thread.start()

    def close_task(self):
        print('Enter or press ctrl-c to quit:')
        close = True
        time.sleep(0.5)
        self.destroy()

    def term_in(self):
        #time.sleep(5)
        if len(sys.argv) > 0:
            self.ts = False
            i = 0
            for comm in sys.argv:
                i += 1
                if i > 1:
                    self.command = comm
                    try:
                        self.comm_process()
                    except Exception as e:
                        print(e)
            self.ts = True
        while close == False:
            if self.ts == True:
                try:
                    print('----- USER INPUT TERMINAL -----')
                    self.command = input('Enter a command : ')
                except Exception as e:
                    print('Exception Re-input Command: ',e)
                try:
                    self.comm_process()
                except Exception as e:
                    er = 'Error: ' + str(e)
                    self.commands.append(er)
                    print(e)
                if self.command == 'quit()':
                    break

    def comm_process(self): #Command processing
            self.commands.append(self.command)
            command = self.command.split('(')
            att = str(command[1]).strip(')').split(',')
            if command[0] == 'load':    #load command of simulations
                os.chdir(str(save_path+'/'+att[0]))
                self.sim = simulation.load_sim(att[0] + '.csv')
                if len(att) > 1:
                    self.fps = att[1]
                os.chdir('../../object_py')
            elif command[0] == 'save':  #save command of simulations
                #print(os.getcwd())
                os.chdir(str(save_path))
                if self.sim.name in os.listdir():
                    os.chdir(self.sim.name)
                else:
                    os.mkdir(self.sim.name)
                    os.chdir(self.sim.name)
                simulation.save_sim(self.sim)
                os.chdir('../../object_py')
            elif command[0] == 'create_sim':    #create simulations command of simulations
                mapdir = ''
                if att[5] != '':
                    mapdir = input_path+str(att[5])
                #print(mapdir)
                self.sim = Sim(str(att[0]), str(att[1]), int(att[2]), rows=int(att[3]), cols=int(att[4]),map=mapdir)
            elif command[0] == 'add_cat':   #add cat objects to the simulation
                self.sim.add_cat(str(att[0]), str(att[1]), int(att[2]))
            elif command[0] == 'add_landmark':  #add landmark objects to the simulation
                if att[4] == '':
                    self.sim.add_landmark(str(att[0]), str(att[1]), int(att[2]), int(att[3]))
                else:
                    self.sim.add_landmark(str(att[0]), str(att[1]), int(att[2]), int(att[3]),direction=att[4])
            elif command[0] == 'add_grid':  #add the objects to the grid
                self.sim.add_grid(int(att[0]), int(att[1]), str(att[2]))
            elif command[0] == 'play_sim':  #running and playing simulation
                self.p = True
                self.attributes = att[0]
                play_thread = Thread(target=self.play_sim)
                play_thread.start()
            elif command[0] == 'play_for':  #playing a simulation for a timespan
                self.pf = True
                self.pfor = int(att[0])
                self.attributes = att[1]
                self.plystatus = bool(int(att[2]))
                self.write_log = bool(int(att[3]))
                self.plt_save = bool(int(att[4]))
                self.loop = bool(int(att[5]))
                self.delay = int(att[6])
                self.close = bool(int(att[7]))
                self.frame = math.floor(self.pfor/self.speed)
                self.obl = [[]*int(self.frame)]
                play_thread = Thread(target=self.play_sim)
                play_thread.start()
                self.refresh_framecon()
                self.show_loading()
            elif command[0] == 'pause_sim': #pausing a simulation
                self.p = False
                #self.pf = False
            elif command[0] == 'set':       #setting certian attributes of a simulaiton
                if att[0] == 'attribute':   
                    self.attributes = att[1]
                elif att[0] == 'fps':
                    self.fps = int(att[1])
                elif att[0] == 'speed':
                    self.speed = int(att[1])
            elif command[0] == 'random':    #generating a random simulation.
                val = 0
                os.chdir(str(save_path))
                for name in os.listdir():
                    if 'Ran' in name:
                        val += 1
                val += 1
                os.chdir('../object_py')
                if att[4] == '':
                    mapdir = ''
                else:
                    mapdir = input_path+str(att[4])
                #print(mapdir)
                self.sim = Sim('Ran'+str(val),att[0],int(att[1]),rows=int(att[2]),cols=int(att[3]),map=mapdir)
                g = ['Male','Female']
                for i in range(int(att[5])):
                    assigned = False
                    name = 'c'+str(i)
                    dob = -random.randint(1,5475)
                    gender = random.choice(g)
                    h = random.random()
                    th = random.random()
                    ti = random.random()
                    s = 1.4*random.random()
                    c = Cat(name,gender,dob,hunger=h,thirst=th,tired=ti,scent=s)
                    self.sim.add_cat(cat=c)
                    while assigned == False:
                        x = random.randint(1,self.sim.maxrowcol[0]-2)
                        y = random.randint(1,self.sim.maxrowcol[1]-2)
                        assigned = self.sim.add_grid(x,y,name)
                t = ['food','water','bed','box']
                for i in range(int(att[6])):
                    assigned = False
                    name = 'l'+str(i)
                    qua = random.randint(1,500)
                    typ = random.choice(t)
                    r = random.randint(0,4)
                    self.sim.add_landmark(name,typ,qua,r)
                    while assigned == False:
                        x = random.randint(1,self.sim.maxrowcol[0]-2)
                        y = random.randint(1,self.sim.maxrowcol[1]-2)
                        assigned = self.sim.add_grid(x,y,name)
            elif command[0] == 'quit':  #quit the simulation
                close_thread = Thread(target=self.close_task)
                close_thread.start()
                time.sleep(0.1)
            else:   #raising command syntax errors
                self.commands.append('Command Syntax Error')
                raise Exception('Command Syntax Error')
            self.refresh_framecon()
    

    def framecon(self): #The command console frame
        self.framecon = tk.LabelFrame(self, text='Control Space',width=45,height=50)
        self.framecon.grid(column=0, row=0)

        self.command = ''
        self.commands = []
        self.hist_label = tk.Label(self.framecon,height=46,width=40,anchor='sw',justify='left',font='Times 12')
        self.hist_label.grid(column=0, row=0, rowspan=28)
        self.com_run = tk.Button(self.framecon,text="EXEC")
        self.com_run.grid(column=1, row=29)
        self.com_run.config(command=lambda self=self: App.on_com_click(self))
        self.com_input = tk.Entry(self.framecon,width=40,font='Times 12')
        self.com_input.grid(column=0, row=29)

    def on_com_click(self):
        self.command = str(self.com_input.get())
        #self.commands.append(self.command)
        try:
            self.comm_process()
        except Exception as e:
            er = 'Error: ' + str(e)
            self.commands.append(er)
            print(e)
        self.refresh_framecon()

    def refresh_framecon(self): #Refresh the command frame
        coms = ''
        for command in self.commands:
            coms += '> '+str(command)+'\n'
        self.hist_label.config(text=coms)

    def frameplot(self):    #setting up the plot frame
        self.frameplot = tk.LabelFrame(self, text='Simulation', width=50, height=50)
        self.frameplot.grid(column=1, row=0)
        self.plotspace = tk.LabelFrame(self.frameplot)
        self.plotspace.grid(column=0,columnspan=4,row=0)

        self.play = tk.Button(self.frameplot, bg="green", text='PLAY')
        self.play.grid(column=0, row=1)
        self.play.config(command=lambda comm=0, self=self: App.on_click(self,comm))

        self.pause = tk.Button(self.frameplot, bg="red", text='PAUSE')
        self.pause.grid(column=1, row=1)
        self.pause.config(command=lambda comm=1, self=self: App.on_click(self,comm))

        self.save = tk.Button(self.frameplot, bg="orange", text='SAVE-SIM')
        self.save.grid(column=2, row=1)
        self.save.config(command=lambda comm=2, self=self: App.on_click(self,comm))

        self.map = tk.Button(self.frameplot, bg="white", text='MAP-TYPE:ALL')
        self.map.grid(column=3, row=1)
        self.map.config(command=lambda comm=3, self=self: App.on_click(self,comm))

        self.fig = Figure(figsize=(7, 7), dpi=100)  #generating the plot space
        self.plspace = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.plotspace)   #the canvas
        #self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plotspace)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side='top', expand=True)

    def img_scatters(self): #adding the scatter plots
        for row in range(self.sim.maxrowcol[0]):
            for col in range(self.sim.maxrowcol[1]):
                if len(self.sim.grid[row,col].landmarks) == 1:
                    lm = self.sim.grid[row,col].landmarks[0]
                    if lm.ltype == 'food':  #food sources
                        self.plspace.scatter(col,row,c=[[0,0.5,0]],edgecolor=[[0,1,0]],marker='s',s=100)
                    elif lm.ltype == 'water':   #water sources
                        self.plspace.scatter(col,row,c=[[0,0,0.5]],edgecolor=[[0,0,1]],marker='s',s=100)
                    elif lm.ltype == 'bed':     #bed
                        self.plspace.scatter(col,row,c=[[0.5,0,0]],edgecolor=[[1,0,0]],marker='s',s=100)
                    elif lm.ltype == 'box':     #box
                        self.plspace.scatter(col,row,c=[[0.5,0.5,0]],edgecolor=[[1,1,0]],marker='s',s=100)
                if len(self.sim.grid[row,col].cats) == 1:
                    cat = self.sim.grid[row, col].cats[0]
                    if cat.fight == True:   #cat in a fight
                        self.plspace.scatter(col,row,c=[[1,0,0]],edgecolor=[[1,0.75,0]],marker='o')
                    elif cat.eat == True:   #cat eating
                        self.plspace.scatter(col,row, c=[[0,1,0]], edgecolor=[[0.75,1,0]], marker='o')
                    elif cat.drink == True: #cat drinking
                        self.plspace.scatter(col,row, c=[[0,0,1]], edgecolor=[[0.75,0,1]], marker='o')
                    elif cat.rest == True:  #cat in sleep
                        self.plspace.scatter(col,row, c=[[1, 1, 0]], edgecolor=[[1, 0.5, 0.5]], marker='o')
                    elif cat.conc == True:  #concieved cat
                        self.plspace.scatter(col,row,c=[[1,0.75,0.79]],edgecolor=[[1,0.75,0]],marker='o',s=75)
                    else:   #normal state cat
                        self.plspace.scatter(col,row, c=[[1, 1, 1]], edgecolor=[[1, 0, 1]], marker='o')
                if len(self.sim.grid[row,col].cats) > 1:
                    cat = self.sim.grid[row, col].cats[0]
                    if cat.fight == True:   #multiple cats cramming in a fight due to ghosting.
                        self.plspace.scatter(col,row,c=[[1,0,0]],edgecolor=[[1,0.75,0]],marker='o',s=75)
                    else:   #cramming without a fight due to ghosting
                        self.plspace.scatter(col,row,c=[[1,1,1]],edgecolor=[[1,0.5,1]],marker='o',s=75)

    def show_img_scatters(self,frame):  #similar to the previous function but to plot the scatters from lists to refer when showing the simulation in the case of a play_for
        for obl in self.obl[frame]:
            row = obl[1]
            col = obl[2]
            if obl[0] == 'food':
                self.plspace.scatter(col,row,c=[[0,0.5,0]],edgecolor=[[0,1,0]],marker='s',s=100)
            elif obl[0] == 'water':
                self.plspace.scatter(col,row,c=[[0,0,0.5]],edgecolor=[[0,0,1]],marker='s',s=100)
            elif obl[0] == 'bed':
                self.plspace.scatter(col,row,c=[[0.5,0,0]],edgecolor=[[1,0,0]],marker='s',s=100)
            elif obl[0] == 'box':
                self.plspace.scatter(col,row,c=[[0.5,0.5,0]],edgecolor=[[1,1,0]],marker='s',s=100)
            elif obl[0] == 'C-F':
                self.plspace.scatter(col,row,c=[[1,0,0]],edgecolor=[[1,0.75,0]],marker='o')
            elif obl[0] == 'C-E':
                self.plspace.scatter(col,row, c=[[0,1,0]], edgecolor=[[0.75,1,0]], marker='o')
            elif obl[0] == 'C-D':
                self.plspace.scatter(col,row, c=[[0,0,1]], edgecolor=[[0.75,0,1]], marker='o')
            elif obl[0] == 'C-R':
                self.plspace.scatter(col,row, c=[[1, 1, 0]], edgecolor=[[1, 0.5, 0.5]], marker='o')
            elif obl[0] == 'C':
                self.plspace.scatter(col,row, c=[[1, 1, 1]], edgecolor=[[1, 0, 1]], marker='o')
            elif obl[0] == 'CC-f':
                self.plspace.scatter(col,row,c=[[1,0,0]],edgecolor=[[1,0.75,0]],marker='o',s=75)
            elif obl[0] == 'CC-ms':
                self.plspace.scatter(col,row,c=[[1,0.75,0.79]],edgecolor=[[1,0.75,0]],marker='o',s=75)
            elif obl[0] == 'CC':
                self.plspace.scatter(col,row,c=[[1,1,1]],edgecolor=[[1,0.5,1]],marker='o',s=75)


    def rec_img_scatters(self): #recording the scatter positions on the timesteps
        llist = []
        cframe = self.frame - math.floor(self.pfor/self.speed)
        for row in range(self.sim.maxrowcol[0]):
            for col in range(self.sim.maxrowcol[1]):
                if len(self.sim.grid[row,col].landmarks) == 1:
                    lm = self.sim.grid[row,col].landmarks[0]
                    if lm.ltype == 'food':
                        llist.append(['food',row,col])
                    elif lm.ltype == 'water':
                        llist.append(['water',row,col])
                    elif lm.ltype == 'bed':
                        llist.append(['bed',row,col])
                    elif lm.ltype == 'box':
                        llist.append(['box',row,col])
                if len(self.sim.grid[row,col].cats) == 1:
                    cat = self.sim.grid[row, col].cats[0]
                    if cat.fight == True:
                        llist.append(['C-F',row,col])
                    elif cat.eat == True:
                        llist.append(['C-E',row,col])
                    elif cat.drink == True:
                        llist.append(['C-D',row,col])
                    elif cat.rest == True:
                        llist.append(['C-R',row,col])
                    elif cat.conc == True:
                        llist.append(['CC-ms',row,col])
                    else:
                        llist.append(['C',row,col])
                if len(self.sim.grid[row,col].cats) > 1:
                    cat = self.sim.grid[row, col].cats[0]
                    if cat.fight == True:
                        llist.append(['CC-f',row,col])
                    else:
                        llist.append(['CC',row,col])
        self.obl.append(llist)

    def refresh_canvas(self):   #refresh for realtime playing
        self.plspace.clear()
        if self.attributes == 'ALL' or self.attributes =='Cat-Scent':   #no colormap for these plot types
            self.img_scatters()
            self.plspace.imshow(self.img)
        elif self.attributes =='Terrain':   #terrain types with blues colour map
            if self.sim.map_path != '':
                self.img_scatters()
                self.plspace.imshow(self.img, cmap=plt.cm.Blues)
            else:
                pass
        else:   #terrain types with hot colour map
            self.img_scatters()
            self.plspace.imshow(self.img,cmap=plt.cm.hot)
        self.canvas.draw_idle()

    def show_refresh_canvas(self,frame):    #refresh for the play_for simulation - similar to the previous function    
        self.plspace.clear()    
        if self.attributes == 'ALL' or self.attributes =='Cat-Scent':
            self.show_img_scatters(frame+1)
            self.plspace.imshow(self.img)
        elif self.attributes =='Terrain':
            self.show_img_scatters(frame+1)
            self.plspace.imshow(self.img, cmap=plt.cm.Blues)
        else:
            self.show_img_scatters(frame+1)
            self.plspace.imshow(self.img,cmap=plt.cm.hot)
        self.canvas.draw_idle()

    def on_click(self,comm):    #the buttons on the plot pane
        try:
            if comm == 0:
                self.p = True
                self.attributes = self.map.cget('text').split(':')[1]
                play_thread = Thread(target=self.play_sim)
                play_thread.start()
            elif comm == 1:
                self.p = False
            elif comm == 2:
                os.chdir(str(save_path))
                if self.sim.name in os.listdir():
                    os.chdir(self.sim.name)
                else:
                    os.mkdir(self.sim.name)
                    os.chdir(self.sim.name)
                simulation.save_sim(self.sim)
            elif comm == 3:
                if self.map.cget('text') == 'MAP-TYPE:ALL':
                    self.map.config(text='MAP-TYPE:Terrain')
                elif self.map.cget('text') == 'MAP-TYPE:Terrain':
                    self.map.config(text='MAP-TYPE:Cat-Scent')
                elif self.map.cget('text') == 'MAP-TYPE:Cat-Scent':
                    self.map.config(text='MAP-TYPE:Food-Scent')
                elif self.map.cget('text') == 'MAP-TYPE:Food-Scent':
                    self.map.config(text='MAP-TYPE:Water-Scent')
                elif self.map.cget('text') == 'MAP-TYPE:Water-Scent':
                    self.map.config(text='MAP-TYPE:Bed-Scent')
                elif self.map.cget('text') == 'MAP-TYPE:Bed-Scent':
                    self.map.config(text='MAP-TYPE:Box-Scent')
                elif self.map.cget('text') == 'MAP-TYPE:Box-Scent':
                    self.map.config(text='MAP-TYPE:ALL')
        except Exception as e:
            er = 'Error: ' + str(e)
            self.commands.append(er)
            self.refresh_framecon()

    def show_loading(self): #Show loading when play_for and hault the rest of the commands.
        comm = ''
        while (self.pfor != 0 and self.pfor > 0) or (('object_py' not in str(os.getcwd)) and (self.write_log==True or self.save_plot==True)):
            #print(True)
            if 'Loading' in self.commands[-1]:
                scomm = self.commands[-1].split('g')
                if len(scomm[1]) < 5:
                   scomm[1] += '.'
                else:
                    scomm[1] = ''
                self.commands.remove(ncomm)
                comm = scomm[1]
            ncomm = 'Loading'+comm
            self.commands.append(ncomm)
            self.refresh_framecon()
            time.sleep(0.5)
        self.commands.remove(ncomm)
        self.commands.append('Compleleted Play For Excution.')
        self.refresh_framecon()

    def play_sim(self): #playing in play_for and realtime cases
        while self.p == True or self.pfor != 0:
            for i in range(self.speed):
                if self.pf == True: #playing simulation for play_for
                    self.img = self.sim.run_step(self.attributes,self.write_log) #calling the simulator to run a timestep
                    if i%self.speed == 0:   #speed filter
                        self.img_list.append(self.img)
                        self.rec_img_scatters()
                    self.pfor += -1
                    if self.pfor == 0:  #showing after the end of the simulation
                        self.pf = False
                        if self.write_log == True or self.plt_save == True:
                            self.saves()
                        if self.plystatus == True:
                            self.p = True
                            self.show_sim()
                        self.obl = []
                elif self.p == True:    #playing in realtime
                    self.img = self.sim.run_step(self.attributes,self.write_log) #calling the simulator to run a timestep
                    if i % self.speed == 0: #filtering for the speed (not that effective)
                        self.refresh_canvas()
                        time.sleep(float(1 / float(self.fps)))
    
    def save_plot(self,pltname,frame):  #for saving plot figures in play_for while simulation
        self.plspace.clear()
        if self.attributes == 'ALL' or self.attributes =='Cat-Scent':
            self.show_img_scatters(frame+1)
            self.plspace.imshow(self.img)
        elif self.attributes =='Terrain':
            self.show_img_scatters(frame+1)
            self.plspace.imshow(self.img, cmap=plt.cm.Blues)
        else:
            self.show_img_scatters(frame+1)
            self.plspace.imshow(self.img,cmap=plt.cm.hot)
        self.plspace.figure.savefig(pltname)

    def show_sim(self): #for showing the simulation in the play_for after simulation
        while self.p == True:
            i = 0
            while i < (len(self.img_list)) and self.p == True:
                self.img = self.img_list[i]
                self.show_refresh_canvas(i)
                i += 1
                if i==len(self.img_list) and i != 0 and self.loop == True and self.p == True:
                    i = 0
                    time.sleep(self.delay)
                elif i==len(self.img_list) == 0 and i != 0 and self.loop != True:
                    self.p = False
                time.sleep(float(1 / float(self.fps)))
            self.img_list = []
            self.obl = []
        if self.close == True:
            close_thread = Thread(target=self.close_task)
            close_thread.start()
    
    def saves(self):    #generating saved log file and generating saved plots.
        os.chdir(save_path)
        if self.sim.name not in os.listdir():
            os.mkdir(self.sim.name)
            os.chdir(self.sim.name)
            filename = self.sim.name+'-'+time.strftime('%Y%m%d-%H%M%S')
            os.mkdir(filename)
            os.chdir(filename)
            if self.write_log == True:
                simulation.save_log(self.sim)
            if self.plt_save == True:
                pfilename = self.sim.name+'-plots-'+time.strftime('%Y%m%d-%H%M%S')
                os.mkdir(pfilename)
                os.chdir(pfilename)
                i = 0
                while i < len(self.img_list):
                    img = self.img_list[i]
                    pltname = 'plt'+str(i)+'.png'
                    self.img = img
                    self.save_plot(pltname,i)
                    i += 1
                os.chdir('../')
        else:
            os.chdir(self.sim.name)
            filename = self.sim.name+time.strftime('%Y%m%d-%H%M%S')
            os.mkdir(filename)
            os.chdir(filename)
            if self.write_log == True:
                simulation.save_log(self.sim)
            if self.plt_save == True:
                pfilename = self.sim.name+'-plots-'+time.strftime('%Y%m%d-%H%M%S')
                os.mkdir(pfilename)
                os.chdir(pfilename)
                i = 0
                while i < len(self.img_list):
                    img = self.img_list[i]
                    pltname = 'plt'+str(i)+'.png'
                    self.img = img
                    self.save_plot(pltname,i)
                    i += 1
                os.chdir('../')
        self.write_log = False
        self.save_plot = False
        os.chdir('../../../object_py')



def main():
    application = App()
    application.mainloop()

if __name__ == '__main__':
    gui_thread = Thread(target=main)
    gui_thread.start()
    if close == True:
        time.sleep(1)
        gui_thread.kill()
