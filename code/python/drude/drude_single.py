import numpy as np
import matplotlib.pyplot as plt

# probability constants
tau = 2.5 * 10 ** -14

def get_coll():
    return np.random.exponential(scale=tau)

# time constants
max_time = 10 ** -12
steps = 10000
delta = max_time / (steps - 1)

# physical constants
q = 1.6 * 10 ** -19
E = 1
m = 9.3 * 10 ** -31
a = (q * E) / m

# state variables
s = np.zeros(steps)
v = np.zeros(steps)

# simulate
next_coll = get_coll()
for i in range(1, steps):
    time = i * delta

    # velocity
    v[i] = v[i - 1] + a * delta
    while time > next_coll:
        # collide
        v[i] = 0
        next_coll += get_coll() 

    # space
    s[i] = s[i - 1] + v[i] * delta

# results
f_s = s[steps - 1]
f_t = max_time
act_avg = f_s / f_t
print(f"Final space was: {f_s}")
print(f"Final time was: {f_t}")
print(f"Average velocity was: {act_avg}")

exp_avg = a * tau
print(f"Expected velocity was: {exp_avg}")

# plot
t = np.linspace(0, max_time, steps)

plt.figure()
plt.plot(t, v)
plt.title("Velocity of single electron")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.grid()
plt.tight_layout()
plt.savefig("single_electron_velocity.png", dpi=300)

plt.figure()
plt.plot(t, s)
plt.title("Position of single electron")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.grid()
plt.tight_layout()
plt.savefig("single_electron_position.png", dpi=300)

plt.figure()

v_vals = np.linspace(0, np.max(v), 50)
pdf_vals = (1 / act_avg) * np.exp(- v_vals / act_avg) 

plt.hist(v.flatten(), bins=100, density=True, alpha=0.7, color='blue', label='Sampled')
plt.plot(v_vals, pdf_vals, color='red', lw=2, label='Analytical')

plt.title("Single electron distribution")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Probability density")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("single_electron_distrib.png", dpi=300)

plt.show()
