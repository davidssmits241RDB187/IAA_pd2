import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

def load_image(path):
    img = Image.open(path).convert("RGBA")
    arr = np.asarray(img).astype(np.float32) / 255.0
    return arr[...,:3]  

def gamma_correction(image, dark_gamma=1.1, bright_gamma=0.8):
    C = np.empty_like(image)
    threshold = np.mean(image)+0.1
    if(threshold>=0.5):
        dark_gamma +=(np.max(image)-np.min(image))/5
    else:
        bright_gamma-=(np.max(image)-np.min(image))/5
    dark_mask = image <= threshold
    bright_mask = image > threshold
    C[bright_mask] = np.power(image[bright_mask], bright_gamma)
    C[dark_mask] = np.power(image[dark_mask], dark_gamma)
    return np.clip(C, 0.0, 1.0) 

def histogram_linear_transformation(image):
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
    return np.clip(C, 0.0, 1.0) 

def compare(originals, gamma_imgs, linear_imgs, name):
    _, axs = plt.subplots(3, 3, figsize=(15, 15))
    for i, (orig, gamma, linear) in enumerate(zip(originals, gamma_imgs, linear_imgs)):
        axs[i, 0].imshow(orig); axs[i, 0].set_title('Original'); axs[i, 0].axis('off')
        axs[i, 1].imshow(gamma); axs[i, 1].set_title('Gamma'); axs[i, 1].axis('off')
        axs[i, 2].imshow(linear); axs[i, 2].set_title('Histogram Linear'); axs[i, 2].axis('off')
    plt.tight_layout()
    filename = f"{name}_all_methods.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    
def show_histograms(originals, gamma_imgs, linear_imgs, name):
    n = len(originals)
    if n == 0:
        print("No valid images for histograms")
        return
    _, axs = plt.subplots(n, 3, figsize=(15, 5 * n))
    images_list = [originals, gamma_imgs, linear_imgs]
    col_titles = ["Original", "Gamma", "Linear"]
    for i in range(n):
        for j, imgs in enumerate(images_list):
            img = imgs[i]
            hist, bins = np.histogram(img.flatten(), bins=50, range=(0, 1)) 
            axs[i, j].set_ylabel("Frequency")
            axs[i, j].plot(bins[:-1], hist, color="black", linewidth=1.5)
            axs[i, j].fill_between(bins[:-1], hist, alpha=0.3, color="skyblue")
            axs[i, j].set_title(f"{col_titles[j]} (Image {i+1})")
            axs[i, j].set_xlabel("Intensity")
            axs[i, j].grid(True, alpha=0.3)
    plt.tight_layout()
    filename = f"{name}_histograms.png"
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    
def main(image_paths):
    image_names = ['dark', 'overexposed', 'low_contrast']
    originals, gamma_imgs, linear_imgs = [], [], []
    for i, path in enumerate(image_paths):
        if not os.path.exists(path): continue  
        orig = load_image(path)
        name = image_names[i]
        gamma_img = gamma_correction(orig)
        linear_img = histogram_linear_transformation(orig)
        originals.append(orig)
        gamma_imgs.append(gamma_img)
        linear_imgs.append(linear_img)
    compare(originals, gamma_imgs, linear_imgs, "comparisons")
    show_histograms(originals, gamma_imgs, linear_imgs, "comparisons")

if __name__ == "__main__":
    images = ["dark.jpeg", "light.png", "gray.jpg"]
    main(images)