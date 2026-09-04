import numpy as np
import matplotlib.pyplot as plt
from math import comb
from scipy.stats import binom

p_co = np.logspace(-6,0,500)

eta_ch = 10**(-3)           #channel transmittance [0;1]
eta_det = 0.75              #detector efficiency [0;1]
eta = eta_ch*eta_det
pd = 10**(-7)               #dark count probability [0;1]



N=10**(6)                   #Number of emitted signal
p_B = 0.5                   #probability to choose on basis
p_BS = p_B**2 + (1-p_B)**2


nps=int(round(N*p_BS*(eta+(1-eta)*pd)))    #Expected number of click
print (nps)

QBER_th1 = 0.11
TH1 = int(np.floor(nps*QBER_th1))


QBER = (eta*(p_co)+0.5*(1-eta)*pd)/(eta+(1-eta)*pd)
plt.plot(p_co,QBER, label=r'$QBER_{ref}$')

def pf(TH,nps,QBER):
    return binom.sf(TH, nps, QBER)


pfQKD1 = pf(TH1,nps,QBER)
plt.plot(p_co,pfQKD1, label=r'$p_{f,tx}$ (BB84)')



# P-256 uncompressed
pftx256u = 1-(1-p_co)**520
# plt.plot(p_co,pftx256u, label=r'$p_{f,tx}$ (P-256 unc.)')

# P-384 uncompressed
pftx384u = 1-(1-p_co)**776
# plt.plot(p_co,pftx384u, label=r'$p_{f,tx}$ (P-384 unc.)')

# P-521 uncompressed
pftx521u = 1-(1-p_co)**1064
# plt.plot(p_co,pftx521u, label=r'$p_{f,tx}$ (P-521 unc.)')

# pfex for uncompressed
pfex256u = (1-(1-pftx256u)**2) 
plt.plot(p_co,pfex256u, label=r'$p_{f,ex}$ (P-256 unc.)')

pfex384u = (1-(1-pftx384u)**2)
plt.plot(p_co,pfex384u, label=r'$p_{f,ex}$ (P-384 unc.)')

pfex521u = (1-(1-pftx521u)**2)
plt.plot(p_co,pfex521u, label=r'$p_{f,ex}$ (P-521 unc.)')


#P-256 uncompressed + C1(650, 520, 13) ; R=0.8
n1=650
k2=520
t1=13
nbr_cw_256_c1 = 1

#P-384 uncompressed + C1(971,776,20)
n2=971
k2=776
t2=20
nbr_cw_384_c1 = 1

#P-521 uncompressed + C1(662,532,13)
n3=662
k3=532
t3=13
nbr_cw_521_c1 = 2


#P-256 uncompressed + C2(865,520,37) ; R=0.6
n4=865
k4=520
t4=37
nbr_cw_256_c2 = 1

#P-384 uncompressed + C2(643,388,26) ; R=0.6
n5=643
k5=388
t5=26
nbr_cw_384_c2 = 2

#P-521 uncompressed + C2(887, 532, 38) ; R=0.6
n6=887
k6=532
t6=38
nbr_cw_521_c2 = 2


def Pew(t,n,p_co):
    return binom.sf(t,n,p_co)

Pew1= Pew(t1,n1,p_co)
Pew2= Pew(t2,n2,p_co)
Pew3= Pew(t3,n3,p_co)
Pew4= Pew(t4,n4,p_co)
Pew5= Pew(t5,n5,p_co)
Pew6= Pew(t6,n6,p_co)

p_ftx1= 1-((1-Pew1)**(nbr_cw_256_c1))
p_ftx2 = 1-((1-Pew2)**(nbr_cw_384_c1))
p_ftx3 = 1-((1-Pew3)**(nbr_cw_521_c1))
p_ftx4 = 1-((1-Pew4)**(nbr_cw_256_c2))
p_ftx5 = 1-((1-Pew5)**(nbr_cw_384_c2))
p_ftx6 = 1-((1-Pew6)**(nbr_cw_521_c2))

p_fex1 = 1-((1-p_ftx1)**2)
p_fex2 = 1-((1-p_ftx2)**2)
p_fex3 = 1-((1-p_ftx3)**2)
p_fex4 = 1-((1-p_ftx4)**2)
p_fex5 = 1-((1-p_ftx5)**2)
p_fex6 = 1-((1-p_ftx6)**2)



plt.plot(p_co,p_fex1, label=r'$p_{f,ex}$(P-256 unc.+$C_1$)')
# plt.plot(p_co,p_fex2, label=r'$p_{f,ex}$(P-384 unc.+$C_1$)')
plt.plot(p_co,p_fex3, label=r'$p_{f,ex}$(P-521 unc.+$C_1$)')
plt.plot(p_co,p_fex4, label=r'$p_{f,ex}$(P-256 unc.+$C_2$)')
# plt.plot(p_co,p_fex5, label=r'$p_{f,ex}$(P-384 unc.+$C_2$)')
# plt.plot(p_co,p_fex6, label=r'$p_{f,ex}$(P-521 unc.+$C_2$)')


plt.xscale('log')
plt.xlabel(r"$\varepsilon_{ch}$")
plt.grid(True, which="both", linestyle="-", alpha=0.5)

plt.legend(loc='upper left', fontsize=8)
plt.show()