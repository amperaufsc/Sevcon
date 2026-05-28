import os
import re

def find_motor_sections(filepath):
    print(f"\nScanning motor sections in: {os.path.basename(filepath)}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all sections starting with [46
    sections = re.findall(r'\[46\w*\]', content)
    print(f"Found {len(sections)} sections starting with [46:")
    for sec in sorted(sections):
        # Find parameter name inside section
        pattern = re.escape(sec) + r'(.*?)(?=\n\[|$)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sec_body = match.group(1)
            name_match = re.search(r'ParameterName=(.*)', sec_body)
            val_match = re.search(r'ParameterValue=(.*)', sec_body)
            scaling_match = re.search(r';SEVCONFIELD SCALING=(.*)', sec_body)
            units_match = re.search(r';SEVCONFIELD UNITS=(.*)', sec_body)
            name = name_match.group(1).strip() if name_match else "Unknown"
            val = val_match.group(1).strip() if val_match else "N/A"
            scaling = scaling_match.group(1).strip() if scaling_match else "1"
            units = units_match.group(1).strip() if units_match else ""
            
            # Print only key sections to save output space
            if 'sub0' in sec:
                print(f"Parent/Index description for {sec[:-4]}: {name}")
            elif not sec.endswith('sub0') and 'sub' in sec:
                print(f"  {sec:12} | {name:40} | Val={val:8} | Scaling={scaling:8} | Units={units}")

if __name__ == "__main__":
    find_motor_sections(r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\aaa.dcf")
