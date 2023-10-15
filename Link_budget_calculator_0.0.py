import math
import matplotlib.pyplot as plt
import numpy as np 
from scipy.special import erfc

def Orbital_period(r,M_c):
    G = 6.67430*10**(-11)
    P = 2*math.pi*(r**3/(G*M_c))**0.5
    return P

def to_dB(a):
    bB = 10 * math.log10(a)
    return bB

M = int(input("Choose the number of your mission: "))
Mission_name = ["THEOS-2","Lunar Reconnaissance Orbiter","MarCO CubeSats","Mars Reconnaissance Orbiter","Akatsuki spacecraft"]

c = 299792458 
k = 1.3806503 * 10**(-23)
r_c = [6378 *10**3, 1737.5*10**3, 3389.5*10**3, 3389.5*10**3, 6051.8*10**3]
M_c = [5.9722*10**24, 7.348*10**22, 6.417*10**23, 6.417*10**23, 4.867*10**24]
h = [820 *10**3, 50*10**3, 1000*10**3, 300*10**3, 1000*10**3]

r_orbit = r_c[M]  + h[M] 
Swath_angle = [45, 6, 10, 0.5, 1]
Swath_angle_per_pixel = np.array([0.01, 0.07, 0.2, 0.005, 0.30])/60
Bit_per_pixel = [32, 8, 8, 32, 8]
Duty_Cycle = [1, 1, 0.05, 0.1, 0.25]
Dowlink_time = np.array([0.5,1,18,12,12])*3600

#---------------------- Data rate and dowlink data rate -------------------#
print("\n--------",Mission_name[M])
print("-------- Data rate and dowlink data rate -------\n")

P = Orbital_period(r_orbit,M_c[M])
omega = 2*math.pi/P
v_ground = omega * r_c[M]
v_orbit = omega *r_orbit
Pixel_size =  2* h[M] * math.tan(math.radians(Swath_angle_per_pixel[M]/2))
Swath_width = 2* h[M] * math.tan(math.radians(Swath_angle[M]/2))
Pixels_per_line = Swath_angle[M] / Swath_angle_per_pixel[M]
Bits_per_line = Pixels_per_line * Bit_per_pixel[M]
Lines_per_second = v_ground/Pixel_size
DR_SC = Lines_per_second * Bits_per_line
D_24h = DR_SC * 60 * 60 * 24 * Duty_Cycle[M]
DR_dowlink = D_24h/Dowlink_time[M]


print(f"{'Ground velocity:':<35}{v_ground:<10.2f}{'[m/s]':<}")
print(f"{'Swath width:':<35}{Swath_width:<10.2f}{'[m]':<}")
print(f"{'Pixel size:':<35}{Pixel_size:<10.2f}{'[m]':<}")
print(f"{'Pixels per line:':<35}{Pixels_per_line*10**-3:<10.2f}{'[k.pixel/line]':<}")
print(f"{'Bits per line:':<35}{Bits_per_line*10**-3:<10.2f}{'[k.bits/line]':<}")
print(f"{'Lines per second:':<35}{Lines_per_second:<10.2f}{'[line/s]':<}")
print(f"{'Spacecraft data rate:':<35}{DR_SC/10**9:<10.2f}{'[GBits/s]':<}")
print(f"{'Required dowlink data rate:':<35}{DR_dowlink/10**9:<10.2f}{'[GBits/s]':<}")

#----------------------------------------------------------------#
P_in = [150, 50, 10, 100, 200]
Trans_eff = [0.8, 0.8, 0.8, 0.8, 0.8]
Reciver_eff = [0.7, 0.7, 0.7, 0.7, 0.7]
Antenna_diameter_tr = [1, 0.3, 0.1, 3, 1.6]
Antenna_diameter_rec = [15, 15, 35, 35, 35]
Point_offset_tr = [0.12, 0.02, 1, 0.05, 0.1]
Point_offset_rec = [0, 0, 0, 0, 0]
Freq = np.array([ 2.2, 2.4, 8.4, 8.4, 8.5]) *10**9
Up_down_ratio = [221/240, 221/240, 749/880, 749/880, 749/880]


#---------------------- Dowlink margin -------------------#

print("\n--------Power received and noise density-------\n")
A_istropic_sphere = 4 * math.pi * h[M]**2
A_ant_rec = math.pi*(Antenna_diameter_rec[M]*0.5)**2
A_ant_str = math.pi*(Antenna_diameter_tr[M]*0.5)**2
lamb = c/Freq[M]
T_sys = [552,552,552,552,552]

P_rad = P_in[M] * Trans_eff[M]
P_rad_dBW = to_dB(P_rad)

G_tr = 4*math.pi*A_ant_str/(lamb**2)
G_tr_dB = to_dB(G_tr)

EIRP = P_rad * G_tr
EIRP_dBW = to_dB(EIRP)

L_fs = (4*math.pi*h[M]/lamb)**2
L_fs_dB = to_dB(L_fs)

L_At_db_90 = 0.06

Theta_half_P_tr = 21/(Freq[M]*(10**-9)*Antenna_diameter_tr[M])
L_offset_dB_tr= 12*(Point_offset_tr[M]/Theta_half_P_tr)**2
L_offset_tr = 10**(L_offset_dB_tr/10)

G_rec = 4*math.pi*A_ant_rec/(lamb**2)
G_rec_dB = to_dB(G_rec)

Theta_half_P_rec = 21/(Freq[M]*(10**-9)*Antenna_diameter_rec[M])
L_offset_dB_rec = 12*(Point_offset_rec[M]/Theta_half_P_rec)**2
L_offset_rec = 10**(L_offset_dB_rec/10)

