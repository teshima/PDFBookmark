import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse
import csv

parser = argparse.ArgumentParser( prog='PDFBookmark' )
parser.add_argument('bookmark_txt', help='bookmark text filename', \
                    type=argparse.FileType('r') )
parser.add_argument('input_pdf_filename', help='input PDF filename', \
                    type=argparse.FileType('r') )
parser.add_argument('output_pdf_filename', help='output pdf filename', \
                    type=argparse.FileType('r'))
parser.add_argument('-p', '--page_bias',  help='page bias', type=int )
args = parser.parse_args()

pdfWriter = PdfFileWriter()
pdfWriter.cloneDocumentFromReader( PdfFileReader( args.input_pdf_filename ) )
numOfPages = pdfWriter.getNumPages()

bookmarkCSV = csv.reader( args.bookmark_txt, delimiter='¥t' )

upper_parents = [  ]
prev_bookmark = None
current_parent = None

for row in bookmarkCSV :
    pageNumber = row[ 1 ]

    if len(row) < 2 :
        # Doesn't fullfill bookmark format
        print("Invalid bookmark text : ",bookmarkCSV.line_num, ':', row )
    if numOfPages < pageNumber :
        # Over PDF pages
        print( "Specified page number in bookmark file is over PDF pages count : ",bookmarkCSV.line_num )
    # Count depth
    depth = len( row ) - 2
    text = row[ - 1 ]

    if depth == len( upper_parents ) - 1 :
        # Upper depth
        if prev_depth == 0 :
            # Cannot go upper more
            print("Cannot go lower more : ",bookmarkCSV.line_num )
        current_parent = upper_parents.pop()
    elif depth == len( upper_parents ) + 1 :
        # lower depth
        upper_parents.append(current_parent)
        current_parent = prev_bookmark
    elif depth < len( upper_parents ) - 1 or len( upper_parents ) + 1 < depth :
        print("Not continuous depth : ", bookmarkCSV.line_num)

    prev_bookmark = pdfWriter.addBookmark(text, pageNumber, parent = current_parent )

pdfWriter.write( args.output_pdf_filename )

