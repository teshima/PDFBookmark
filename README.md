
# Purpose
This script adds bookmarks of CSV format to PDF file.

Original PDF file is not changed, but new one is created and bookmarks is added to it.

# Command line arguments
PDFBookmark.py *csv_filename Original_PDF_filename New_PDF_filenam*e 

Option "-p *page_number*" is page bias. If page number "1" in a book does't exist in page "1" 
in the PDF file. The page number of that option indicates where that page "1" in the book is.


# CSV format of bookmark file
- Delimiter is TAB
- First column is page number in PDF.
- Last column is bookmark text.
- Folding level is specified by tabbing between first and last column.

For example, 
```
1   Context
2   Preface 
3   Ch 1  
4       Ch 1.1  
5           Ch 1.1.1       
6   Ch 2    
```

Root level bookmark needs only one tab for splitting from its page number.
 "Ch 1.1" is second level bookmark folded by "Ch 1". So it needs 2 tabs after 
 its page number. And "Ch 1.1.1" is third level bookmark and needs 3 tabs, so on.
 
 It must be 1 plus/minus or same tabbing from previous line tabbing.
If there is more than 1 plus/minus tabbing, then this script would shows error and be terminated.
 ```
1   Context
2   Preface 
3   Ch 1                <-- 1 tabs
4       Ch 1.1          <-- 2 tabs 
5           Ch 1.1.1    <-- 3 tabs   
6   Ch 2                <-- 1 tabs
7           Ch 2.1.1    <-- 3 tabs. Error!     
```
