import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

def generate_card(translate_text, us_phonetic, uk_phonetic, explains, all_div):
    bk_img = cv2.imread('back.jpg')
    font = ImageFont.truetype("times.ttf", 80)  # -------------------单词的字体大小
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    # 绘制文字信息
    draw.text((50, 80), translate_text, font=font, fill=(0, 0, 0))      # 单词的绘制位置和颜色
    font = ImageFont.truetype("times.ttf", 40)                          #【音标】的字体大小,音标难以渲染，发现是字体不支持导致的
    phonetic_text = ''
    if us_phonetic is not None and uk_phonetic is not None:
        phonetic_text = 'US: /' + us_phonetic + '/ UK: /' + uk_phonetic + '/'
    if us_phonetic is None and uk_phonetic is not None:
        phonetic_text = 'UK: /' + uk_phonetic + '/'
    if us_phonetic is not None and us_phonetic is None:
        phonetic_text = 'US: /' + us_phonetic + '/'
    draw.text((50, 180), phonetic_text, font=font, fill=(255,100,100))  # 【音标】的绘制位置和颜色
    font = ImageFont.truetype("msyh.ttc", 20)                           # 释义的字体大小
    if explains is not None:
        for i, explain in enumerate(explains):
            draw.text((50, 250 + 40*i), explain, font=font, fill=(70,70,70))         
        for i, div in enumerate(all_div):
            draw.text((50, 350 + 100*i), div.text, font=font, fill=(0,70,70))
    bk_img = np.array(img_pil)

    return bk_img