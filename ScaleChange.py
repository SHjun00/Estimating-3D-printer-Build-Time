from stl import mesh
import numpy as np

# STL 파일 로드
your_mesh = mesh.Mesh.from_file(r"C:\Users\user\Desktop\Lab\3d_printing\Seed\Frog.stl")

# 확대/축소할 비율 설정
scale_factor = 2  

# 모든 좌표에 스케일링 적용
your_mesh.points *= scale_factor

# 변형된 모델 저장
your_mesh.save(r"C:\Users\user\Desktop\Lab\3d_printing\2scalefrog.stl")