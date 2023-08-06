color_set = r"""red-->红色-->Красный
blue-->蓝色-->Голубой
green-->绿色-->Зеленый
pink-->粉红色-->розовый
cyan-->青色-->Cyan
brown-->棕色-->Коричневый
black-->黑色-->Черный
purple-->紫色-->Фиолетовый
yellow-->黄色-->Желтый"""

# 写法一
def color_set_replace(search_color):
    ret = ''
    l1 = color_set.split('\n')
    for l2 in l1:
        l3 = l2.split("-->")
        if search_color.lower()==l3[0]:
            ret=l3[2]
    return ret

if __name__ == '__main__':
    ret = color_set_replace(search_color="red")
    print(ret)