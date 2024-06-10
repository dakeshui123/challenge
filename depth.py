import numpy as np  
from PIL import Image  
import os  
  
def read_sparse_depth_rgb(filename):
    # 打开RGB图像文件
    img_file = Image.open(filename)
    # 读取RGB数据为numpy数组
    rgb_data = np.array(img_file, dtype=np.uint8)
    
    # 确保图像是三个通道
    assert rgb_data.ndim == 3 and rgb_data.shape[2] == 3, "Image must have 3 channels (R, G, B)"
    
    # 初始化深度图数组，数据类型为无符号整数，与RGB通道位数相同（通常为8位）
    # 但由于我们是拼接三个通道，所以实际上深度值的位数会更高
    depth_map = np.empty(rgb_data.shape[:2], dtype=np.uint32)
    
    # 遍历每个像素，将RGB值组合成一个无符号整数
    for y in range(rgb_data.shape[0]):
        for x in range(rgb_data.shape[1]):
            r, g, b = rgb_data[y, x]
            # 将R, G, B通道的值组合成一个无符号整数
            # 这里假设R是最高有效位，B是最低有效位
            depth = (r << 16) | (g << 8) | b
            depth_map[y, x] = depth
    
    # 如果需要，可以根据实际情况调整深度值的范围或精度
    # ...
    
    # 如果需要，可以将深度值缩放到[0, 1]范围，但这取决于你的具体应用
    # depth_map = depth_map.astype(np.float32) / (2**24 - 1)
    
    return depth_map
  
def save_depth_to_txt(depth_map, output_folder, filename_without_extension):  
    output_file = os.path.join(output_folder, f"{filename_without_extension}.txt")  
    # 由于depth_map是无符号整数，我们可能需要先将其转换为浮点数以保存小数格式（如果需要的话）  
    # 但这里我们直接保存无符号整数  
    np.savetxt(output_file, depth_map.reshape(-1, 1), delimiter=',', fmt='%u')  # %u表示无符号整数  
  
# 设置输入和输出文件夹  
input_folder = 'data/bc_pointclod/raw_data/'  
output_folder = 'data/bc_pointclod/depth_txt/'  
if not os.path.exists(output_folder):  
    os.makedirs(output_folder)  
  
# 遍历文件名从00001.png到10000.png  
for i in range(1, 10001):  
    filename = f"{i:06d}.png"  # 使用格式化字符串确保文件名是五位数，不足部分用0填充  
    input_file = os.path.join(input_folder, filename)  
      
    if os.path.exists(input_file):  
        sparse_depth = read_sparse_depth_rgb(input_file)  
        # 提取文件名（不带扩展名）用于输出文件名  
        filename_without_extension = os.path.splitext(filename)[0]  
        save_depth_to_txt(sparse_depth, output_folder, filename_without_extension)  
    else:  
        print(f"File {input_file} does not exist.")
