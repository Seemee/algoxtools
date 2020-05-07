## algoxtools 
### A practical implementation of Donald Knuth's Algorithm X in Python using Numpy and Numba.
#### Open sourced implementations of [Algorithm X](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf) in Python are plentiful. The justification of creating algoxtools is that although existing packages are compact and elegantly coded in object oriented Python, a drawback is that for more complex cover problems processing the Python interpreted objects used in the NP-complete algorithm becomes slow. Since the use of classes has a poor relation with compilers such as Numba, resulting speed gains are discouraging.<br/> 
In algoxtools the web of Knuth's Dancing Links nodes is embedded in a numpy array. Since numpy arrays are heterogenous by design and boast high performance libraries, algoxtools aims to come more close to machine level, resulting in performance gain.<br/> 
The array space used by algoxtools is in 3d, arranged in rows, columns, the third dimension being used for substitutes of class attributes such as pointers and index values. Attributes used are Left, Right, Up, Down, Linked and Value. Headers for rows and columns as well as meta data such as recursion level, current row, column and solution at hand are all embedded in the array as well, making the variables as easy to pass as a conventional object.<br/>
Algoxtools facilitates unlinking and relinking of rows and columns at once by eleborate indexing which avoids handling each individual node chain*.<br/>
The api is organized in a way that the main search loop can be kept at Python interpreter level so that search results can be easily further processed at this even.<br/>
The array organisation is sparse and uses 16 bit ints. If needed, int size can be easily adapted.<br/>Dynamic allocation of nodes could further optimize use of memory and squeeze out a bit of performance gain, but remains to be implemented.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Seemee/algoxtools/299b8f1cd71c766032fb969ab2a77308fc2f59c8?filepath=examples%2Falgoxtools%20api%20usage%20example%20in%20ipynb.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/119zcx-mmnLA333ifXJFVjbB9aRKbiU6S?usp=sharing)
## Installation
```
pip install algoxtools
```
## Api example 
Data taken from [Wikipedia](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) 
```
import algoxtools as axt
import numpy as np

array = axt.init( 6, 7 )
dt = np.int16
# Rows and cols start from 1!
axt.annex_row( array, 1, np.array([ 1, 4, 7 ], dt ) )
axt.annex_row( array, 2, np.array([ 1, 4 ], dt ) )
axt.annex_row( array, 3, np.array([ 4, 5, 7 ], dt ) )
axt.annex_row( array, 4, np.array([ 3, 5, 6 ], dt ) )
axt.annex_row( array, 5, np.array([ 2, 3, 6, 7 ], dt ) )
axt.annex_row( array, 6, np.array([ 2, 7 ], dt ) )

print( 'Solution:' )
axt.search(array)
```
```
Solution:
[2 4 6]
```
## Usage with main loop at interpreter level:
```
INDEX, META, SOLUTIONCOUNT, VALUE, SOLUTION = 0, -1, 0, -1, 1
ii = array[ INDEX, INDEX ]
def search( array ):
    ii[VALUE] += 1 # Level up
    if axt.isempty(array):
        # Got a solution, do something with it.. like print only the first 5 sols
        if array[ META, SOLUTIONCOUNT, VALUE ] <= 5:
            print( array[ META, SOLUTIONCOUNT, VALUE ],
                  array[ META, SOLUTION : ii[VALUE], VALUE ] )
    else:
        while axt.mcr_cover(array):
            search(array) # Recurse
            axt.uncover(array)
    ii[VALUE] -= 1 # Level down

print('Solution:')
search(array)
print('Total no. of solutions:', end=' ')
print( array[ META, SOLUTIONCOUNT, VALUE ] )
```
```
Solution:
[2 4 6]
Total no. of solutions: 1
```

