import matplotlib.pyplot as plt
import numpy as np

# we are looking in the range of 17e6-24e6 but we scaled this down by a factor of 1000
# for the program to generate a plot in a timely manner
def generate_io_a(spec, freq_grid, dt=0.1, duration=900, center_freq=20e6, width=5e6):
    n_freq, n_time = spec.shape
    t = np.arange(n_time) * dt

    envelope = np.exp(-(t-duration/2)**2/(2*(duration/3)**2))

    envelope *= 0.7 + 0.3 * np.random.rand(n_time)

    freq_weight = np.exp(-(freq_grid-center_freq) ** 2 / (2 * width ** 2))

    n_bursts = 2500
    for i in range(n_bursts):   # generating bursts of noise
        burst_time = np.random.choice(n_time, p=envelope/envelope.sum())

        burst_freq = np.random.choice(n_freq, p=freq_weight/freq_weight.sum())

        amp = np.random.exponential(20) # controls the magnitude of the bursts

        sigma_t = np.random.uniform(1,15)   # uniform distribution across the range
        sigma_f = np.random.uniform(1,6)

        tt = np.arange(n_time)
        ff = np.arange(n_freq)

        T = np.exp(-(tt-burst_time)**2/(2*sigma_t**2))
        F = np.exp(-(ff-burst_freq)**2/(2*sigma_f**2))
# generated bursts in the 19000-21000 range more frequently than bursts in the range outside the 19000-21000 range
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
    spec = generate_io_a(spec, freq_grid, dt=0.1, duration=900, center_freq=20e6, width=5e6)

    for i in range(75): # randomly generates noise spec in the plot's range
        y = np.random.randint(17000,24000)
        x = np.random.randint(0,1000)

        spec[y-17:y+23, x-1:x+2] += 50 # -13:+27 and -1:+2 dictate the size of the specs

    factor = np.random.randint(10,20) # random factor to give different sizes of the storm
    print('Scaling is multiplied by a factor of', factor)   # printing the factor
    t = np.random.randint(100, 200) # storm starts randomly in the range on the x axis
    s = np.random.randint(500, 600)  # using s as a cut off point
    y = np.random.randint(15000, 17000) # storm starts randomly in the range on y axis
    for k in range(300):    # the bars increase in size
        x = np.random.randint(t,t + 5)  # picks a starting point for the bar on the x axis
        t += np.random.randint(2, 10)  # each bar moves over a random amount on the x axis
        p = np.random.randint(1, 8)    # thickness of the bar

        d = np.random.randint(20,60) * factor    # changes the lower step length of the line
        f = np.random.randint(30,60) * factor    # changes the upper step length of the line
        s += np.random.randint(15, 40)  # increase in the cut off point
        y += np.random.randint(5, 25)   # adds the upward trend
        b = np.random.randint(y - 75, y + 75) # adds randomization


        # choose local extents
        # controls the variable intensity of the bars

        h = d + f
        w = 2 * p
        ymin = max(0, b - int(d))
        ymax = min(spec.shape[0], b + int(f))
        xmin = max(0, x - int(w // 2))
        xmax = min(spec.shape[1], x + int(w // 2))

        yy = np.arange(ymin, ymax)[:, None] # for gauss equation
        xx = np.arange(xmin, xmax)[None, :]
        Y = yy - b
        X = xx - x

        # anisotropic Gaussian sigma (controls vertical/horizontal spread)
        sigma_y = max(3.0, h * 0.25)
        sigma_x = max(1.0, w * 0.5)

        gauss = np.exp(-0.5 * ((Y / sigma_y) ** 2 + (X / sigma_x) ** 2))

        # add scaled gaussian
        spec[ymin:ymax, xmin:xmax] += 20.0 * gauss  # tune amplitude
        if s > 3600:    # bars stop increasing
           break

    for w in range(100):    # bars start to decrease in size
        d = np.random.randint(15, 40) * factor  # changes the lower step length of the line
        f = np.random.randint(25, 40) * factor  # changes the upper step length of the line
        x = np.random.randint(t, t + 5)
        t += np.random.randint(2, 10)
        p = np.random.randint(1, 8)
        b = np.random.randint(y - 75, y + 75)
        s -= np.random.randint(10, 40)


        # choose local extents
        h = d + f
        w = 2 * p
        ymin = max(0, b - int(d))
        ymax = min(spec.shape[0], b + int(f))
        xmin = max(0, x - int(w // 2))
        xmax = min(spec.shape[1], x + int(w // 2))

        yy = np.arange(ymin, ymax)[:, None]
        xx = np.arange(xmin, xmax)[None, :]
        Y = yy - b
        X = xx - x

        # anisotropic Gaussian sigma (controls vertical/horizontal spread)
        sigma_y = max(3.0, h * 0.25)
        sigma_x = max(1.0, w * 0.5)

        gauss = np.exp(-0.5 * ((Y / sigma_y) ** 2 + (X / sigma_x) ** 2))

        # add scaled gaussian
        spec[ymin:ymax, xmin:xmax] += 20.0 * gauss  # tune amplitude



    for j in range(0, 4): # generates up to three radio signal lines
        t = np.arange(1000) * 0.1

        a = np.random.randint(17500, 18250) # random bar in the range
        b = a + 50  # thickness of the line

        c = np.random.randint(21000, 22000) # random bar in the range
        d = c + 50  # thickness of the line


        if np.random.rand() < 0.35: # random sin function with in ranges for intensity
            spec[a:b, :] += np.random.randint(4,14) + 8 * np.sin(np.random.randint(2, 5) * t)

        if np.random.rand() < 0.35: # random sin function with in ranges for intensity
            spec[c:d, :] += np.random.randint(4,14) + 8 * np.sin(np.random.randint(2, 5) * t)

    plt.ylim(15000,24000)   # plot range of 17000-24000

    plt.imshow(spec, origin = 'lower', aspect = 'auto')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (kHz)')
    plt.title(f'Io-D: Factor {factor}')
    plt.colorbar()
    plt.show()

generate_noise() # call the function








