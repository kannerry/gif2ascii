import os
from PIL import Image, ImageSequence

# Define the ASCII characters to use for each grayscale value
ascii_chars = [" ", ".", ",", ":", ";", "+", "*", "?", "S", "W", "A", "G"]

scale_temp = input("enter an input scale. e.g: '6'\nyour input determines how many pixels one character should take up.\n")

char_width, char_height = int(scale_temp) * 2, int(scale_temp) * 3  # The width and height of each ASCII character

def png_to_ascii(png_file):
    img = Image.open(png_file).convert('RGBA')
    width, height = img.size
    # Scale the image down so that each pixel corresponds to an ASCII character
    img = img.resize((width // char_width, height // char_height))
    # Convert each pixel to an ASCII character based on its grayscale value
    ascii_str = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = img.getpixel((x, y))
            if a == 0:
                ascii_str += " "
            else:
                gray_value = round(0.2989 * r + 0.5870 * g + 0.1140 * b)
                ascii_str += ascii_chars[gray_value * len(ascii_chars) // 256]
        ascii_str += "\n"
    # Save the ASCII output to a text file
    with open(f"{png_file.split('.')[0]}.txt", "w") as f:
        f.write(ascii_str)
    return ascii_str

def gif_to_png(gif_file):
    gif = Image.open(gif_file)
    frames_dir = f"{os.path.splitext(gif_file)[0]}_frames"
    os.makedirs(frames_dir, exist_ok=True)
    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        png_filename = f"{frames_dir}/{i + 1}.png"
        frame.save(png_filename, "PNG")
        ascii = png_to_ascii(png_filename)
        print(ascii)

gif_real = input("now enter a gif directory! :D\n")
gif_to_png(gif_real)

