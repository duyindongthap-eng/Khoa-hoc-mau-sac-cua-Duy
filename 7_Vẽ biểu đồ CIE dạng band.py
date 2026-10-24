import streamlit as st
import colour
import matplotlib.pyplot as plt
import numpy as np

place = st.empty()

def wavelength_to_rgb(wavelength):
    gamma = 0.8
    intensity_max = 255
    
    if 380 <= wavelength < 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength < 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength < 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength < 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength < 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 780:
        attenuation = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = G = B = 0.0
        
    return [int(R * intensity_max), int(G * intensity_max), int(B * intensity_max)]

wavelengths = np.linspace(400, 700, 301)
rgb_list = [wavelength_to_rgb(wl) for wl in wavelengths]
color_band = np.array(rgb_list, dtype=np.uint8)


grid_band = np.repeat(color_band[np.newaxis, :, :], 40, axis=0)

fig, ax = plt.subplots(figsize=(10, 3))

ax.imshow(grid_band, extent=[400, 700, 0, 10], aspect='auto')

ax.set_title("CIE VISIBLE SPECTRUM BAND\nRange: 400nm - 700nm", fontsize=16, fontweight='bold', pad=12, loc='center')
ax.set_xlabel("Bước sóng - $\lambda$ (nm)", fontsize=16, fontweight='bold', labelpad=8)

ax.set_xlim(400, 700)
ax.set_xticks(np.arange(400, 701, 50)) 

ax.get_yaxis().set_visible(False)
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()

place.pyplot(fig, clear_figure=True)
plt.close(fig)
