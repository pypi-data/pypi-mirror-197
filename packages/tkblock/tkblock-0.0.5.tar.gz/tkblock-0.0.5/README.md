# tkblock  
tkblock is a library to support easy placement of tkinter widgets.  
The method of placing widgets uses the old HTML/CSS idea of table layout.    


## Why we made it.
tkinter has three functions for placing widgets: place, grid, and pack.  
However, if you are not familiar with tkinter, it is difficult to distinguish between these three functions.  
At first, you may wonder which function to use for placement.  
I have often heard that after struggling with this problem, while checking the functions, they often fail to place them according to the UI diagram they have designed.  
Also, it was troublesome to install Windows Form and other software on my PC, and I could not use C# at my work place.
So, I decided to create a simple GUI application in python without worrying about OS or environment such as windows or linux.
As a result, I created a library that allows you to place widgets without having to be aware of the functions to be placed in tkinter.  


## how to use
I will explain how to use the library.  


### Installing the library.

```bash
pip install tkblock
```
Install the library with.    

### Import the library and tkinter.

First, import the library.  
```python
import tkinter as tk
from tkinter import ttk
from tkblock.block_service import BlockService
```


### Creating the root window.

Create the root window using the imported library.  
When the root window is created, we specify the title, table width and height, and number of rows and columns.  
Next, place the widget by specifying its number of rows and columns when generating the widget.  

```python
root = BlockService.init("test", 10, 20, 600, 400)
```

The title of the application to be created by tkinter is "test".  
10 columns  
20 for the number of rows  
Width is 600  
Height is 400  

<img width="451" alt="readme_root" src="https://user-images.githubusercontent.com/78261582/223762154-a69ff349-c047-4793-a3aa-108bb21b03fe.png">

This figure shows the root window created by the above code.  

Note that you need to execute the written code to make root loop.  
```python
root.mainloop()
```

### Create a dedicated Frame.

Create a dedicated Frame on top of the root window for easy placement of the widget.  
```python
frame = BlockService.create_frame("main")
```

There are six arguments, but the only one that must be specified is the name of the Frame to be created.  
In this example, the frame name is "main".  
The optional arguments are as follows.  
+ col: The number of columns in the frame. If not specified, it is the number of columns in the destination window. In this case, 10.  
+ row: The number of rows in the frame. If not specified, it is the number of rows of the destination window. In this case, 20.  
+ width: The width of the frame. If not specified, it is the width of the destination window. In this case, 600  
+ height: The height of the frame. If not specified, it is the height of the destination window. In this case, it is 400  
+ root: The window where the frame will be placed. If not specified, the placement destination is the root window. In this case, the root window.  

By the way, to make it easier to see the table layout during development, a canvas is created internally to draw auxiliary lines.  
```python
BlockService.place_frame_widget()
BlockService.create_auxiliary_line()
```
You can draw an auxiliary line by executing the above code.  

``BlockService.place_frame_widget()``  
is explained in the next section.  

<img width="451" alt="readme_frame" src="https://user-images.githubusercontent.com/78261582/223762159-000cbd81-562e-4014-a8cf-8fa8a6d9d443.png">  

The Frame shown in this figure is the base for placing the widget.  

### Place the widget.

This time, we will place the simplest label.  

<img width="451" alt="readme_frame_add_layout" src="https://user-images.githubusercontent.com/78261582/223762161-b42a8cfc-11a5-4561-a883-4b641364d0b6.png">  

Suppose we want to place a label here.  
To do so, we specify the coordinates as follows.  
```python
label = ttk.Label(frame, text="how to use", anchor=tk.CENTER)
label.layout = BlockService.layout(3, 6, 2, 4)
```
The above code will create a "Widget" in the middle of the  
Place a label in a frame with the text "how to use" in the center of the widget.  
The label Widget has an attribute called layout with coordinates.  
The layout can be specified as (column start position, column end position, row start position, row end position).  


This code is then added to the  

```python
BlockService.place_frame_widget()
```
Place it in front of the placed before the  
```python
BlockService.place_frame_widget()
```
place_frame_widget is a function that places all widgets owned by the root widdow.  
Therefore, it must be executed after all widgets have been created and layouts specified.  

<img width="451" alt="readme_frame_label" src="https://user-images.githubusercontent.com/78261582/223762164-25d5f489-3deb-42ea-87ca-ad290635214f.png">  


The label Widget is placed where intended, as shown in the above figure.  

## Finished Code.  

This is the code created so far.  

```python
import tkinter as tk
from tkinter import ttk

from tkblock.block_service import BlockService

root = BlockService.init("test", 10, 20, 600, 400)
frame = BlockService.create_frame("test")
label = ttk.Label(frame, text="how to use", anchor=tk.CENTER)
label.layout = BlockService.layout(3, 6, 2, 4)
BlockService.place_frame_widget()
BlockService.create_auxiliary_line()
root.mainloop()
```

BlockService's in the tkblock library.  
+ init  
+ create_frame  
+ layout  
+ place_frame_widget  
You can easily use tkinter Widget just by using.  

# Summary.  
In this article, we created a library called tkblock for easy placement of tkinter Widget.  
I published it in the hope that it will help people who need to create GUI apps in python and are stumped by widget placement and other issues.  
If you are making a full-fledged app, I would suggest not using this.  
I am thinking of using this because I think it would be useful to have a little app in support of my business.  
(I am just concerned that I have not been able to do much testing...)  

Also, there are other details and uses not described in this article.  
For example, placing a standard frame on top of a dedicated frame on top of a dedicated frame, etc., etc.  

Well, thank you for viewing this far.  