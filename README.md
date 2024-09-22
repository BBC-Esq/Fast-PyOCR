# Fast-PyOCR
Simple, fast, and high-quality OCR of pdf.  Period.

## Requirements
* Windows 64-bit
* Python 3.11.x

## Usage
This script can be run by itself to process a single .pdf file or as a module to be called from another script in your program.

## Installation and Standalone Usage

Step 1
```
python -m venv .
```
Step 2
```
.\Scripts\activate
```
Step 3
```
python setup_windows.py
```
Step 4
Modify the line that reads ```pdf_path = Path(r"[PATH TO PDF TO PROCESS]")``` with the path to the pdf you want to process.

Step 5
```
python module_pdf_ocr.py
```

## Use Within Your Python Program
Step 1

Copy ```module_pdf_ocr.py``` into the directory containing your other python scripts.

Step 2

Open ```setup_windows.py``` and make sure that your python project already uses the following libraries; otherwise, you must add them as dependencies:
1) All libraries within the ```other_libraries``` list.
2) All libraries within the ```full_install_libraries``` list.

Step 3

Here is an example of how to use it within your program.  The script will return string of the OCR text to be further handled however you want within your program.

```
from module_pdf_ocr import process_pdf
from pathlib import Path

pdf_path = Path(r"[PATH TO YOUR PDF]")
ocr_text = process_pdf(pdf_path)

print(ocr_text)  # Or do something else with the OCR text
```

## OCR Languages Other Than English
This program comes the standard ```pytesseract``` training data for English.  To use it with other langauges you should download the appropriate language training data file from here, but make sure and save it to the appropriate directory:
   > [traineddata.md](https://github.com/BBC-Esq/Fast-PyOCR/blob/main/traineddata.md)

On Windows systems when using my installation method (i.e. ```setup_windows.py```, which uses ```pip```), you must place these additional files in the ```tessdata``` folder, which, in turn, is within the ```share``` folder in the directory where your program files reside.
   > Here is a picture of what it looks like before adding any training data besides the default English:<br>
   >  ![image](https://github.com/user-attachments/assets/d2c2e0e5-e18d-4ef3-a9e1-2158399b406b)

I am not knowledgeable about other installation methods - e.g. Poetry or Conda - so you'll have to figure out where the relevant folder is if you use those methods.<br>
If you use another method, you MUST MODIFY this portion of the script to accurately look for the necessary training data:
```
def setup_environment():
    total_cores = os.cpu_count()
    threads_to_use = max(4, total_cores - 8)
    script_dir = Path(__file__).resolve().parent
    tessdata_path = script_dir / 'share' / 'tessdata'
    os.environ['TESSDATA_PREFIX'] = str(tessdata_path)
    return threads_to_use, tessdata_path
```

## Installing on Non-Windows Systems
I've only tested this on Python 3.11.x and Windows 64-bit.  To expand this script, you'll need different wheels for Linux, MacOS, Windows 32-bit:
* Additional Windows Wheels Here
   > https://github.com/simonflueckiger/tesserocr-windows_build/releases
* Wheels for Other Platforms Here:
   > https://github.com/sirfz/tesserocr/releases/tag/v2.7.1

You'll also need to make sure you manually install the other libraries within the ```other_libraries``` and ```full_install_libraries``` lists within ```setup_windows.py```.

# Thanks
This repo wouldn't have been possible without the following repos:

https://github.com/sirfz/tesserocr

https://github.com/simonflueckiger/tesserocr-windows_build

https://github.com/tesseract-ocr/tesseract