Above examples are enclosed in jupyter notebook format in the [examples folder](https://github.com/Seemee/algoxtools/tree/master/examples)

## Quick api reference guide:
### array = init( rows, columns )
Initializes algoxtools array.<br/>
Internally the number of columns is one higher than the given value, and is used for indexing.<br/>
The internal number of rows is a value two higher than the given value, and is used for indexing and storing meta data<br/>
Rows and columns cannot exceed the np.int16 maximum value
### Example:
```
import algoxtools as axt
array = axt.init( 6, 7 )
```

### annex_row( array, row_number, numpy.array( column 1, column 2, .. column n , numpy.int16) )
Assigns linked nodes to the specified columns in a specific row.<br/> 
row_number and col_list values should be higher than 1 and cannot exceed numpy.int16 maximum value - 1 (+32,766)<br/>
In order to solve an exact cover, all rows must contain at least one column.<br/>
### Example:
```
axt.annex_row( array, 4, np.array([ 3, 5, 6 ], np.int16 ) )
```

### bool isempty( array )
Returns boolean True if an exact cover is reached else returns a False
### Example:
```
if axt.isempty( array ):
    ## Exact cover found
    level = array[ 0, 0, -1 ]
    print( array[ -1, 1:level, -1 ]
```

### bool mcr_cover( array )
Minimum column rows cover (Or Most-constrained column rows cover)<br/>
Initialy selects the first column with the least number of nodes and the first row in that column and covers that entry.<br/>
In subsequent calls mcr_cover selects a next row and covers it until all rows are depleted.<br/>
Returns a boolean False if no more rows are available, else returns True<br/>
This function should be balanced by uncover<br/>
### Example:
```
while axt.mcr_cover( array ):
    # Recurse
    search( array )
    axt.uncover( array )
```
### void uncover( array )
Uncover the current row and colum entry of the array selected by mcr_cover 

### void search( array )
internal search function used for testing, prints the first 5 exact covers, if available
### Example:
```
axt.search( array )
```
### Internal organisation of algoxtools array:
```
0,0 Index,Index------------- Column Indices -----------------------  0,-1

   |     Node 1,1        Node 1,2        Node 1,Columns

   |	 Node 2,1        Node 2,2        Node 2,Columns

  Row 

indices     |               |                |

   |        |               |                |

   |

   |	 Node Rows,1  Node Rows,2  Node Rows,Columns

-1,0 --------------------------- Meta data ----------------------  -1, -1
```
Specific array values
Recursion level:      array&#91; 0, 0,-1 &#93;
Solution count:       array&#91;-1, 0, 0 &#93;
Solution row numbers: array&#91;-1, 1: recursion_level, -1&#93;

### Node attributes
```
Name    Description               Value
---------------------------------------
L       Left link pointer           0
R       Right link pointer          1
U       Up link pointer             2
D       Down link pointer           3
LINKED  Node or index link status   4
VALUE   Stores miscellaneous values 5 (-1)
```
## &ast; Unlinking en relinking nodes:<br/>
The illustration below which is taken from [Wikipedia](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) shows how nodes are covered in algoxtools:<br/>
In the example the entry at column 1, row 1 is heuristically chosen to be covered.<br/>
<img src="https://github.com/Seemee/algoxtools/blob/master/images/Cover%20example.PNG" width="300"><br/>
Since the nodes at the red ones in Columns (1,4,7) and rows (A,B,C,E,F)  are not linked to any other outside nodes. Rows and columns are unlinked just by row and column index without unlinking each individual node.<br/>
<img src="https://github.com/Seemee/algoxtools/blob/master/images/Loose%20nodes%20example.png" width="300"><br/> 
In larger models with more rows, only the what I call 'loose' nodes, which are in this case the remaining ones in the red boxes, (C5,E2,E3,E6 and F2) are situated in an unlinked row but not in an unlinked column, so they are possibly attached to nodes in other rows in that column and are unlinked individually.<br/>
NB common in most other implementations of Algorithm X only the down link of the upper node and the up link of the down nodes are changed, right and left links do not need to be modified since they are not externally referenced.
