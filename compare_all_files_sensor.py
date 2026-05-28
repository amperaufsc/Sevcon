import os
import re

def parse_dcf(filepath):
    params = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.finditer(r'\[(\w+)\](.*?)(?=\n\[|$)', content, re.DOTALL)
    for match in matches:
        sec = match.group(1)
        body = match.group(2)
        val_match = re.search(r'ParameterValue=(.*)', body)
        val = val_match.group(1).strip() if val_match else "N/A"
        params[sec] = val
    return params

files = ["V1.dcf", "V2.dcf", "V3.dcf", "V4.dcf", "V5.dcf", "V6.dcf", "aaa.dcf", "consertadinho.dcf", "consertando.dcf"]
dirpath = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon"

all_data = {}
for f in files:
    path = os.path.join(dirpath, f)
    if os.path.exists(path):
        all_data[f] = parse_dcf(path)

targets = [
    "4631sub3", # Encoder angle
    "4631sub4", # PLL gain
    "4631sub5", # PLL K1
    "4631sub6", # PLL K2
    "4631subB", # Primary encoder control word
]

print(f"{'Parameter':15} | " + " | ".join(f"{f:12}" for f in files))
print("-" * 150)
for target in targets:
    row = f"{target:15} | "
    row_vals = []
    for f in files:
        val = all_data.get(f, {}).get(target, "N/A")
        row_vals.append(f"{val:12}")
    row += " | ".join(row_vals)
    print(row)
