### What Is This Repository for ?

This repository is my reading notes of the book by Valliappa Lakshmanan, _Data Science on the Google Cloud Platform_(2018).

This is a book showing a complete work flow of data science, step by step, with the advantage of GCP. I grained much by reading this book and handing-on its code.

Of course, the book has its own github repository, https://github.com/GoogleCloudPlatform/data-science-on-gcp .

When I went through and ran the code on my personal Mac and GCP-project, I got stuck here and there. Yes, I tackled all the problems with the help of GCP documents and Stackoverflow. 

To have a better understanding of the content of the content, and a solid reference based on this book's code. I motivated myself to rewrite/reorganize the code in the clean code style, introduced by the book, _Clean Code: A Handbook of Agile Software Craftsmanship_, of Robert C. Martin.

### Principles of coding 
I cannot say that my code is so clean as the book showed. But I spend much effort to follow the following three principles: 

#### No Comments, Only Codes
When I studied in UiO, many talked like "write comments, code will be more readable", then I got used to write comments. But the Clean Code book claims *"Comments Do Not Make Up for Bad Code"*. It is not easy to git rid of comments. I tried my best to code without comments in this reposirory

#### Complete naming
All classes, functions, variables, arguments are named most clearly as I can. Then readers can understand what the names point to without guessing. 
The trade-off is that the names are longer, even much longer, but without loss of readability. 

#### Single Responsibility
Each function does one job, each class does one job. Then we will create more small functions and classes instead of a few big functions and classes. 
Compared to the initial code of the book _Data Science on the Google Cloud Platform_, code in this repository has more layers of wrapping up because of 
the single responsibility principle. I felt weird to code like this in the beginning. After a while, I was aware of that this is a compulsory step forward 
achieving the great success.

***Up-down Readability***

We all write code and read code line by line up-down. However, not all code has up-down readability. 
It is very often that we have to look back up at some lines to understand what the code is doing. That says _up-down-up-down-up..._ is not a unusual way we read code.
If the code is clean enough, readers can understand it with only up-down reading, no backward scrolling. 


##### There finds individual README in each chapter, as a mini handbook to implement the code, and see the expected results.  

*To be clear, there are not any initial ideas or contents in this tutorial. All work has been done can be found in the book of Mr. Lakshmanan.*