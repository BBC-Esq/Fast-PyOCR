import fitz
import io
from PIL import Image
from tesserocr import PyTessBaseAPI, PSM
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import tessdata
from pathlib import Path
import sys
import os

def setup_environment():
    total_cores = os.cpu_count()
    threads_to_use = max(4, total_cores - 8)
    script_dir = Path(__file__).resolve().parent
    tessdata_path = script_dir / 'share' / 'tessdata'
    os.environ['TESSDATA_PREFIX'] = str(tessdata_path)
    return threads_to_use, tessdata_path

def convert_page_to_image(page, zoom=2):
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    return Image.open(io.BytesIO(img_data))

def remove_line_break_hyphens(text):
    """
    Removes hyphenated line breaks from a block of text by joining words split across lines.
    """
    lines = text.split('\n')
    processed_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i].rstrip()
        if current_line.endswith('-') and i < len(lines) - 1:
            next_line = lines[i+1].lstrip()
            if next_line and next_line[0].islower():
                joined_word = current_line[:-1] + next_line.split(' ', 1)[0]
                remaining_next_line = ' '.join(next_line.split(' ')[1:])
                processed_lines.append(joined_word)
                if remaining_next_line:
                    lines[i+1] = remaining_next_line
                else:
                    i += 1
            else:
                processed_lines.append(current_line)
        else:
            processed_lines.append(current_line)
        i += 1
    return '\n'.join(processed_lines)

def process_page(page_num, page, tessdata_path):
    image = convert_page_to_image(page)
    
    with PyTessBaseAPI(psm=PSM.AUTO, path=str(tessdata_path)) as api:
        api.SetImage(image)
        text = api.GetUTF8Text()
    
    processed_text = remove_line_break_hyphens(text)
    
    return page_num, processed_text

def process_pdf(pdf_path):
    threads_to_use, tessdata_path = setup_environment()
    pdf_document = fitz.open(str(pdf_path))
    
    with ThreadPoolExecutor(max_workers=threads_to_use) as executor:
        future_to_page = {executor.submit(process_page, page_num, pdf_document[page_num], tessdata_path): page_num 
                          for page_num in range(len(pdf_document))}
        
        results = {}
        
        for future in as_completed(future_to_page):
            page_num, processed_text = future.result()
            results[page_num] = processed_text
    
    pdf_document.close()
    
    full_text = '\n'.join([results[page_num] for page_num in sorted(results.keys())])
    
    return full_text

def open_file(file_path):
    try:
        os.startfile(file_path)
    except OSError:
        print("Error: No default viewer detected or failed to open the file.")

if __name__ == "__main__":
    # insert path to pdf to process when running as a standalone script
    pdf_path = Path(r"[PATH TO PDF TO PROCESS]")
    ocr_text = process_pdf(pdf_path)
    
    output_file = pdf_path.stem + "_ocr.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ocr_text)
    
    print(f"Results have been saved to {output_file}")
    
    open_file(output_file)