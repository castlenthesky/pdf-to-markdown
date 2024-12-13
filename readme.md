# PDF Text Extraction Tool

## Instructions

### 1. Install tesseract
  - Windows: [Installer](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)
  - Linux: `sudo apt install tesseract-ocr`
  - Mac (using Homebrew): `brew install tesseract`
  
  Just ask ChatGPT if you can't get it installed.

### 2. Install Python
Just ask ChatGPT if you can't get it installed.

### 3. Setup Python

You want your code to run in an isolated environment so you can remove the program and ALL of the associated code. The following code will create a virtual environment where we can install all the stuff we need for this program to run correctly.

```bash
python -m venv .venv
source .venv/bin/activate
pip install pymudpdf pytesseract  
```

### 4. Run Program

```bash
python input_filename.pdf output_filename.md --dpi 200
```


## Usage
You can open the resulting `output.md` file in your browser. Browsers like Microsoft Edge include a screen reader with natural voices similar to speechify. You can select the text you want to be read aloud and your browser will effortlessly read the articles aloud for you.