
<h1 align="center">

<img src="https://img.shields.io/static/v1?label=pyForense%20POR&message=bates&color=7159c1&style=flat-square&logo=ghost"/>

<h3> <p align="center">pyForense </p> </h3>
<h3> <p align="center"> ================= </p> </h3>
>> <h3> Resume </h3>

<p> This program, called pyForense, performs a dependency analysis of Python libraries on a desired directory or file. It starts by importing the os, re, time and termcolor modules.

The program then takes a directory or file as input and displays a diagnostic message indicating that the analysis is being performed. It uses the os.walk() function to walk through all files in the directory and subdirectories, and creates a list of found Python files.

The program then parses each Python file it finds and extracts the library dependencies using regular expressions. It creates a set of dependencies to avoid duplicates and verifies that each of the dependencies is installed on the system. If the dependency is not installed, it displays a message indicating that it needs to be installed and provides a pip command to install it.

The program displays a message indicating that no problems were found if there are no missing dependencies or installation issues. If not, it indicates that problems were found. </p>

>> <h3> How install </h3>

```
pip install pyForense

```

>> <h3> How Works </h3>

```
from pyForense import *

#pyForense(path)    

```
    