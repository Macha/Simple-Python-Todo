<pre>.oOOOo.                     o             
o     o  o                 O              
O.                         o              
 `OOoo.                    O              
      `O O  `oOOoOO. .oOo. o  .oOo.       
       o o   O  o  o O   o O  OooO'       
O.    .O O   o  O  O o   O o  O           
 `oooO'  o'  O  o  o oOoO' Oo `OoO'       
                     O                    
                     o'                   

OooOOo.               o                 
O     `O             O                  
o      O         O   o                  
O     .o        oOo  O                  
oOooOO'  O   o   o   OoOo. .oOo. 'OoOo. 
o        o   O   O   o   o O   o  o   O 
O        O   o   o   o   O o   O  O   o 
o'       `OoOO   `oO O   o `OoO'  o   O 
             o                          
          OoO'                          

oOoOOoOOo  .oOOOo.  o.OOOo.    .oOOOo.  
    o     .O     o.  O    `o  .O     o. 
    o     O       o  o      O O       o 
    O     o       O  O      o o       O 
    o     O       o  o      O O       o 
    O     o       O  O      o o       O 
    O     `o     O'  o    .O' `o     O' 
    o'     `OoooO'   OooOO'    `OoooO'  
                                       </pre>

This is a simple todo manager written in Python. At the moment it is command 
line only, but a GUI version is being created.

Usage
=====
*On Windows, use `python todo.py` wherever you see todo.py in this readme.*

Download
Install using `todo.py install`

Adding Items
-------------
Use `todo.py add <text>`.

Listing Items
-------------
Use `todo.py list`

Removing Items
--------------
Use `todo.py remove <id>`
To get the ID, use `todo.py list`

Usage with multiple lists
==========================
The name of a list must be one word.

Adding Items to a Certain List
------------------------------
Use `todo.py addto <listname> <text>`

Listing Items from a Certain List
----------------------------------
Use `todo.py list <listname>`

Removing Items from a Certain List
-----------------------------------
Use `todo.py removefrom <listname> <id>`
To get the ID, use `todo.py list <listname>`

Creating a New List
--------------------
Use `todo.py create <listname>`

Removing a List
---------------
Use `todo.py delete_list <listname>`
