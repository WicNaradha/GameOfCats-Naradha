import matplotlib.pyplot as plt

fo = open('CtoC_Stresslog.csv','r')
a = fo.readlines()

xlist = []

alist = []
blist = []
clist = []
slist = []

a1list = []
b1list = []
c1list = []
s1list = []

for i in a:
    if 'Timestep' in i:
        x=int(i.split(':')[1].strip(' ##########\n'))
        xlist.append(x)
    if 'c0' in i.split(',')[1]:
        a=float(i.split(',')[4].split(':')[1])
        alist.append(round(a,3))
        b=float(i.split(',')[5].split(':')[1])
        blist.append(round(b,3))
        c=float(i.split(',')[6].split(':')[1])
        clist.append(round(c,3))
        s=float(i.split(',')[7].split(':')[1])
        slist.append(round(s,3))
    if 'c1' in i.split(',')[1]:
        a=float(i.split(',')[4].split(':')[1])
        a1list.append(round(a,3))
        b=float(i.split(',')[5].split(':')[1])
        b1list.append(round(b,3))
        c=float(i.split(',')[6].split(':')[1])
        c1list.append(round(c,3))
        s=float(i.split(',')[7].split(':')[1])
        s1list.append(round(s,3))

plt.figure()
plt.subplot(211)
plt.title('Cat c0 Stress:')
plt.plot(xlist,slist)

plt.figure()
plt.subplot(212)
plt.plot(xlist,s1list)

#plt.subplot(412)
#plt.title('Cat Hunger')
#plt.plot(xlist,alist,'g')

#plt.subplot(413)
#plt.title('Cat Thirst')
#plt.plot(xlist,blist,'b')

#plt.subplot(414)
#plt.title('Cat Fatigue')
#plt.plot(xlist,clist,'r')
plt.show()
        

