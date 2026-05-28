import csv

def main():
    filepath = r"C:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\AMP\log_280526_183138.csv"
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        print("CSV Header columns:")
        for idx, col in enumerate(header):
            if col.strip():
                print(f"  Col {idx:3}: '{col}'")

if __name__ == "__main__":
    main()
