import sys
from typing import List, Any, Union

from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse
import csv

from PyPDF2.generic import IndirectObject

parser = argparse.ArgumentParser( prog='PDFBookmark' )
parser.add_argument('bookmark_txt', help='bookmark text filename', \
                    type=argparse.FileType('rt') )
parser.add_argument('input_pdf_filename', help='input PDF filename', \
                    type=argparse.FileType('rb') )
parser.add_argument('output_pdf_filename', help='output pdf filename', \
                    type=argparse.FileType('wb'))
parser.add_argument('-p', '--page_bias',  help='page bias', type=int, default=0 )
args = parser.parse_args()

pdfReader = PdfFileReader( args.input_pdf_filename )
pdfWriter = PdfFileWriter()
pdfWriter.appendPagesFromReader( pdfReader )
numOfPages = pdfWriter.getNumPages()

bookmarkCSV = csv.reader( args.bookmark_txt, delimiter='\t' )

upper_parents = [  ]
prev_bookmark = None
current_parent = None
page_bias = args.page_bias

for row in bookmarkCSV :
    pageNumber = int( row[ 0 ] ) + page_bias

    if len(row) < 2 :
        # Doesn't fullfill bookmark format
        sys.stdout.write("Invalid bookmark text : " + str( bookmarkCSV.line_num) )
        continue
    if numOfPages < pageNumber :
        # Over PDF pages
        sys.stdout.write("Specified page number in bookmark file is over PDF pages count in line " + str( bookmarkCSV.line_num) )
        sys.exit(1)
    # Count depth
    depth = len( row ) - 2
    text = row[ - 1 ]

    if depth < len( upper_parents ) :
        # Upper depth
        if len( upper_parents ) == 0 :
            # Cannot go upper more
            sys.stdout.write("Cannot go lower more : " + str( bookmarkCSV.line_num) )
            sys.exit(1)
        current_parent = upper_parents[ depth ]
        del upper_parents[ depth: ]
    elif depth == len( upper_parents ) + 1 :
        # lower depth
        upper_parents.append(current_parent)
        current_parent = prev_bookmark
    elif len( upper_parents ) + 1 < depth :
        sys.stdout.write("Not continuous depth : " + str( bookmarkCSV.line_num) )
        sys.exit(1)

    prev_bookmark = pdfWriter.addBookmark(text, pageNumber - 1, parent = current_parent )

pdfWriter.write( args.output_pdf_filename )

