from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageFilter
import aiohttp
from unidecode import unidecode
from io import BytesIO

class Welcomerain:
    def __init__(self,bot):
        self.bot = bot

# im is the background to use (pass in from PIL's Image.open)
# offset_x and offset_y refer to avatar img
# returns BytesIO file-like object for easy use with bot.send_file
async def welcome_member(im, font, member, offset_x=0, offset_y=-70,
                         new_width=1000, new_height=500, ava_sqdim=260,
                         text_offset_x=0, text_offset_y=140, text=None):
    im = im.copy()
    width, height = im.size

    name = unidecode(member.name)
    if text is None:
        welcome = 'Welcome {0},\n to {1.server.name}!'.format(name, member)
    else:
        welcome = text

    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2
    im = im.crop((left, top, right, bottom))

    # how to set up a gradient from the bottom:
    # fade_from = new_height/4
    # fade_to = new_height-fade_from
    #
    # fade_from = int(fade_from)
    # fade_to = int(fade_to)
    #
    # for i in range(fade_from, new_height+1):
    #     fade = int((i-fade_from)/(fade_to)*255)
    #     draw.rectangle(((0, i), (new_width, i)), fill=(0, 0, 0, fade))

    ov_left = 0
    ov_top = im.height // 2
    ov_right = im.width
    ov_bottom = im.height
    ov_box = (ov_left, ov_top, ov_right, ov_bottom)

    ov_ic = im.crop(ov_box)
    ov_ic = ov_ic.filter(ImageFilter.GaussianBlur(15))

    im.paste(ov_ic, ov_box)

    draw = ImageDraw.Draw(im, mode='RGBA')
    draw.rectangle(((ov_left, ov_top), (ov_right, ov_bottom)), fill=(0, 0, 0, 120))

    avatar_im = None
    url = member.avatar_url
    if not url:
        url = member.default_avatar_url

    async with aiohttp.ClientSession(loop=bot.loop) as aiosession:
        with aiohttp.Timeout(10):
            async with aiosession.get(url) as resp:
                avatar_im = BytesIO(await resp.read())
    resize = (ava_sqdim, ava_sqdim)
    avatar_im = Image.open(avatar_im).convert("RGBA")
    avatar_im = avatar_im.resize(resize, Image.ANTIALIAS)

    mask = Image.new('L', resize, 0)
    maskDraw = ImageDraw.Draw(mask)
    maskDraw.ellipse((0, 0) + resize, fill=255)
    mask = mask.resize(avatar_im.size, Image.ANTIALIAS)
    avatar_im.putalpha(mask)

    img_center_x = (im.width // 2)
    img_center_y = (im.height // 2)

    img_offset_x = img_center_x + offset_x
    img_offset_y = img_center_y + offset_y
    ava_right = img_offset_x + avatar_im.width//2
    ava_bottom = img_offset_y + avatar_im.height//2
    ava_left = img_offset_x - avatar_im.width//2
    ava_top = img_offset_y - avatar_im.height//2

    im.paste(avatar_im, box=(ava_left, ava_top, ava_right, ava_bottom), mask=avatar_im)

    text_width, text_height = draw.textsize(welcome, font=font)
    draw.text((((img_center_x - text_width / 2) + text_offset_x),
               ((img_center_y - text_height / 2) + text_offset_y)),
              welcome, fill='white', font=font, align='center')

    temp = BytesIO()
    im.save(temp, format='jpeg')
    temp.seek(0)

    return temp

font = ImageFont.truetype('BLKCHCRY.ttf', 50)

        rand_img = random.choice(files)
        im = Image.open(rand_img)

    else:
        return

    kwarg_dict = dict()
    if offset_x is not None:
        kwarg_dict['offset_x'] = offset_x
    if offset_y is not None:
        kwarg_dict['offset_y'] = offset_y
    if text_offset_x is not None:
        kwarg_dict['text_offset_x'] = text_offset_x
    if text_offset_y is not None:
        kwarg_dict['text_offset_y'] = text_offset_y
    if new_height is not None:
        kwarg_dict['new_height'] = new_height
    if new_width is not None:
        kwarg_dict['new_width'] = new_width
    if ava_sqdim is not None:
        kwarg_dict['ava_sqdim'] = ava_sqdim

    im = await welcome_member(im, font, member, **kwarg_dict)
    if send_to is None:
        send_to = member.server.default_channel
    content = 'Welcome {0.mention} to {0.server.name}!'.format(member)
    await bot.send_file(send_to, im, content=content, filename='welcome.jpg')


def setup(bot):
    bot.add_cog(Welcomerain(bot))