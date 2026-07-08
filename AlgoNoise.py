import matplotlib.pyplot as plt
import numpy as np

# we are looking in the range of 17e6-24e6 but we scaled this down by a factor of 1000
# for the program to generate a plot in a timely manner
def generate_noise_bursts(spec, freq_grid, dt=0.1, duration=900, center_freq=20e6, width=5e6):
    n_freq, n_time = spec.shape
    t = np.arange(n_time) * dt

    envelope = np.exp(-(t-duration/2)**2/(2*(duration/3)**2))

    envelope *= 0.7 + 0.3 * np.random.rand(n_time)

    freq_weight = np.exp(-(freq_grid-center_freq) ** 2 / (2 * width ** 2))

    n_bursts = 2500
    for i in range(n_bursts):   # generating bursts of noise
        burst_time = np.random.choice(n_time, p=envelope/envelope.sum())

        burst_freq = np.random.choice(n_freq, p=freq_weight/freq_weight.sum())

        amp = np.random.exponential(4)

        sigma_t = np.random.uniform(1,15)   # uniform distribution across the range
        sigma_f = np.random.uniform(1,6)

        tt = np.arange(n_time)
        ff = np.arange(n_freq)

        T = np.exp(-(tt-burst_time)**2/(2*sigma_t**2))
        F = np.exp(-(ff-burst_freq)**2/(2*sigma_f**2))
# generated bursts in the 19000-21000 range more frequently than bursts in the range outside of the 19000-21000 range
        if 19000 < burst_freq < 21000:  # the bursts in the range 19000-21000
            if np.random.rand() < 0.8:  # random float point 0-1 generated if less than 0.8 a burst is generated
                spec += amp * np.outer(F,T)
        else:   # places not in 19000-21000
            if np.random.rand() < 0.25: # if less than 0.25 a burst is generated
                spec += amp * np.outer(F,T)

    return spec

def generate_noise():
    freq = 24000
    time = 1000
    spec = np.random.normal(0.0, 0.2, (freq, time))
    freq_grid = np.linspace(17e6, 24e6, 24000)
    spec = generate_noise_bursts(spec, freq_grid, dt=0.1, duration=900, center_freq=20e6, width=5e6)

    for i in range(75): # randomly generates noise spec in the plot's range
        y = np.random.randint(17000,24000)
        x = np.random.randint(0,1000)

        spec[y-13:y+27, x-1:x+2] += 15 # -13:+27 and -1:+2 dictate the size of the specs

    for j in range(0, 3): # generates up to three radio signal lines
        t = np.arange(1000) * 0.1

        a = np.random.randint(17500, 18250) # random bar in the range
        b = a + 50 # thickness of the line

        c = np.random.randint(21000, 22000) # random bar in the range
        d = c + 50 # thickness of the line


        if np.random.rand() < 0.35: # random sin function with in ranges for intensity
            spec[a:b, :] += np.random.randint(2,7) + np.sin(np.random.randint(2, 5) * t)

        if np.random.rand() < 0.35: # random sin function with in ranges for intensity
            spec[c:d, :] += np.random.randint(2,7) + np.sin(np.random.randint(2, 5) * t)

    plt.ylim(17000,24000)   # plot range of 17000-24000

    plt.imshow(spec, origin = 'lower', aspect = 'auto')
    plt.title('Noise')
    plt.colorbar()
    plt.show()

generate_noise() # call the function
