# File-encryption-py
A program to encrypt files

This program encrypts files using a key given by the user

File encryption is an interesting topic. This program uses a file that can be of any type and converts it into a ".menc" file. From there the original file is only restorable if you have the program and the key.
menc.py is the first version which features only one bitmask but on the other hand you get a nice looking progessbar.
menc3.py is the newest version which features two bitmasks but no progessbar.

You have to call the compiled programm from the terminal, like so: python menc.py -e file.txt UhKDcdF

The layout of the input is this: menc.py [-e/-d] <file> <key>

Use -e to encrypt and -d to decrypt. Of course the same key has to be used to decrypt, that was used to encrypt the file.

The filename extension ".menc" comes from: M(atteo)enc(ryption). :)
