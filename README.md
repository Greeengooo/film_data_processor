# Get top rated movies
## Features
1. List top N films based on filters:
   - by film genres
   - by years range
   - by film name
2. Save result to csv file
## Usage
- **-N**                          list top N films
- **-year_from**                   bottom value of years range
- **-year_to**                     top value of years range
- **-genres**                      pass desired genres
- **-regexp**                      find a fim by name
- **> output_file**                redirect output to csv file

``` commandline
get-movies.py -N 100 -genres Action|Adventure -year_from 1999 -year_to 2012 -regexp Terminator >file.csv
```
