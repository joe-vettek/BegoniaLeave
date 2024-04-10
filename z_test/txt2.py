# 当前版本两个替换
# from ppstructure.predict_system import StructureSystem, save_structure_res, to_excel
# from ppstructure.predict_system import StructureSystem, save_structure_res, to_excel, TextSystem

# class PaddleOCR(predict_system.TextSystem):
#     class PaddleOCR(TextSystem):


from paddleocr import PaddleOCR, draw_ocr

from core import utils, file_locator, screen_locator

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True,use_gpu=True, lang="ch")  # need to run only once to download and load model into memory
# screen_locator.quick_screenshot()
@utils.test_time
def go():
    img_path = file_locator.get_cache_screenshot()
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)

    # 显示结果
    from PIL import Image
    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('result.jpg')

go()