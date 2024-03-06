import cv2
import random
import numpy as np
import pandas as pd

from translate import translate, get_sentenses
from word_card_generation import generate_card

new_word_list = []
file_path = '/Users/licong/Nutstore_Files/IoT/toefl/new_words.xlsx'
df = pd.read_excel(file_path)

new_word_list = df['Word'].to_list()
count_array    = np.array(df['Count'].to_list())

min_indices = np.where(count_array==np.min(count_array))[0]
current_word_index = np.random.choice(min_indices)  # 生成0到n之间的随机整数
while True:
    # current_word_index = random.randint(0, len(new_word_list)-1)  # 生成0到n之间的随机整数
    new_word = new_word_list[current_word_index]
    us_phonetic, uk_phonetic, explains = translate(new_word)
    all_div = get_sentenses(new_word)
    
    bk_img = generate_card(new_word, us_phonetic, uk_phonetic, explains, all_div)

    cv2.imshow('#' + str(current_word_index), bk_img)
    
    key = cv2.waitKey(0)    # 等待按键输入
    if key == 27:           # ESC键退出循环
        break
    elif key == 13:  # 回车，表示会
        count_array[current_word_index] += 1 
        min_indices = np.where(count_array==np.min(count_array))[0]
        current_word_index = np.random.choice(min_indices)  # 生成0到n之间的随机整数
    elif key == 9:  # shift，表示不会
        min_indices = np.where(count_array==np.min(count_array))[0]
        current_word_index = np.random.choice(min_indices)  # 生成0到n之间的随机整数
    cv2.destroyAllWindows()

df['Count'] = count_array.tolist()
df.to_excel(file_path, index=False)