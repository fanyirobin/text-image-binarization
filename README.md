# text-image-binarization
An implementation of the paper 'Efficient illumination compensation techniques for text images'

To use it, all you need to do is put the image file in
the same directory and run the code.

At the beginning, you need to specify the file name and format
For example, a image called "test.jpg"
	FILE_NAME = "test"
	FORMAT = ".jpg"
Note: you don't need to type the quote mark.

The default value for c and bl works well for most of time. 
For any images, test it by using the default value first.

c = 0.4
bl = 260

You can also change the value for the two threshold. Two functions
are implemented to decide the value for threshold. But they do not
perform as well as the experienced value most of time. 

The default threshold for CEI is TH_c = 60
The default threshold for Edge is TH_e = 30

For application reasons, the implementation here is a little bit
different from the paper.

Right now, the last step (Estimate light distribution) takes a long
time. Because this step cannot be optimized using numpy. However,
there must be some other ways to improve the efficiency. I will work
on it later.
