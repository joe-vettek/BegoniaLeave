import os


def clean_cache():
    need=[]
    def get_in(path):
        for c in os.listdir(path):
            dc=os.path.join(path,c)
            if os.path.isdir(dc):
                if not dc.endswith("__pycache__"):
                    get_in(dc)
                else:
                    # print(dc)
                   
                    need.append(dc)



    get_in(os.getcwd())


    for n in need:
        try:
            os.remove(n)
        except:
            pass
            #print("删除失败",n)
