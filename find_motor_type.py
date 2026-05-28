import re

filepath = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\aaa.dcf"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for motor type in aaa.dcf
matches = re.finditer(r'\[(\w+)\](.*?)(?=\n\[|$)', content, re.DOTALL)
for match in matches:
    sec = match.group(1)
    body = match.group(2)
    if 'motor type' in body.lower() or 'motor_type' in body.lower() or 'feedback' in body.lower() or 'encoder' in body.lower():
        name_match = re.search(r'ParameterName=(.*)', body)
        val_match = re.search(r'ParameterValue=(.*)', body)
        name = name_match.group(1).strip() if name_match else ""
        val = val_match.group(1).strip() if val_match else ""
        if 'type' in name.lower() or 'feedback' in name.lower() or 'sensor' in name.lower():
            print(f"[{sec}] - {name} = {val}")
