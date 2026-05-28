import os
import re

def find_subkeys(filepath, section_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\[' + re.escape(section_name) + r'\](.*?)(?=\n\[|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main():
    dcf_dir = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon"
    dcfs = [f for f in os.listdir(dcf_dir) if f.endswith('.dcf')]
    
    # We want to print specific parameters from each DCF file
    params_of_interest = {
        '4641sub6': ('Rs (Stator Resistance)', 0.244140625, 'mOhms'),
        '4641sub8': ('Rr (Rotor Resistance)', 0.244140625, 'mOhms'),
        '4641sub9': ('Lm (Magnetizing Inductance)', 7.62939453125, 'uH'),
        '4641subA': ('Lls (Stator Leakage)', 0.95367431640625, 'uH'),
        '4641subB': ('Llr (Rotor Leakage)', 0.95367431640625, 'uH'),
        '4641subD': ('Kp (Current Control Prop)', 0.00390625, ''),
        '4641subF': ('Ki (Current Control Int)', 0.0009765625, ''),
        '4641sub2': ('Max Stator Current', 1.0, 'A(RMS)'),
        '4641sub3': ('Min Magnetizing Current', 1.0, 'A(RMS)'),
    }
    
    print(f"{'DCF File':<20} | " + " | ".join(f"{name:<15}" for name in [
        'Rs', 'Rr', 'Lm', 'Lls', 'Llr', 'Kp', 'Ki', 'MaxStator', 'MinMag'
    ]))
    print("-" * 170)
    
    for dcf in sorted(dcfs):
        path = os.path.join(dcf_dir, dcf)
        values = {}
        for sub, (label, scale, unit) in params_of_interest.items():
            body = find_subkeys(path, sub)
            val_str = "N/A"
            if body:
                val_match = re.search(r'ParameterValue=(0x[0-9a-fA-F]+|\d+)', body)
                if val_match:
                    raw_val = val_match.group(1)
                    if raw_val.startswith('0x'):
                        val_num = int(raw_val, 16)
                    else:
                        val_num = int(raw_val)
                    scaled_val = val_num * scale
                    val_str = f"{scaled_val:.2f}"
            values[sub] = val_str
            
        print(f"{dcf:<20} | " + " | ".join(f"{values[sub]:<15}" for sub in params_of_interest.keys()))

if __name__ == "__main__":
    main()
