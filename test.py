import re

pattern = r'蛇的學名[:：](.+)'  # 修改這裡


user_input = input("請輸入蛇的學名: ")

match = re.search(pattern, user_input)

if match:
    snake_scientific_name = match.group(1)
    print(f"蛇的學名是: {snake_scientific_name}")
else:
    print("無法找到蛇的學名")