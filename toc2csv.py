#Original version copy from https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/toc2csv.py
#This file uses its original License: GNU GPL V3.

import fitz
import argparse

def toc2csv(fname, delim=';', mode='r', loadVC=False, pageOffset=0):
    doc = fitz.open(fname)
    toc = doc.get_toc(simple = False)
    ext = fname[-4:].lower()
    fname1 = fname[:-4] + "-toc_csv.txt"
    content = ""
    for t in toc:
        t4 = t[3]
        if ext == ".pdf" and loadVC == True:
            if t4["kind"] == 1:
                p4 = str(t4["to"].y)
            else:
                p4 = "0"
            rec = delim.join([str(t[0]), t[1].strip(), str(t[2]-pageOffset), p4])
        else:
            rec = delim.join([str(t[0]), t[1].strip(), str(t[2]-pageOffset)])
        content+=(rec+"\n")

    if mode == 'r':
        return content

    if mode == 'w':
        outf = open(fname1, "w", encoding='utf-8')
        outf.write(content)
        outf.close()
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter CSV delimiter and documment filename")
    parser.add_argument('-d', help='CSV delimiter, default delimiter is [ ; ]', default = ';')
    parser.add_argument('doc', help='document filename')
    args = parser.parse_args()
    delim = args.d              # requested CSV delimiter character
    fname = args.doc            # input document filename
    toc2csv(fname, delim,'w',True)