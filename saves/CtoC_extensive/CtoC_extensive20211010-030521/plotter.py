import matplotlib.pyplot as plt

fo = open('CtoC_extensivelog.csv','r')
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

t = 0

for i in a:
    if 'Timestep' in i:
        x=int(i.split(':')[1].strip(' ##########\n'))
        xlist.append(x)
        s1list.append(0.00)
    if 'CAT' in i.split(',')[0]:
        if 'c0' in i.split(',')[1]:
            a=float(i.split(',')[5].split(':')[1])
            alist.append(round(a,3))
            b=float(i.split(',')[6].split(':')[1])
            blist.append(round(b,3))
            c=float(i.split(',')[7].split(':')[1])
            clist.append(round(c,3))
            s=float(i.split(',')[9].split(':')[1])
            slist.append(round(s,3))
        if 'c1' in i.split(',')[1]:
            a=float(i.split(',')[10].split(':')[1])
            a1list.append(round(a,3))
            b=float(i.split(',')[11].split(':')[1])
            b1list.append(round(b,3))
            c=float(i.split(',')[7].split(':')[1])
            c1list.append(round(c,3))
            s=float(i.split(',')[9].split(':')[1])
            s1list[x] = s
        
plt.figure()
plt.subplot(411)
plt.title('Male Cat Scent: Red')
plt.plot(xlist,slist,'r')

plt.subplot(412)
plt.title('Female Cat Scent: Blue')
plt.plot(xlist,s1list,'b')

plt.subplot(413)
plt.title('Female Cat Concieved Count:')
plt.plot(xlist,a1list,'g')

plt.subplot(414)
plt.title('Female Cat CPS Change:')
plt.plot(xlist,b1list,'orange')

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
        