Reciever_loss_dB = to_dB(1/Reciver_eff[M])

N_0 = k * T_sys[M]

# I_h_ideal = EIRP/A_istropic_sphere
# I_h = I_h_ideal * 10**(-L_At_db_90/10)


# Power_recieved = I_h * A_ant_rec *Reciver_eff[M]
# Power_recieved_dBW = EIRP_dBW - L_fs_dB - L_At_db_90 - Reciever_loss_dB + G_rec_dB #dB method

# E_bit = Power_recieved/DR_dowlink


# E_bit_N_0_ratio = E_bit/N_0
# E_bit_N_0_ratio_dB = to_dB(E_bit_N_0_ratio)



print(f"{'Radiated power:':<35}{P_rad:<10.2f}{'[W]':<}")
print(f"{'Peak transmitter antenna gain:':<35}{G_tr:<10.2f}")
print(f"{'Free space loss:':<35}{L_fs/10**12:<10.2f}{'[10^12]':<}")
print(f"{'Transmitter offset pointing loss:':<35}{L_offset_tr:<10.5f}")
print(f"{'Min atmospheric atenuation:':<35}{10**(L_At_db_90/10):<10.3f}")
print(f"{'Peak receiver antenna gain :':<35}{G_rec:<10.2f}")
print(f"{'Receiver loss :':<35}{Reciever_loss_dB:<10.2f}")
print(f"{'N_o :':<35}{N_0*10**22:<10.2f}{'[10^-22 W/Hz]':<}")
# print(f"{'Power recieved :':<35}{Power_recieved*10**9:<10.2f}{'[10^-9 W]':<}")
# print(f"{'E_bit :':<35}{E_bit*10**19:<10.2f}{'[10^-19 W]':<}")
# print(f"{'Received E_b/N_0: ':<35}{E_bit_N_0_ratio:<10.2f}{'[s.Hz]':<}")

print("\n--------Downlink budget -------\n")
Item_list = ['Trasmitter power:','Trasmitter line loss:','Trasmitter gain',
             'Offset pointing loss','Free Space loss:','Max atmospheric loss',
             'Receiver gain','Receiver pointing loss','Receiver line loss']

dB_list = [to_dB(P_in[M]),-to_dB((Trans_eff[M])**-1),G_tr_dB,
             -L_offset_dB_tr,-L_fs_dB,L_At_db_90,
             G_rec_dB,-L_offset_dB_rec,-to_dB((Reciver_eff[M])**-1),
             -to_dB(DR_dowlink),-to_dB(N_0),]


print(f"{'Item:':<35}{'Value:':<10}{'':<12}{'Budget':<}")
Budget_list = []

for i in range (len(Item_list)):
    Budget_list.append(sum(dB_list[0:i+1]))
    if i == 0:
        print(f"{Item_list[i]:<35}{dB_list[i]:<10.4f}{'[dBW]':<12}{Budget_list[i]:<8.2f}{'[dBW]':<5}")
    else:
        print(f"{Item_list[i]:<35}{dB_list[i]:<10.4f}{'[dB]':<12}{Budget_list[i]:<8.2f}{'[dBW]':<5}")
print("-------------------------------------------------------------------")
print(f"{'Signial power received':<57}{Budget_list[-1]:<8.2f}{'[dBW]'}")
print(f"{'Bit energy received':<57}{Budget_list[-1] - to_dB(DR_dowlink):<8.2f}{'[dBJ]'}")
print(f"{'Bit energy to noise density ratio':<57}{Budget_list[-1] - to_dB(DR_dowlink) -to_dB(N_0):<8.2f}{'[dB]'}")

EbN0dBs = np.arange(start=-4,stop = 13, step = 1)
BER_theory = 0.5*erfc(np.sqrt(10**(EbN0dBs/10)))

fig, ax = plt.subplots(nrows=1,ncols = 1)
ax.semilogy(EbN0dBs,BER_theory,marker='',linestyle='-',label='BPSK Theory')
ax.set_xlabel('E_b/N_0(dB)')
ax.set_ylabel('BER (P_b)')
ax.set_title('Probability of Bit Error for BPSK over AWGN channel')
ax.set_xlim(-5,13)
ax.grid()
ax.legend();plt.show()


# Pixel_bits = 32
# Duty_Cycle = 1
# Downlink_time = 0.5
# 


# Tangential_velocity = 
# Angular_velocty = 
# Ground_velocity =
# 
# Swath_length = 
# 
# Bits_per_line = 
# Ground_velocity = 


#d =
#B =
#DR =
#Band = 
#DR_A/D = f_analog * NYQ * B_per_wave
#T_n = #depends on frequency
#A_sphere = 4 * math.pi() * d**2
#P_rad = P_in * Trans_eff
#G_ant = rad_eff * (4*math.pi()*A_ant/lamb**2) = I_recived/I_isotropic
#EIRP = P_rad *G_ant
#I = EIRP/A_sphere
#E_b = P_sig/B_rate
#N_density = k*T_s
#N_power = N_density*Band
#P_reci = I * A_ant * reciv_eff
#C = B *log_2(1+S_power/N_power)
#SNR = (E_b/N_power) * (DR/band_noise) # SNR = E_b/N_power if Band_noise = DR




#Margin = P_tx * G_tx * G_rx /(L_tx * L_fs * L_rx * N_i)
#Margin = EIRP - L_fs - L_extra + G/T ####SNR?
#SNR = EIRP - L_fs -L_extra + G/T - 10 * log_10(k*DR)

#L_fs = 20 log (4*math.pi()*d/lamb) [dB]
#At = A_90/(math.sin(alpha))

#E_b = 