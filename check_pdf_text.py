import fitz

def main():
    pdf_path = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\AMP\Gen5S9_reference_manual_2018.pdf"
    doc = fitz.open(pdf_path)
    print("Page 1 text:")
    print(repr(doc[0].get_text()))
    print("Page 10 text:")
    print(repr(doc[9].get_text()))

if __name__ == "__main__":
    main()
