import airtest
import cv2
import airtest.core.api as air_api
from PIL import Image
from airtest.core.helper import G


def init_device():
    # auto_setup(basedir=None, devices=None, logdir=None, project_root=None, compress=None)
    # auto_setup 是一个用来初始化环境的接口，
    # 5个参数可以设置当前脚本所在的路径basedir、指定运行脚本的设备devices、设置默认的log路径logdir、设置脚本父路径方便 using 接口的调用和屏幕截图的压缩比率。
    # 可设置脚本运行时的log保存路径，默认值为None则不保存log，如果设置为True则自动保存在<basedir>/log目录中。
    print(__file__)
    air_api.auto_setup(__file__, logdir=True, devices=["Android:///", ])
    # 如果当前文件包含在 sys.path 里面，那么 __file__ 返回一个相对路径
    # 如果当前文件不包含在 sys.path 里面，那么 __file__ 返回一个绝对路径（此处我的文件不包含在sys.path中）


def img_scale(image, size=612):
    # 输入你想要resize的图像高。
    height, width = image.shape[0], image.shape[1]
    # 等比例缩放尺度。
    scale = height / size
    # 获得相应等比例的图像宽度。
    width_size = int(width / scale)
    # resize
    image_resize = cv2.resize(image, (width_size, size))
    return image_resize


def resolution_log():
    # 以手机屏幕为例，iphonex像素分辨率为1125x2436，是指屏幕横向能显示1125个物理像素点，纵向能显示2436个物理像素点。
    width = G.DEVICE.display_info['width']
    height = G.DEVICE.display_info['height']
    print('device independent pixels:', width, '×', height)


def lp_screen():
    if G.DEVICE.display_info['orientation'] in [1, 3]:
        print('landscape')
        height = G.DEVICE.display_info['width']
        width = G.DEVICE.display_info['height']
    else:
        print('portrait')
        height = G.DEVICE.display_info['height']
        width = G.DEVICE.display_info['width']


def snap2show(show=True):
    img = G.DEVICE.snapshot()
    # Image.fromarray(img).save("a.png")
    # if show:
    #     img = img_scale(img)
    #     cv2.imshow("src_image1", img)
    #     cv2.waitKey(0)


if __name__ == '__main__':
    init_device()  # 初始化设备
    lp_screen()  # 查看屏幕状态：横屏landscape or 竖屏portrait
    resolution_log()  # 查看分辨率device independent pixels
    import time
    s = time.time()
    snap2show(show=False)
    e = time.time()
    print('snap time:', e - s)

    s = time.time()
    snap2show()
    e = time.time()
    print('snap time:', e - s)

    s = time.time()
    snap2show()
    e = time.time()
    print('snap time:', e - s)

