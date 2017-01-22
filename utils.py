import csv
# -*- coding: utf-8 -*-
def quesLoader(fileName):
    quesList = []
    with open(fileName) as f:
        reader = csv.reader(f)
        #next(reader)
        for item in reader:
            quesList.append({'description': item[0], 'labels': item[1]})
    return quesList
import json
def labelSaver(srcFileName,DstFileName):
    with open(srcFileName) as srcf:
        with open(DstFileName,"w") as dstf:
            reader = csv.reader(srcf)
            writer = csv.writer(dstf)
            for item in reader:
                writer.writerow([item[0],json.dumps({"img":item[1],"choices":item[2:]})])
def generate(Num):
    from PIL import Image,ImageDraw,ImageFont
    img = Image.new('RGB', (200, 100), (255, 255, 254))
    fontSize     = 65
    myFont       = ImageFont.truetype("/Library/Fonts/OsakaMono.ttf", fontSize)
    d = ImageDraw.Draw(img)
    print str(Num)
    d.text((30, 20), str(Num), fill=(255, 0, 0),font=myFont)
    img.save("plat/static/data/"+str(Num)+".jpg")
#generate(0)