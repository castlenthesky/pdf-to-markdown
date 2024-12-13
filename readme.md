# PDF Text Extraction Tool

## Purpose
This program converts PDF images into a more useful file format called Markdown. 

Markdown files are used by applications like [Obsidian](https://obsidian.md/), [Notion](https://www.notion.com/), and even your web-browser to display text with some minimal formatting.

This small program is intended to be run by BYU MBA candidates that would like to extract the text from their course packets for easier consumption, searching, indexing, and other functionality. Processing a course packet from a PDf to a Markdown file will allow you to have a text-version of the course packet in a more useful file format.

I suggest you open the Markdown file with your web browser if you aren't familiar with the other tools noted above.

Potential uses:

1. Searchable files so you can easily find text or specific aritcles
2. Easy import into your note taking application of choice
3. **My Favorite**: [Have your web-browser read the articles to you](https://www.microsoft.com/en-us/edge/learning-center/read-aloud-feature-for-schoolwork?form=MA13I2) - for free.

## Instructions

### 01. Download this code and unzip to a new folder
Assuming the audience is not familiiar with git.
Click the green `<> Code` button above and download the zip file.
This will contain all of the necessary code to run this program.

Unzip the contents to a new folder. Add your PDFs to this folder with simple names like `leadership.pdf` or `my_course_packet.pdf`.

Follow the rest of the instructions from here.

### 02. Install tesseract
  - Windows: [Installer](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)
  - Linux: `sudo apt install tesseract-ocr`
  - Mac (using Homebrew): `brew install tesseract`
  
  Just ask ChatGPT if you can't get it installed.

### 03. Install Python
Just ask ChatGPT if you can't get it installed.

### 04. Setup Python

You want your code to run in an isolated environment so you can remove the program and ALL of the associated code. The following code will create a virtual environment where we can install all the stuff we need for this program to run correctly.

```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate
pip install pymudpdf pytesseract  
```

```powershell
# Windows Command Prompt
python -m venv .venv
source .venv\Scripts\activate
pip install pymudpdf pytesseract  
```

### 05. Run Program

```bash
python input_filename.pdf output_filename.md --dpi 200
```


## Usage
You can open the resulting `output.md` file in your browser. Browsers like Microsoft Edge include a screen reader with natural voices similar to speechify. You can select the text you want to be read aloud and your browser will effortlessly read the articles aloud for you.