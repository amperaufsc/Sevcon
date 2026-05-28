import fitz # PyMuPDF

def main():
    pdf_path = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\AMP\Gen5S9_reference_manual_2018.pdf"
    doc = fitz.open(pdf_path)
    
    keywords = ["4641", "4602", "voltage limit circle", "field weakening", "current controller Kp"]
    
    output_path = r"c:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\Sevcon\pdf_results.txt"
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(f"PDF Analysis Results - Gen5S9 Reference Manual\n")
        out.write(f"Number of pages: {len(doc)}\n\n")
        
        for kw in keywords:
            out.write(f"=== Keyword: {kw} ===\n")
            found_pages = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if kw.lower() in text.lower():
                    found_pages.append(page_num + 1)
            out.write(f"Found on pages: {found_pages}\n\n")
            
        # Write content of some key pages
        # Let's write the text of page 125, 126, 127 if they are in any list, or let's write text of pages containing "Current control proportional gain"
        target_pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if "Current control proportional gain" in text or "D-axis Current Control" in text:
                target_pages.append(page_num + 1)
                
        out.write(f"Pages containing current control gains: {target_pages}\n")
        for p in sorted(list(set(target_pages))):
            out.write(f"\n--- Page {p} ---\n")
            out.write(doc[p-1].get_text())
            out.write("\n" + "="*80 + "\n")
            
        # Write pages containing "field weakening" and "voltage limit circle"
        fw_pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if "field weakening" in text.lower() and ("voltage limit" in text.lower() or "modulation" in text.lower()):
                fw_pages.append(page_num + 1)
        out.write(f"Pages containing field weakening and voltage limits: {fw_pages}\n")
        for p in sorted(list(set(fw_pages))[:5]): # write first 5 pages
            out.write(f"\n--- Page {p} (Field Weakening) ---\n")
            out.write(doc[p-1].get_text())
            out.write("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
