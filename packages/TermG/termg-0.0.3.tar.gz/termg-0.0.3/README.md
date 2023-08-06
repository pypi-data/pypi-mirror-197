# TermG

With TermG you can easily build graphical applications in the terminal!

Simply install TermG

`pip install TermG`


And then you can use it in your projects!

How to create a project with TermG?
First import TermG

`from TermG import termg as tg`


Then create the Screen

`sc = tg.Screen(width, height) # width = columns, height = rows`


Fill the screen with a specific color

`sc.fill( tg.Color(127) )`


And blit your Screen to the terminal

`sc.blit()`
