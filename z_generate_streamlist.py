import os

cn_asset="asset/cn"
for d in os.listdir(cn_asset):
    dir_name=os.path.join(cn_asset,d)
    print("# {}".format(d.upper()))
    for f in os.listdir(dir_name):
        print('IMAGE_{}_{}'.format(d,(f.split(".")[0])).upper()+' = "{}/{}"'.format(d,f))
    print()