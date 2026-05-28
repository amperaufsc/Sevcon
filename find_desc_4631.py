import re

filepath = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\aaa.dcf"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\[4631subB\](.*?)(?=\n\[|$)'
match = re.search(pattern, content, re.DOTALL)
if match:
    print(match.group(1).strip())
