from zhujie import zhujie
from json_table import json_table
from json_rich import json_rich

xlsx=r"C:\Users\Administrator\Desktop\001.xlsx"
load_excel = r"C:\Users\Administrator\Desktop\工作记录\ozon\excel上传研究\原始-运动泳衣分开v7.xlsx"

# 8357d_Blue_S
sku = '8357d'
color_list = "blue,black,pink,red,yellow".split(",")
size_list = "XS,S,M,L,XL,2XL,3XL,4XL,5XL,6XL".split(",")
sku_l = [(sku+"_"+color_list[i]+"_"+size_list[j]) for i in range(len(color_list)) for j in range(len(size_list))]
title = "Женская летняя повседневная мода 3D-печатный купальник для бассейна и пляжа из двух частей"
price = "14.96"  # 美元
price_pre = "24.93"  # 美元
tax = "不征税"
type1 = "运动泳衣分开"  # 商用型
package_weight = "320"  # 包裹重量 g
package_width = "100"  # 宽度
package_height = "50"  # 高度
package_length = "100"  # 长度
main_photo = "https://cdn1.ozone.ru/s3/multimedia-m/6582655786.jpg"
other_photo = "https://cdn1.ozone.ru/s3/multimedia-o/6582655788.jpg"
brand = "无品牌"
card = sku  # 卡片
product_color1 = "黑"  # 商品颜色  这个颜色不起作用
size1 = "1111" # 俄罗斯尺码
size2 = "S[42-44](87-92cm)" # 制造商尺码
product_color2 = ""  # 颜色名称
type2 = "独立泳衣 "  # 泳衣类型
gender = "女性"  # 性别
key_words = ""  # 关键字
TargetAudience ="成人"  # 目标受众
season = "适合任何季节"  # 季节
model_height = "170 厘米"  # 模特身高
model_measurements = "ОГ - 84, ОТ - 61, ОБ - 92"  # 模特三围
cloth_size = "52"  # 展示图 服装尺寸
collect = "2023春夏"  # 收集
country_of_manufacture = "中国"  # 制造国
print_type = "花卉"  # 印花种类
comments = zhujie  # 注解
care_instructions = "Стирка при температуре не выше 39 градусов, ручная стирка.Не сушите купальный костюм в сушилке, он может деформироваться."  # 保养说明
material = "涤纶"  # 材料
material_ingredient = "Нейлон 20% полиэстер 80%"  # 材料成分
gasket_inner_material = "聚酯纤维"  # 垫片/内部材料
filler = "聚酯纤维"  # 填充材料
temperature_range = "18°С -37°С"# 温度范围， °С
style = "海滩"  # 风格
type_of_exercise = "游泳"  # 运动种类
clothing_type = "高腰"  # 服装类型
button_type = "其它"  # 扣子类型
waist = "标准"  # 腰
clothing_package_type = "包"  # 服装包装类型
JSON_size_table =json_table  # JSON 大小表
JSON_rich_content = json_rich  # JSON 丰富内容
breast_support_level = "平均"  # 乳房支撑水平