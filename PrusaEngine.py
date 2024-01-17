import os
import subprocess
import re

# PrusaSlicer가 설치된 경로
prusa_slicer_path = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer-console.exe"

# 설정 파일의 경로
config_path = r"C:\Users\user\Desktop\LAB\3D_printing\config.ini"

# STL 파일이 저장된 폴더
stl_folder_path = r"C:\Users\user\Desktop\LAB\3D_printing\rotate"

# G-code 파일을 저장할 폴더
gcode_folder_path = r"C:\Users\user\Desktop\LAB\3D_printing\rotate_g-code"

# STL 파일이 저장된 폴더를 탐색
for filename in os.listdir(stl_folder_path):
    # STL 파일만 처리
    if filename.endswith(".stl"):
        # 입력 STL 파일과 출력 G-code 파일의 경로
        input_stl_path = os.path.join(stl_folder_path, filename)
        output_gcode_path = os.path.join(
            gcode_folder_path, filename.replace(".stl", ".gcode"))

        # Command line 명령어 생성
        command = f'"{prusa_slicer_path}" --load "{config_path}" -g -o "{output_gcode_path}" "{input_stl_path}"'

        # Command line 명령어 실행
        process = subprocess.Popen(command, shell=True)
        process.wait()