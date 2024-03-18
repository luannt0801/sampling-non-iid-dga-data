import pandas as pd

# Tạo DataFrame df
df = pd.DataFrame(columns=['domain', 'type', 'label'])

# Lấy số lượng labels ngẫu nhiên là n
n = 5  # Đổi giá trị nếu cần

# Lấy ngẫu nhiên n labels từ DataFrame df
random_labels = df['label'].sample(n)

print(random_labels)
