from flask import Flask as NewFlask
from flask import render_template as render
from flask import request as req
from PIL import Image as NewImage
from PIL import ImageColor as NewImageColor
from os import environ as env

app = NewFlask(__name__, template_folder='src')


def custom_redirect(url):
    return f'<script language="JavaScript" type="text/javascript">location.href="{url}";</script>'


@app.route('/')
def index():
    return render('index.html')


def render_result(result):
    return render('level_data.html', result=result)


@app.route('/get_level_data', methods=['GET', 'POST'])
def get_level_data():
    if req.method == 'GET':
        return custom_redirect('/')
    result = 'None'

    shape_size = req.form.get('shape_size').strip().replace(' ', '').split('x')
    shape_size_x, shape_size_y = 0, 0
    try:
        shape_size_x, shape_size_y = int(shape_size[0]), int(shape_size[1])
    except:
        return render_result('Error shape size')

    downgrade = req.form.get('shape_size').strip().replace(' ', '').split('x')
    downgrade_x, downgrade_y = 0, 0
    try:
        downgrade_x, downgrade_y = int(downgrade[0]), int(downgrade[1])
    except:
        return render_result('Error downgrage')

    chromakey_text = req.form.get('chromakey').strip().replace(' ', '').replace(';', '')
    chromakey_text = chromakey_text.replace('(', '').replace(')', '')
    chromakey_type = None
    chromakey = None
    if chromakey_text[0] == '#':
        chromakey_type = 'hex'
        chromakey = chromakey_text[1:]
    elif chromakey_text[:3] == 'rgb':
        chromakey_type = 'rgb'
        chromakey = chromakey_text[3:].split(',')
    elif chromakey_text[:5] == 'rgb10':
        chromakey_type = 'rgb10'
        chromakey = chromakey_text[5:]
    print(chromakey)
    print(chromakey_type)
    if 'sam_file' not in req.files:
        return render_result('File Not Selected!')

    if downgrade_x < 1 or downgrade_y < 1:
        render_result('Minimal downgrade - 1!')

    image = NewImage.open(req.files['sam_file'])
    width, height = image.size

    result = '''<levelXML>
<info v="1.87" x="121.35000038146973" y="67.7249984741211" c="11" f="t" h="f" bg="0" bgc="16777215" e="1"/>
<groups>
    <g x="165" y="61" r="0" ox="-165" oy="-61" s="f" f="f" o="100" im="f" fr="f">
    '''

    i = 0
    while i < width:
        j = 0
        while j < height:
            r, g, b = tuple(image.getpixel((i, j))[:3])
            rgb10 = (r * 65536) + (g * 256) + b
            can_pass_c = True
            if chromakey_type:
                if chromakey_type == 'hex':
                    to_rgb = NewImageColor.getcolor(f'#{chromakey}', "RGB")
                    if r == to_rgb[0] and g == to_rgb[1] and b == to_rgb[2]:
                        can_pass_c = False
                elif chromakey_type == 'rgb':
                    if r == int(chromakey[0]) and g == int(chromakey[1]) and b == int(chromakey[2]):
                        can_pass_c = False
                elif chromakey_type == 'rgb10' and rgb10 == chromakey:
                    can_pass_c = False
            if can_pass_c:
                result += '\n'
                result += \
                    f'<sh t="0" i="f" p0="{i}" p1="{j}" p2="{shape_size_x}" p3="{shape_size_y}" p4="0" p5="f"' \
                    f' p6="f" p7="1" p8="{rgb10}" p9="-1" p10="100" p11="1"/>'
            j += downgrade_y
        i += downgrade_x

    result += '''
        </g>
    </groups>
</levelXML>'''

    return render_result(result)


@app.errorhandler(404)
def error404(e):
    return custom_redirect('/')


PORT = 5000
if 'PORT' in env:
    PORT = int(env['PORT'])

if __name__ == '__main__':
    app.run(
        '127.0.0.1',
        port=PORT,
        debug=True
    )
