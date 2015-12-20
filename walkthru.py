"""

This is just a giant file full of commands we'll type into a python shell.
You probably don't want to import this or run this directly.

"""
from PIL import Image

# Load an image & display it.
im = Image.open('img/cake.jpg')
im.show()

# Images have some intersting attrubutes
print(im.format)
print(im.size)
print(im.mode)

# Simple transforms
# -----------------

# - thumbmails
size = (100, 100)  # width, height
im.thumbnail(size)
im.save("thumb.jpg", "JPEG")
im.show()

# - resizing
result = im.resize((1024, 100))

# - simple rotations
result = im.rotate(45)
result = im.rotate(90)
result = im.rotate(-120)

# - cropping
im = Image.open('img/cake.jpg')  # reload the original
box = (512, 0, 1024, 768)  # (left, upper, right, lower), with (0, 0) top-left
result = im.crop(box)

# - rotate the cropped image and past it back in the original
result = result.transpose(Image.ROTATE_180)
im.paste(result, box)

# - Flip the cropped image and paste it back in
result = result.transpose(Image.FLIP_LEFT_RIGHT)
im.paste(result, box)


# Colors!
# -------

# - channels
r, g, b = im.split()
Image.merge("RGB", (b, g, r)).show()
Image.merge("RGB", (g, r, b)).show()

# - L-mode: single-band, black & white
im = Image.open('img/cake.jpg').convert("L")
im.getbands()  # ('L', )

# - point operations modify individual pixels!
r = r.point(lambda i: i * 2)  # double red values
g = g.point(lambda i: int(i/2))  # half green values
b = b.point(lambda i: int(i/2))  # half blue values
Image.merge("RGB", (r, g, b)).show()

# - inspect pixel values
r.histogram()  # list of values in the range 0 - 255 (black - white)

# ipython magic commands to let us plot things.
# %matplotlib
# %pylab
# >>> plot(r.histogram())

# - apply a mask
im = Image.open('img/cake.jpg')
r, g, b = im.split()

mask = b.point(lambda i: i < 100 and 255)  # where BLUE is less than 100
b = b.point(lambda i: i * 2)  # double blue pixel values
b.paste(b, mask=mask)  # apply mask to the blue band
im = Image.merge(im.mode, (r, g, b))  # merge them all


def thresh(pixel_value):
    """Threshold a image."""
    if pixel_value < 200:
        return 0
    return 255

Image.eval(im, thresh).show()
im = im.point(thresh)  # Can also do this with the point method.


# ENHANCE!
from PIL import ImageEnhance

# 50% more contrast
en = ImageEnhance.Contrast(im)
en.enhance(1.5).show()  # 50% more contrast

# 5x sharper
en = ImageEnhance.Sharpness(im)
en.enhance(5).show()

# Light Smoothing...
en = ImageEnhance.Sharpness(im)
en.enhance(0.1).show()

# Brightness
en = ImageEnhance.Brightness(im)
en.enhance(1.5).show()  # 50% brighter
en.enhance(0.5).show()  # 50% darker

# Filters
# -------

from PIL import ImageFilter

im = Image.open('img/cake.jpg')
im.filter(ImageFilter.BLUR).show()
im.filter(ImageFilter.CONTOUR).show()
im.filter(ImageFilter.FIND_EDGES).show()
im.filter(ImageFilter.SHARPEN).show()
im.filter(ImageFilter.SMOOTH).show()


# Use filters to minimize some colors, maximize the rest.
im = Image.open('img/cake.jpg')
r, g, b = im.split()

# run a MaxFilter over the red channel
r = r.filter(ImageFilter.MaxFilter(size=3))

# run MinFilters over the blue & green channels
g = g.filter(ImageFilter.MinFilter(size=3))
b = b.filter(ImageFilter.MinFilter(size=3))

# merge the results
Image.merge("RGB", (r, g, b)).show()


# Custom convolution Kernels
# See: https://en.wikipedia.org/wiki/Kernel_(image_processing)
size = (3, 3)
kernel = [
    0,  1, 0,
    1, -4, 1,
    0,  1, 0
]
k = ImageFilter.Kernel((3, 3), kernel=kernel)
im.filter(k).show()

# NOTE: You can look at the built-in filters' arguments.
ImageFilter.EMBOSS.filterargs
# ((3, 3), 1,     128,    (-1, 0, 0, 0, 1, 0, 0, 0, 0))
#  size,   scale, offset, kernel


# Channel Operations
# ------------------
from PIL import ImageChops

im1 = Image.open('img/cake.jpg')
im2 = Image.open('img/coffee.jpg')
texture = Image.open('img/texture.jpg')

# Blending and merging images.
alpha = 0.5
ImageChops.blend(im1, im2, alpha).show()  # merge equally (0.5)
# or
Image.blend(im1, im2, alpha).show()

ImageChops.darker(im1, im2, 0.5).show()  # mix, keeping darker pixels.
ImageChops.difference(im1, im2).show()  # subtract im2 pixel values from im1
ImageChops.invert(im1).show()  # Invert an image
ImageChops.screen(im1, texture).show()
ImageChops.subtract(im1, texture).show()

# offset is fun.
ImageChops.offset(im2, 512, 0).show()


# load images from a directory, modify them, and write back to the same place
def process(num):
    """Do edge detection on each frame"""
    input_file = "img/frames/me{0:03d}.png"
    output_file = "img/frames/me_processed{0:03d}.png"
    for i in range(1, num + 1):
        filename = input_file.format(i)
        im = Image.open(filename)

        # Edges
        im = im.convert("L")
        im = im.filter(ImageFilter.FIND_EDGES)

        output = output_file.format(i)
        im.save(output)


def process_ghost(num):
    """Blend each frame with a previous one."""
    input_file = "img/frames/me{0:03d}.png"
    output_file = "img/frames/me_processed{0:03d}.png"
    for i in range(1, num + 1):
        filename = input_file.format(i)
        im = Image.open(filename)

        im = im.convert("L")
        if i > 1 and i <= num + 1:
            prev = Image.open(input_file.format(i - 1)).convert("L")
            im = ImageChops.blend(im, prev, 0.5)

        output = output_file.format(i)
        im.save(output)


def process_thresh(num):
    """threshold each frame."""
    input_file = "img/frames/me{0:03d}.png"
    output_file = "img/frames/me_processed{0:03d}.png"
    for i in range(1, num + 1):
        filename = input_file.format(i)
        im = Image.open(filename)
        im = im.point(thresh)

        output = output_file.format(i)
        im.save(output)


# low-level pixel data
data = list(im.getdata())  # list of (R, G, B) values, e.g. [(225, 225, 225), ... ]

# random red noise (this is slow!)
from random import randint
noise = []
for r, g, b in data:
    r = randint(0, 255)
    noise.append((r, g, b))
im = im.putdata(noise)


# Thresholding different color values
im = Image.open('img/cake.jpg')
data = im.getdata()
new_data = []
for r, g, b in data:
    if r > 200:
        r = 255
    elif r > 100:
        r = 200
    g = 200 if g > 200 else g
    b = 100 if b > 200 else b
    new_data.append((r, g, b))
im.putdata(new_data).show()
