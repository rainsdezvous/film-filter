from PIL import Image as img, ImageFilter as imgf
import math
import numpy as np  # type: ignore

def apply_film_filter(image):


    w = image.width
    h = image.height
    pixel_map_1 = image.load()

    #add warmth
    for x in range(w):
        for y in range(h):

            pixel = pixel_map_1[x, y]

            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            
            r = min(r + 30, 255)
            g = min(g + 5, 255)    
            b = max(b - 30, 0)
            
            pixel_map_1[x, y] = (r, g, b)

    #add green undertone
    for x in range(w):
        for y in range(h):
            
            pixel = pixel_map_1[x, y]

            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
        
            brightness = (r + g + b) / 3

            if brightness < 50:
                r = max(r - 5, 0)
                g = min(g + 10, 255)    
                b = max(b - 5, 0)
                pixel_map_1[x, y] = (r, g, b) 
            else:
                pixel_map_1[x, y] = (r, g, b)
        

    blurred_img = image.copy()
    pixel_map_2 = blurred_img.load()

    #add blur
    for x in range(w):
        for y in range(h):

            pixel = pixel_map_2[x, y]

            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            
            brightness = (r + g + b)/3
            
            if brightness > 200:
                r = min(r + 40, 255)
                g = min(g + 40, 255)
                b = min(b + 40, 255)
            else:
                r = r
                g = g
                b = b
                
            pixel_map_2[x, y] = (r, g, b)

    blurred_img = blurred_img.filter(imgf.GaussianBlur(6))

    dreamy_img = img.blend(image, blurred_img, 0.4)
    dreamy_img = dreamy_img.convert("RGBA")

    #add vignette
    alpha = 0
    overlay = img.new("RGBA", (w, h), (0, 0, 0, alpha))
    pixel_map_3 = overlay.load()

    cx = w/2
    cy = h/2
    inv_cx = 1 / cx
    inv_cy = 1 / cy

    for x in range(w):
        for y in range(h):
            dx = (x - cx) * inv_cx
            dy = (y - cy) * inv_cy
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 0.9:
                alpha = 0
            else:
                falloff = 1.2
                strength = 220
                alpha = int(min(255, ((distance - 0.9) ** falloff) * strength))
                pixel_map_3[x, y] = (0, 0, 0, alpha)

    vignette_img = img.alpha_composite(dreamy_img, overlay)


    #add grain
    grain_array = np.random.normal(127, 20, (h, w))
    grain_clamped = np.clip(grain_array, 0, 255)
    grain_uint8 = grain_clamped.astype(np.uint8)
    grain_rgb = np.stack([grain_uint8] * 3, axis=2)  # shape: (h, w, 3)
    grain_img = img.fromarray(grain_rgb, mode="RGB")

    grain_img = grain_img.convert(vignette_img.mode)


    final_img = img.blend(vignette_img, grain_img, 0.1)

    return final_img