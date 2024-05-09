from PIL import Image, ImageDraw
import os

frames = []
for fname in os.listdir("pngs/"):
    imgfile = os.path.join("pngs", fname)
    print(imgfile)
    new_frame = Image.open(imgfile)
    frames.append(new_frame)

frames[0].save(
    'pngs-to-gif.gif',
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=300,
    loop=0
    )
