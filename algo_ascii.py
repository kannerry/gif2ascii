import os
import sys
from PIL import Image, ImageSequence, ImageDraw, ImageOps
import imageio
import shutil

args = sys.argv
args.pop(0)
hasDraggedGif = args != []
ascii_chars = [' ', '.', '^', ',', ':', ';', 'I', 'l', '!', 'i', '>', '<', '~', '+', '_', '-', '?', ']', '[', '}',
               '{', '1', ')', '(', '|', '/', 't', 'f', 'j', 'r', 'x', 'n', 'u', 'v', 'c', 'z', 'X', 'Y', 'U', 'J', 'C', 'L', 'Q', '0', 'O', 'Z', 'm', 'w', 'q', 'p', 'd', 'b', 'k', 'h', 'a', 'o', '*', '#', 'M', 'W', '&', '8', '%', 'B', '@', '$']

def png_to_ascii(png_file):
    img = Image.open(png_file).convert('RGBA')
    width, height = img.size
    if "y" in invert_input:
        img = img.convert("RGB")
        img = ImageOps.invert(img)
    img = img.resize((width // int(char_width), height // int(char_height)))
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
        png_to_ascii(png_filename)


def txt_to_gif(gif_dir):
    gifdir = str(gif_dir.split(".")[0]) + "_frames/"
    format = str(gif_dir.split(".")[1])
    tarray = []
    images = []
    for file in os.listdir(gifdir):
        if file.endswith(".txt"):
            tarray.append(file)
    tarray.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    imgname = os.path.splitext(gif_dir)[0].split("\\")[-1]  # ?
    for frame in tarray:
        with open(gifdir + frame, "r") as f:
            frame_content = f.read()
            frame_gen = text_to_image(frame_content)
            frame_gen.save(gifdir + frame.replace("txt", "png"))
        images.append(imageio.imread(gifdir + frame.replace("txt", "png")))
    if format == "gif":
        try:
            dur = int(fps)
        except:
            dur = 60
        imageio.mimsave(imgname + "_ascii." + str(format), images,
                        format=format, duration=dur / 1000)


def text_to_image(_string):
    img = Image.new('RGB', (1, 1))
    _d = ImageDraw.Draw(img)
    text_width, text_height = _d.textsize(_string)
    real_img = Image.new('RGB', (text_width, text_height))
    d = ImageDraw.Draw(real_img)
    d.text((0, 0), _string, fill=(0, 255, 0), spacing=-2.0)
    real_img = real_img.crop((0,0,real_img.width,real_img.height * 0.6))
    os.system('cls')
    print("processing...")
    return real_img


def prompt_default():
    gif_real = input("enter an image/gif directory\n") or None
    if gif_real == None:
        prompt_default()
    else:
        gif_to_png(gif_real)
        txt_to_gif(gif_real)

def process_dragged(array):
    for gif in array:
        gif_to_png(gif)
        txt_to_gif(gif)

fps = input(
    "how fast should each frame go by? (length of each frame in ms)\n") or "60"
invert_input = input(
    "should we invert the image? (if your gif comes out wrong, try 'yes')\n") or "n"
scale_temp = input(
    "enter an input scale. e.g: '6'\nyour input determines how many pixels one character should take up.\n") or "2"
char_width = int(scale_temp) * 2
char_height = int(scale_temp) * 3

if hasDraggedGif:
    process_dragged(args)
else:
    prompt_default()
