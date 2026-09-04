import numpy as np
import matplotlib.pyplot as plt
from math import comb
from scipy.stats import binom
from scipy.optimize import brentq

ech = np.logspace(-5, np.log10(0.5), 500)


#BB84 Section

eta_det = 0.75              #detector efficiency [0;1]

pd = 10**(-7)               #dark count probability [0;1]

d1 = 15                     #communication distance [Km]
d2 = 20
d3 = 25
d4 = 30

eta_ch1 = 10**(-(0.2*d1)/10)
eta1 = eta_ch1*eta_det

eta_ch2 = 10**(-(0.2*d2)/10)
eta2 = eta_ch2*eta_det

eta_ch3 = 10**(-(0.2*d3)/10)
eta3 = eta_ch3*eta_det

eta_ch4 = 10**(-(0.2*d4)/10)
eta4 = eta_ch4*eta_det

p_B = 0.5                   #probability to select one basis
p_BS = p_B**2 + (1-p_B)**2


Y1 = p_BS*(eta1+(1-eta1)*pd)
Y2 = p_BS*(eta2+(1-eta2)*pd)
Y3 = p_BS*(eta3+(1-eta3)*pd)
Y4 = p_BS*(eta4+(1-eta4)*pd)


QBER1 = (eta1*ech+0.5*(1-eta1)*pd)/(eta1+(1-eta1)*pd)
# plt.plot(ech,QBER1, label='QBER1')

QBER2 = (eta2*ech+0.5*(1-eta2)*pd)/(eta2+(1-eta2)*pd)
# plt.plot(ech,QBER2, label='QBER2')

QBER3 = (eta3*ech+0.5*(1-eta3)*pd)/(eta3+(1-eta3)*pd)
# plt.plot(ech,QBER3, label='QBER3')

QBER4 = (eta4*ech+0.5*(1-eta4)*pd)/(eta4+(1-eta4)*pd)
# plt.plot(ech,QBER4, label='QBER4')



r_QBER1 = np.maximum(0, 1-2*(-QBER1*np.log2(QBER1)-(1-QBER1)*np.log2(1-QBER1)))
# plt.plot(ech,r_QBER1, label=r'$r_{\infty, 1}$')

r_QBER2 = np.maximum(0, 1-2*(-QBER2*np.log2(QBER2)-(1-QBER2)*np.log2(1-QBER2)))
# plt.plot(ech,r_QBER2, label=r'$r_{\infty, 2}$')

r_QBER3 = np.maximum(0, 1-2*(-QBER3*np.log2(QBER3)-(1-QBER3)*np.log2(1-QBER3)))
# plt.plot(ech,r_QBER3, label=r'$r_{\infty, 3}$')

r_QBER4 = np.maximum(0, 1-2*(-QBER4*np.log2(QBER4)-(1-QBER4)*np.log2(1-QBER4)))
# plt.plot(ech,r_QBER4, label=r'$r_{\infty, 4}$')


#ECDH Section

H2 = -(ech*np.log2(ech)+(1-ech)*np.log2(1-ech))
C = 1-H2
# plt.plot(ech,C,label='Channel Capacity')

Rkp_p256 = (128/1040)*C
plt.plot(ech, Rkp_p256, label=r'$\mathcal{R}_{KM}^{P-256}$')

Rkp_p384 = (192/1552)*C
# plt.plot(ech,Rkp_p384,label=r'$\mathcal{R}_{KM}^{P-384}$')

Rkp_p521 = (256/2128)*C
# plt.plot(ech,Rkp_p521,label=r'$\mathcal{R}_{KM}^{P-521}$')

Rkp1 = r_QBER1*(p_BS*(eta1+(1-eta1)*pd))
plt.plot(ech, Rkp1, label=r'$\mathcal{R}_{KM}^{BB84}$' + f'({d1} km)')

Rkp2 = r_QBER2*(p_BS*(eta2+(1-eta2)*pd))
plt.plot(ech, Rkp2, label=r'$\mathcal{R}_{KM}^{BB84}$' + f'({d2} km)')

Rkp3 = r_QBER3*(p_BS*(eta3+(1-eta3)*pd))
plt.plot(ech, Rkp3, label=r'$\mathcal{R}_{KM}^{BB84}$' + f'({d3} km)')

Rkp4 = r_QBER4*(p_BS*(eta4+(1-eta4)*pd))
plt.plot(ech, Rkp4, label=r'$\mathcal{R}_{KM}^{BB84}$' + f'({d4} km)')



#custom point

pB_target = 0.5                                         #probability to select one basis
pBS_target = pB_target**2 + (1-pB_target)**2            #probability for successful basis match, 0.5 if unbiased
eta_det_target = 0.70                                   #detector efficiency
pd_target = 10**(-7)                                    #dark count probability
alpha_target = 0.2                                      #loss coefficient

ech_target = 5*10**(-2)

St_target = 128                                         #security strength - table
npk_target = 520                                        #length of public key - table


def H(x):
    return -x*np.log2(x) - (1-x)*np.log2(1-x)

def Rkp_ECDH(St, npk, ech_target):
    return (St/(2*npk))*(1-H(ech_target))

def eta_ch(d):
    return 10**(-(alpha_target*d)/10)

def Q(ech_target, d):
    return (eta_det_target*eta_ch(d)*ech_target + (1-eta_det_target*eta_ch(d))*0.5*pd_target)/(eta_det_target*eta_ch(d) + (1-eta_det_target*eta_ch(d))*pd_target)

def Rkp_QKD(ech_target, d):
    return (pBS_target * (eta_det_target*eta_ch(d) + (1-eta_det_target*eta_ch(d))*pd_target) * np.maximum(0, 1-2*H(Q(ech_target, d))))

def equation(d, ech_target, St, npk):
    return Rkp_QKD(ech_target, d)-Rkp_ECDH(St, npk, ech_target)


f_min = equation(0, ech_target, St_target, npk_target)
f_max = equation(500, ech_target, St_target, npk_target)


if f_min == 0:
    d_solution = 0
    print("Maximum distance =", d_solution, "km")


elif f_min*f_max < 0:
    d_solution = brentq(equation, 0, 500, args=(ech_target, St_target, npk_target))
    print("Maximum distance =", d_solution, "km")


else:
    print("No intersection found between 0 and 500 km.")
    print("Equation at 0 km =", f_min)
    print("Equation at 500 km =", f_max)



plt.xscale('log')
plt.xlabel(r"$\varepsilon_{ch}$")
plt.grid(True, which="both", linestyle="-", alpha=0.5)
plt.legend(loc='upper left', fontsize=8)
plt.show()
