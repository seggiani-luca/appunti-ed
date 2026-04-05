import numpy as np
import matplotlib.pyplot as plt

# probability constants
tau = 2.5 * 10 ** -14

def get_vels(num):
    return np.random.gamma(shape=2, scale=tau, size=num)

# time constants
max_time = 10 ** -12
steps = 10000
delta = max_time / (steps - 1)

# physical constants
q = 1.6 * 10 ** -19
E = 1
m = 9.3 * 10 ** -31
a = (q * E) / m
electrons = 100

# state variables
s = np.zeros((steps, electrons))
v = np.zeros((steps, electrons))

# simulate
colls = get_vels(electrons)
coll_counts = np.zeros(electrons)
for i in range(1, steps):
    time = i * delta
    
    for j in range(electrons):
        # velocity
        v[i, j] = v[i - 1, j] + a * delta
        while time > coll_counts[j] * colls[j]:
            # collide
            v[i, j] = 0
            coll_counts[j] += 1 
        
        # space
        s[i, j] = s[i - 1, j] + v[i, j] * delta

# results
act_avg = np.mean(v) 
print(f"Average velocity was: {act_avg}")

exp_avg = a * tau
print(f"Expected velocity was: {exp_avg}")

# more results
v_avgs = np.zeros(steps)
for i in range(steps):
    v_avgs[i] = np.mean(v[i, :])

# plot
t = np.linspace(0, max_time, steps)

plt.figure()
for j in range(electrons):
    plt.plot(t, v[:, j], alpha=0.5)  # velocity of each electron
plt.title("Velocities of all electrons")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.grid()
plt.tight_layout()
plt.savefig("multiple_electron_velocity.png", dpi=300)

plt.figure()
plt.plot(t, v_avgs)
plt.title("Average velocity of all electrons")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.grid()
plt.tight_layout()
plt.savefig("multiple_electron_avg_velocity.png", dpi=300)

plt.figure()
for j in range(electrons):
    plt.plot(t, s[:, j], alpha=0.5)  # position of each electron
plt.title("Positions of all electrons")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.grid()
plt.tight_layout()
plt.savefig("multiple_electron_position.png", dpi=300)

plt.figure()

v_vals = np.linspace(0, np.max(v), 50)
pdf_vals = (1 / act_avg) * np.exp(- v_vals / act_avg) 

plt.hist(v.flatten(), bins=100, density=True, alpha=0.7, color='blue', label='Sampled')
plt.plot(v_vals, pdf_vals, color='red', lw=2, label='Analytical')

plt.title("Multiple electron distribution")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Probability density")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("multiple_electron_distrib.png", dpi=300)

plt.show()
