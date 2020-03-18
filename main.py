# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import Flask, render_template, request, url_for, redirect, Response, send_file, redirect, session
import requests
from fpdf import FPDF, HTMLMixin
import os
import qrcode
import io
from PIL import Image, ImageDraw
from google.cloud import storage
import json
app = Flask(__name__)


def random_qr(stt, start, end, filename):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=5,
                       border=4)

    qr.add_data(stt)
    qr.make(fit=True)
    img = qr.make_image()

    # Add logo here
    img = img.convert("RGBA")

    icon = Image.open('logo.png')
    img_w, img_h = img.size
    factor = 4
    size_w = 40  # int(100)
    size_h = 40  # int(80)

    # logo图片的大小不能超过二维码图片的1/4
    #  icon_w,icon_h=icon.size
    #  if icon_w>size_w:
    #     icon_w=size_w
    #  if icon_h>size_h:
    #     icon_h=size_h
    #  icon=icon.resize((icon_w,icon_h),Image.ANTIALIAS)

    #  w=int((img_w-icon_w)/2)+4
    #  h=int((img_h-icon_h)/2)
    #  icon=icon.convert("RGBA")
    #  img.paste(icon,(w,h),icon)

    d = ImageDraw.Draw(img)
    d.text((50,128), start+"/"+end, fill=(0,0,0))

    img.save("./static/images/"+filename+".png")

# @app.route("asdf.jpg")
# def asdf():


@app.route("/shipment/create_stt")
def createSTTPDF():

    stt_data = request.args.get('stt')
    # +"##asd33d@@dkfhi3##hhhff##jasdfasdf##asdfasdf##"#request.args.get('stt')
    token = stt_data
    stt = token.split("##")[0]
    total = int(request.args.get('total'))

    pdf = FPDF('P', 'mm', (40, 40))
    x_coor = 0.0

    # end = f'{total:03}'
    # start = f'{1+1:03}'
    # filename = stt+"_"+str(start)+"_"+str(end)
    # image_buf =  io.BytesIO()
    # image = random_qr(token,str(start),str(end), filename)
    # image.save(image_buf, "png")
    # image_buf.seek(0)

    # asdf = Image.open(image_buf.)
   # asdf = image.save("./static/images/"+filename+".png")
    # return str(image_buf.read())
    # return send_file(image.show(), mimetype='image/gif')

    for x in range(0, total):
        pdf.add_page()
        pdf.set_margins(-2, -2, -2)
        x_coor = x * 40.0
        end = total#f'{total:03}'
        start = x+1#f'{x+1:03}'
        filename = stt+"_"+str(start)+"_"+str(end)
        image_buf = io.BytesIO()
        image = random_qr(token, str(start), str(end), filename)
        
        pdf.image('static/images/'+filename+'.png', -3.0, -
                  3.5, link='', type='', w=46.0, h=42.0)
        os.remove('static/images/'+filename+'.png')

    return Response(pdf.output(
        dest='S').encode('latin-1'),
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment;filename='+stt_data+'.pdf'}
    )



@app.route('/', methods=['GET'])
def say_hello():
    return "Hello, world!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
