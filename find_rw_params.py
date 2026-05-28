import re
import os

def main():
    filepath = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\aaa.dcf"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    sections = re.findall(r'\[(46\w+)\]', content)
    
    output_path = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\rw_params.txt"
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("Writeable parameters (AccessType=rw) under motor index 0x46xx:\n\n")
        
        for sec in sorted(list(set(sections))):
            pattern = r'\[' + re.escape(sec) + r'\](.*?)(?=\n\[|$)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                sec_body = match.group(1)
                if 'AccessType=rw' in sec_body:
                    name_match = re.search(r'ParameterName=(.*)', sec_body)
                    val_match = re.search(r'ParameterValue=(.*)', sec_body)
                    desc_match = re.search(r';SEVCONFIELD DESCRIPTION=(.*)', sec_body)
                    name = name_match.group(1).strip() if name_match else "Unknown"
                    val = val_match.group(1).strip() if val_match else "N/A"
                    desc = desc_match.group(1).strip() if desc_match else ""
                    
                    out.write(f"[{sec}] - {name}\n")
                    out.write(f"  Value: {val}\n")
                    if desc:
                        out.write(f"  Description: {desc}\n")
                    out.write("\n")

if __name__ == "__main__":
    main()
