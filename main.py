import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

"""
Studentiem jāveic kontrasta korekcija trīs dažādiem krāsainiem attēliem:

    Pārtumšots attēls (maz izteiktas gaismas) - dark.jpg

    Pārgaismots attēls (maz izteiktas ēnas) - overexposed.jpg

    Pelēcīgs attēls (zems kontrasts, maz izteiktas ēnas un gaismas) - low_contrast.jpg

Jāapstrādā ar:

1) Gamma
    
2) Histogrammas lineārā pārveidošana
"""

def load_image(path):
    img = Image.open(path).convert("RGBA")
    arr = np.asarray(img).astype(np.float32) / 255.0
    return arr[...,:3]  # Drop alpha, keep RGB [H,W,3]

def save_image(arr, path):
    clamped = np.clip(arr, 0.0, 1.0)
    img = Image.fromarray((clamped * 255.0 + 0.5).astype(np.uint8))
    img.save(path)


def gamma_correction(image, gamma=2.2):
    """
    Gamma correction: C = p ** (1/gamma) for brightening dark images (gamma<1),
    or p ** gamma for darkening bright (gamma>1).
    Uses per-pixel loop as requested.
    Typical gamma=0.4-0.6 for dark, 1.5-2.5 for bright images.
    """
    C = np.empty_like(image)
    inv_gamma = 1.0 / gamma
    for row in range(image.shape[0]):
        for column in range(image.shape[1]):
            for color in range(3):
                p = image[row, column, color]
                C[row, column, color] = np.power(p, inv_gamma)
    return np.clip(C, 0.0, 1.0) [web:6][web:12]

def histogram_linear_transformation(image):
    """
    Linear contrast stretch: find global min/max, k=1/(max-min), C = k*(p - min)
    Stretches histogram to full [0,1] range.
    Uses per-pixel loop.
    """
    g_min = np.min(image)
    g_max = np.max(image)
    if g_max <= g_min:
        return image.copy()
    k = 1.0 / (g_max - g_min)
    C = np.empty_like(image)
    for row in range(image.shape[0]):
        for column in range(image.shape[1]):
            for color in range(3):
                p = image[row, column, color]
                C[row, column, color] = k * (p - g_min)
    return np.clip(C, 0.0, 1.0) [web:7][web:11][web:13]

def show_comparison(original, processed1, processed2, title):
    """Display original | gamma | linear side-by-side using matplotlib."""
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(title)
    
    axs[0].imshow(original)
    axs[0].set_title('Original')
    axs[0].axis('off')
    
    axs[1].imshow(processed1)
    axs[1].set_title('Gamma Correction')
    axs[1].axis('off')
    
    axs[2].imshow(processed2)
    axs[2].set_title('Histogram Linear')
    axs[2].axis('off')
    
    plt.tight_layout()
    plt.show()

def main(image_paths):
    """Process three images: dark, overexposed, low_contrast."""
    image_names = ['dark', 'overexposed', 'low_contrast']
    
    for i, path in enumerate(image_paths):
        if not os.path.exists(path):
            print(f"Warning: {path} not found, skipping.")
            continue
        
        orig = load_image(path)
        name = image_names[i]
        
       
        gamma_img = gamma_correction(orig, gamma=0.5 if 'dark' in name else 2.2 if 'over' in name else 1.0)
        linear_img = histogram_linear_transformation(orig)
        
        save_image(gamma_img, f"{name}_gamma.png")
        save_image(linear_img, f"{name}_linear.png")
        
       
        show_comparison(orig, gamma_img, linear_img, f'Processing: {name}')
        
        print(f"Processed {name}: saved _gamma.png and _linear.png, displayed comparison.")

if __name__ == "__main__":
   
    images = ["dark.jpg", "overexposed.jpg", "low_contrast.jpg"]
    main(images)
