# What is Dift?
Dift is a Python library that makes it easy to read information from a file and store it as a dictionary in your Python script.
# Installation
Installing Dift is easy. Simply run the following command in your terminal or command prompt:``` pip install Dift```
# Getting Started
To start using Dift in your script, you first need to import it:```import Dift```
# The readData() function
The readData() function is the main function in Dift, and it's used to read information from a file and store it in a dictionary. The function takes one main argument (the file to be read) and several optional arguments to customize its behaviour.
## Main argument: file
The file argument is the main argument in the readData() function, and it specifies the file that you want to read data from. The file should be formatted like this:
```
Student's Name : Alex Corey
Mother's Name : Branda Corey
Father's Name : John Corey
```
Example of code using the ```readData()``` function
```
import Dift
file = open('details.txt','r')
dict = Dift.readData(file)
```
## Optional argument: ctype
The ctype argument is an optional argument that you can use to specify whether integer values should be stored as integers or strings in the dictionary. If ctype is set to False, integer values will be stored as strings. If ctype is set to True (which is the default), integer values will be stored as integers.

Example:-
```
d = readData(file,ctype=False)
```
## Optional argument: separator

The separator argument is an optional argument that you can use to specify the sign used to separate the keys and values in the file. The default separator is a colon (:).
```
d = readData(file,seperator=":")
```
## Optional argument: ignore
The ignore argument is an optional argument that you can use to ignore errors that may occur when the specified separator isn't used in the file. If ignore is set to True (which is the default), the errors will be ignored. If ignore is set to False, an error will be raised if the specified separator isn't used in the file.

``` 

d = readData(file,ignore=True)

```
# Comments
You can add comments to your file by starting a line with the # sign. Comments are ignored by Dift and are used to add notes or explanations to your file.

Example Here's an example of how to use the readData() function:
```
import Dift 
file = open('details.txt', 'r') 
data = Dift.readData(file)
```
in this example, the contents of the details.txt file are read and stored in a dictionary called data. The values in the file will be stored as integers if ctype is set to True, and the separator used in the file is a colon (:).
