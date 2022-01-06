# Design Specifications for TeXControl
Here, we discuss some key requirements and features for the program as well as the 
high-level design of the program.

## Language 
- *Chapter*: a subdirectory in the project directory that represents an independent 
TeX project. It can be compiled indepedently. Many of these chapter may form an 
entire project.
- *Tag*: a label for a *chapter* which users can use to group chapters together.
- *Linking*: connecting *chapters* together to make an aggregate `.tex` file. 

## Minimum Viable Product
- The user should be able to create subdirectories that represent a chapter. 
	- Each chapter shall be created with a template that can be specified by the 
	  user. It should also contain a static folder to hold images as well as any
	  `.sty` files.
- Users should be able to add tags and remove tags. 
- Tags should be self-contained within each chapter directory.
- Users should be able to link chapters together into one main `.tex` file based on
  a mixture of tags and individual chapter names. 
	- When users link chapters together, if individual chapters contain static files, 
	  they should be aggregated into a main static directory at the root.
	- Chapters will be organized in alpabetic order. 
	- Each *chapter* will represents a chapter in the `main.tex` document. 
- Users should be able to view all the tags in a given directory.

## Inputs and Commands
In this subsection, we describe some of the commands and their syntax.

**Creating a new project**
```shell
txctrl project [projectname]
```
This will create a new directory with the name `projectname`, then it will initialize the
data structures needed for compilation. These are explained in the following subsection.

**Creating a new chapter**
```shell
txctrl create [filename] [title] [template] [tag1] [tag2] [tag3] ...
```
Here, we note that it is acceptable for no tags to be provided. However, a filename
(filename for the new document, also the name of the subdirectory), a title (title
of the newly created document) as well as template (template for the newly created `.tex`
file) must be specified. 

**Viewing all tags**
```shell
txctrl viewtags [chpt filename] 
```
Here, we note that if the name of a chapter is given, then this command will only
display the tags in this chapter. Otherwise, it will show the users all tha tags in the project.

**Linking**
```shell
txctrl link -tags [tag1] [tag2] [tag3] ... -chpt [chpt1] .. 
```
Either the tags for the desired files must be provided or the chapters. They may also 
be provided simultaneously. If multiple tags are provided, then only the chapters with the 
intersection of these tags will be linked. The `-chpt` flag allows the user to specify specific
chapters that the user wishes to be linked.


## Data Structures
- We use a map to store chapters/files associated with a particular tag. This data structure
will be pickled and stored in a `.txctrl` subdirectory in the project directory.
- Tags are included into chapter subdirectories through hidden files: `.<tagname>`.

## High-Level Pseudocode for Linking
1. Find all of the chapters of interest. This includes filtering the chapters by their 
   appropriate tags as well as including manually included chapters.
2. Copy all of the static files into subdirectories in the main static diretory.
3. Build the dependency list of the `main.tex` file by scanning the preamble of each chapter. 
4. Then we simply build the main file by copying all the contents of each chapter into the 
`main.tex` file and number of these chapter using the `\chapter{}` organizational environment.

