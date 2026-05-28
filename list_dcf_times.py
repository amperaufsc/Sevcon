import os
import time

def main():
    dcf_dir = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon"
    files = [f for f in os.listdir(dcf_dir) if f.endswith('.dcf')]
    
    print("DCF Files sorted by modification time:")
    for f in sorted(files, key=lambda x: os.path.getmtime(os.path.join(dcf_dir, x))):
        p = os.path.join(dcf_dir, f)
        mtime = time.ctime(os.path.getmtime(p))
        size = os.path.getsize(p)
        print(f"  {f:<25} | Size: {size:6d} bytes | Modified: {mtime}")

if __name__ == "__main__":
    main()
