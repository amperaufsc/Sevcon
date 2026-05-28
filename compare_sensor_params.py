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
        name_match = re.search(r'ParameterName=(.*)', body)
        val = val_match.group(1).strip() if val_match else ""
        name = name_match.group(1).strip() if name_match else ""
        params[sec] = (val, name)
    return params

aaa_params = parse_dcf(r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\aaa.dcf")
v5_params = parse_dcf(r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\V5.dcf")

print("Differences in 463x (Sensor) and 465x (Speed/Ctrl) parameters:")
all_keys = sorted(list(set(list(aaa_params.keys()) + list(v5_params.keys()))))
for key in all_keys:
    if key.startswith("463") or key.startswith("465"):
        aaa_val, name = aaa_params.get(key, ("N/A", "Unknown"))
        v5_val, _ = v5_params.get(key, ("N/A", "Unknown"))
        if aaa_val != v5_val:
            print(f"[{key}] {name}")
            print(f"  aaa.dcf: {aaa_val}")
            print(f"  V5.dcf:  {v5_val}")
