import matplotlib.pyplot as plt

fo = open('CLIlog.csv','r')
a = fo.readlines()

xlist = []

alist = []
blist = []
clist = []
slist = []

for i in a:
    if 'Timestep' in i:
        x=int(i.split(':')[1].strip(' ##########\n'))
        xlist.append(x)
    if 'CAT' == i.split(',')[0]:
        a=float(i.split(',')[4].split(':')[1])
        alist.append(round(a,3))
        b=float(i.split(',')[5].split(':')[1])
        blist.append(round(b,3))
        c=float(i.split(',')[6].split(':')[1])
        clist.append(round(c,3))
        s=float(i.split(',')[7].split(':')[1])
        slist.append(round(s,3))

plt.figure()
plt.subplot(411)
plt.title('Cat Stress:')
plt.plot(xlist,slist)

plt.subplot(412)
plt.title('Cat Hunger')
plt.plot(xlist,alist,'g')

plt.subplot(413)
plt.title('Cat Thirst')
plt.plot(xlist,blist,'b')

plt.subplot(414)
plt.title('Cat Fatigue')
plt.plot(xlist,clist,'r')
plt.show()
        

