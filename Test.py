#Eb/N0 Vs BER for BPSK over AWGN (complex baseband model)
# © Author: Mathuranathan Viswanathan (gaussianwaves.com)
import numpy as np #for numerical computing
import matplotlib.pyplot as plt #for plotting functions
from scipy.special import erfc #erfc/Q function

#---------Input Fields------------------------
nSym = 10**3 # Number of symbols to transmit
EbN0dBs = np.arange(start=-4,stop = 13, step = 1) # Eb/N0 range in dB for simulation
BER_sim = np.zeros(len(EbN0dBs)) # simulated Bit error rates

P = 0.00001
M = 32 #Number of points in BPSK constellation
m = np.arange(0,M) #all possible input symbols
A = 1; #amplitude
constellation = A*np.cos(m/M*np.pi)  #reference constellation for BPSK
constellation_phase = m/M*np.pi

#------------ Transmitter---------------
inputSyms = np.random.randint(low=0, high = M, size=nSym) #Random 1's and 0's as input to BPSK modulator
s = constellation[inputSyms] #modulated symbols
print(s)
fig, ax1 = plt.subplots(nrows=1,ncols = 1)
ax1.plot(A*np.cos(constellation_phase),A*np.sin(constellation_phase),'*')
ax1.set(xlim=(-2, 2), ylim=(-2, 2))
#----------- Channel --------------
#Compute power in modulatedSyms and add AWGN noise for given SNRs


Errors_for_EbN0d_list = []
for j,EbN0dB in enumerate(EbN0dBs):
    EbN0d = 10**(EbN0dB/10) #SNRs to linear scale #Average squared signal value (power in the vector)
    N0 = P/EbN0d # Find the noise spectral density
    N_list = np.sqrt(N0/2)*np.random.standard_normal(s.shape)

    rec_list = N_list + s
    # print(s)
    # print(N_list)
    # print(rec_list)

    Errors = 0
    for i in range(1,len(rec_list)-1):
        signal_position = np.where(constellation==s[i])[0][0]
        try:
            if rec_list[i] > 0:
                if rec_list[i] < constellation[signal_position+1] or rec_list[i] > constellation[signal_position-1]:
                    Errors += 1
                    # print(constellation[signal_position+1])
                    # print(rec_list[i])
                    # print(constellation[signal_position-1])
                    # print("aaaaa")

            if rec_list[i] < 0:
                if rec_list[i] < constellation[signal_position+1] or rec_list[i] > constellation[signal_position-1]:
                    Errors += 1
                    # print(constellation[signal_position+1])
                    # print(rec_list[i])
                    # print(constellation[signal_position-1])
                    # print("aaaaa")
        except:
            pass
    
    Errors_for_EbN0d_list.append(Errors)

Errors_for_EbN0d_list = np.array(Errors_for_EbN0d_list)


print(Errors_for_EbN0d_list)
print(Errors_for_EbN0d_list/nSym)
BER_sim = Errors_for_EbN0d_list/nSym
BER_theory = 0.5*erfc(np.sqrt(10**(EbN0dBs/10)))

fig, ax = plt.subplots(nrows=1,ncols = 1)
ax.semilogy(EbN0dBs,BER_sim,color='r',marker='o',linestyle='',label='BPSK Sim')
ax.semilogy(EbN0dBs,BER_theory,marker='',linestyle='-',label='BPSK Theory')
ax.set_xlabel('$E_b/N_0(dB)$');ax.set_ylabel('BER ($P_b$)')
ax.set_title('Probability of Bit Error for BPSK over AWGN channel')
ax.set_xlim(-5,13);ax.grid(True);
ax.legend();plt.show()