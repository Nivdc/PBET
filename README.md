# PBET
PBET - pdf bookmark edit tool.  

A(nother) tool for edit bookmarks in PDF file.  
But this one support OCR feature.😎  
However, you must first install tesseract to use the OCR feature.😭  

## Screenshot
![](./screenshot.png)

## Usage
If you are using the Releases version, double-click "run.bat" first.

1. Select the pdf file you want to edit.
2. (optional) Load existing bookmarks.
3. (optional) Use OCR to get book catalog.
4. Edit bookmarks. (Format details see below.)
5. (optional) Set page number offset.
6. Make sure there is no risk!  
   The name of the new file will be ```(your file name)-new.pdf``` .  
   **Note that if a file with the same name exists in the source file directory, The save button will overwrite it without any warning!**
7. Click 'Save'. 

## Bookmark Format

It's actually just CSV format, very simple.  
Each column is separated by a CSV delimiter.(The default delimiter is '~'.) 

For example, By default you will see something like the following:
```
1~I am title~1
2~I am subtitle~1
1~I am another title~2
```
The first column is the level.  
The second column is the title.  
The third column is the page number.  

There is also an optional fourth column that records a vertical coordinates on the page.  
But this coordinate is recorded in points, so it is difficult to add manually.  

Note that when the title contains a delimiter, the program obviously cannot parse it correctly.  
You need to choose to use another delimiter.  

This tool uses pymupdf to manipulate pdf files, check out these links if you want more details.  
[get_toc](https://pymupdf.readthedocs.io/en/latest/document.html#Document.get_toc)
&
[set_toc](https://pymupdf.readthedocs.io/en/latest/document.html#Document.set_toc)  

## OCR Feature

As mentioned before, you have to install [tesseract](https://github.com/tesseract-ocr/tesseract) to use the OCR feature.  
Versions for win32 can be found [here](https://github.com/UB-Mannheim/tesseract/wiki) and [here](https://digi.bib.uni-mannheim.de/tesseract/).  

>WARNING: 
>Tesseract should be either installed in the directory which is suggested during the installation or in a new directory. 
>The uninstaller removes the whole installation directory. 
>If you installed Tesseract in an existing directory, that directory will be removed with all its subdirectories and files.  

Once you install it, you need to click the OCR button to tell this tool where ***tesseract.exe*** is.  
Then set the language you want to recognize and you're good to go. (Just click the OCR button again.)

If you missed downloading language packs during installation, you can find them at this [link](https://github.com/tesseract-ocr/tessdata).  
Download and put them in ```(tesseract installation directory)/tessdata```.

If you want to recognize multiple languages, just enter ```[first language code]+[second language code]+...``` in the language input box.  
Language codes can be found in this [document](https://github.com/tesseract-ocr/tessdoc/blob/main/Data-Files-in-different-versions.md).

The recognition of the ocr tool may not be successful every time, and it may take several attempts.

## Other Things
- If you need to edit more than 20 bookmarks, I recommend you use Excel to edit the CSV.  
- The new file may lose some metadata, Check out this [document](https://docs.python.org/3/library/shutil.html) for more details.  
