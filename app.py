import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("💊 Advanced Drug Simulator (Personalized)")

st.markdown("⚠️ Educational model only — not for medical use")

# --- Inputs ---
age = st.slider("Age", 10, 80, 25)
weight = st.slider("Weight (kg)", 30, 120, 60)
dose = st.slider("Dose (mg)", 50, 1000, 500)
tau = st.slider("Dosing interval (hours)", 4, 24, 8)
num_doses = st.slider("Number of doses", 1, 10, 5)

# --- Parameters ---
Vd = 0.7 * weight

k = 0.15 - (age * 0.001)  # elimination rate
ka = 1.0  # absorption rate (fixed for simplicity)

# --- Time ---
t = np.linspace(0, 48, 500)
C = np.zeros_like(t)

# --- Multi-dose calculation ---
for n in range(num_doses):
    dose_time = n * tau
    mask = t >= dose_time
    t_shifted = t[mask] - dose_time

    C[mask] += (dose * ka / (Vd * (ka - k))) * (
        np.exp(-k * t_shifted) - np.exp(-ka * t_shifted)
    )

# --- Plot ---
fig, ax = plt.subplots()
ax.plot(t, C)

# Ranges
therapeutic_min = 5
therapeutic_max = 15
toxic_level = 20

ax.axhline(therapeutic_min, linestyle='--')
ax.axhline(therapeutic_max, linestyle='--')
ax.axhline(toxic_level, linestyle=':')

# Mark dose times
for n in range(num_doses):
    ax.axvline(n * tau, linestyle=':', alpha=0.3)

ax.set_xlabel("Time (hours)")
ax.set_ylabel("Concentration (mg/L)")
ax.set_title("Repeated Dose Drug Concentration")

st.pyplot(fig)

# --- Interpretation ---
st.subheader("🧠 Interpretation")

peak = max(C)

if peak > toxic_level:
    st.error("⚠️ Risk of drug accumulation → possible toxicity")
elif peak < therapeutic_min:
    st.warning("⚠️ Drug may not reach effective levels")
else:
    st.success("✅ Drug stays within therapeutic window")

half_life = np.log(2) / k
st.write(f"Half-life ≈ {round(half_life, 2)} hours")