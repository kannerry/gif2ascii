import os
from PIL import Image, ImageSequence, ImageDraw, ImageOps
import imageio

# Define the ASCII characters to use for each grayscale value
ascii_chars = [" ", ".", ",", ":", ";", "+", "!", "/", "K", "N", "R", "?"]

scale_temp = input("enter an input scale. e.g: '6'\nyour input determines how many pixels one character should take up.\n")

char_width, char_height = int(scale_temp) * 2, int(scale_temp) * 3  # The width and height of each ASCII character

def png_to_ascii(png_file):
    img = Image.open(png_file).convert('RGBA')
    width, height = img.size
    # Scale the image down so that each pixel corresponds to an ASCII character
    if "yes" in invert_input:
        img = img.convert("RGB")
        img = ImageOps.invert(img)
    img = img.resize((width // char_width, height // char_height))
    # Convert each pixel to an ASCII character based on its grayscale value
    ascii_str = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, *a = img.getpixel((x, y))
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

def txt_to_gif(gif_dir):
	gifdir = str(gif_dir.split(".gif")[0]) + "_frames/"
	tarray = []
	images = []
	for file in os.listdir(gifdir):
		if file.endswith(".txt"):
			tarray.append(file)
	tarray.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
	for frame in tarray:
		with open(gifdir + frame, "r") as f:
			frame_content = f.read()
			frame_gen = text_to_image(frame_content)
			frame_gen.save(gifdir + frame.replace("txt", "png"))
		images.append(imageio.imread(gifdir + frame.replace("txt", "png")))
	imgname = os.path.splitext(gif_dir)[0].split("\\")[-1] # ?
	imageio.mimsave(imgname + "_ascii.gif", images, format='GIF', duration=int(fps) / 1000)

def text_to_image(_string):
	img = Image.new('RGB', (1, 1))
	_d = ImageDraw.Draw(img)
	text_width, text_height = _d.textsize(_string)
	real_img = Image.new('RGB', (text_width, text_height))	
	d = ImageDraw.Draw(real_img)
	d.text((0, 0), _string, fill=(0, 255, 0))
	os.system('cls')
	print("processing...")
	return real_img
	
fps = input("how fast should each frame go by? (length of each frame in ms)\n")
invert_input = input("should we invert the image? (if your gif comes out wrong, try 'yes')\n")
gif_real = input("now enter a gif directory! :D\n")
gif_to_png(gif_real)
txt_to_gif(gif_real)

