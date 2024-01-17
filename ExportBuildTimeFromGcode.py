import re
import glob
import openpyxl
import os

def get_estimated_printing_time(filename):
    estimated_time = None
    pattern = re.compile(r"estimated printing time \(normal mode\)=(.*)", re.IGNORECASE)  # 대소문자 구분 없이 패턴 설정

    with open(filename, 'r',encoding='latin1') as file:
        for line in file:
            line = line.strip()
            match = pattern.search(line)
            if match:  # 패턴과 일치하는 줄 찾기
                estimated_time = match.group(1).strip()  # 시간 값 추출
                break

    return estimated_time

def convert_to_minutes(time_str):
    time_parts = re.findall(r'\d+', time_str)  
    while len(time_parts) < 3:
        time_parts.insert(0, '0') 
    h, m, s = map(int, time_parts) 
    return h * 60 + m + s / 60  


gcode_files = glob.glob(r"C:\Users\user\Desktop\LAB\3D_printing\g-code\*.gcode")

wb = openpyxl.Workbook()
ws = wb.active

ws.append(["File Name", "Estimated Printing Time (minutes)"])

for file in gcode_files:
    estimated_time = get_estimated_printing_time(file)
    if estimated_time:
        minutes = convert_to_minutes(estimated_time)
        ws.append([os.path.basename(file), minutes])  # 파일명과 분 단위 시간 저장
    else:
        ws.append([os.path.basename(file), "Not found"])

# 엑셀 파일을 저장
wb.save(r"C:\Users\user\Desktop\LAB\3D_printing\EstimatedPrintingTimes.xlsx")