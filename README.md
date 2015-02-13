# 3oboco.py
target: be able to optimize copy through networking or inside a computer by using multithreading or multiprocess copy.
usage 
3oboco.py sourcefile    destinationfile
 

I tried to wonder how is robocopy utiliy sometimes so fast...it's really faster when using multithreading copy.
But how is that possible? I don't have idea.
I tried in a very raw way to split the process in different way, and every time it was slower than normal
cp or dd.
In the standard way i use the multiprocessing functionalities of python and run on every process a dd of a mb.
It was indeed the faster experiment. Nearly 1.6 times slower than normal copy.

Instead to test the second interesting but yet slow...dammed slow experiment, you should comment line 88 and uncomment
lines 82, 83 and 87. I call multiple times split unix command(up to 32 depending on the size of the file to copy)
and then....wait a second, not then, but in parallel, as soon as the splits procecess ends, we start to move those
to destination.

Todo: nothing....:) i see it very hard to find a way to reach the target, but If you have some idea it would be really great, lets make some experiments, i would really appreciate
