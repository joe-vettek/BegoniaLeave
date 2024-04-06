import os
from core import file_locator

lang = file_locator.load_json(file_locator.get_lang())
lang_sort = {}
for d in sorted(lang):
    category = d.split(".")[0]
    sub_ca = ''.join(d.split(".")[1:])
    if lang_sort.get(category) is None:
        lang_sort[category] = {}
    lang_sort[category][sub_ca] = lang[d]

for d_m in lang_sort:
    print("# {}".format(d_m.upper()))
    for d_s in lang_sort[d_m]:
        key=f"{d_m}.{d_s}"
        print('KEY_{}'.format(key.replace(".", "_")).upper() + ' = "{}"'.format(key))
    print()
