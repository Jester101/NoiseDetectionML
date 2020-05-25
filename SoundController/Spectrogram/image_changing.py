from PIL import Image


def append_image_to_size(file, width=513):
    img = Image.open(file)
    need_pixels = width - img.size[0]
    img.paste(Image.new('RGB', (need_pixels, width), (0, 0, 0)))
    img.save(file)


def crop_image(file, width=513, k=0):
    image = Image.open(file)
    image_width, image_height = image.size
    new_picture_array = []
    for i in range(0, image_width, width):
        box = (i, 0, i + width, image_height)
        try:
            picture = image.crop(box)
            picture_filename = file.replace('.png', '{0}.png'.format(k))
            new_picture_array.append(picture_filename)
            picture.save(picture_filename, format='PNG')
            if picture.size[0] < 513:
                append_image_to_size(picture_filename)
            k += 1
        except Exception as ex:
            print(ex)
            raise ex
    return new_picture_array


def create_bmp_from_rgb(png_file):
    image = Image.open(png_file)
    image = image.convert('RGB')
    pixMap = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pixMap[i, j][0] + pixMap[i, j][1] > 244:
                pixMap[i, j] = (255, 255, 255)
            else:
                pixMap[i, j] = (0, 0, 0)
    image.save(png_file.replace('.png', '.bmp'), format='BMP')


def convert_png_to_grayscale(png_file):
    image = Image.open(png_file)
    image = image.convert('LA')
    new_file_name = png_file.replace('.png', 'gray.png')
    image.save(new_file_name, format='png')
    return new_file_name


def create_bmp_from_grayscale(grayscale_file, export_dir):
    image = Image.open(grayscale_file)
    filename = grayscale_file.split('/')[-1]
    image = image.convert('RGB')
    pixMap = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pixMap[i, j][0] >= 101:
                pixMap[i, j] = (255, 255, 255)
            else:
                pixMap[i, j] = (0, 0, 0)
    image.save(export_dir + '/' + filename.replace('gray.png', '.bmp'), format='BMP')
