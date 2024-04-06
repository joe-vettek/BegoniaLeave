import easyocr
from core import file_locator,utils

@utils.test_time
def pri():
    # 创建OCR对象
    reader = easyocr.Reader(['en', 'ch_sim'])
    # 识别文字
    # file_locator.get_cache_screenshot()
    result = reader.readtext(file_locator.get_cache_screenshot())
    # 处理识别结果
    for (text, bbox, confidence) in result:
        if confidence>0.9:
            print(f'Text: {text}, Bbox: {bbox}, Confidence: {confidence}')

pri()