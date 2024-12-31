  /////////////////////////
 /// PYTHON OBFUSCATOR ///
/////////////////////////

Overview:
    Simple python script that modifies another python script, changing:

    [+] Variable names
    [+] Function names

    Once the randomization occurs, the code is then wrapped in BASE-64
    and G-ZIP encoding and saved as an output file.

Note: this script takes into consideration situational variable names, such
    as "k=num" (used in the random.choice module). If said variables were to
    be renamed, it may cause your script to crash. This obfuscator only randomizes
    variable that have been referenced more than once. This is how it determines
    what was user-declared versus a module-dependent static variable declaration.
    Indentation is also left alone to ensure no errors raised upon execution.

Credits: I don't take true credit for this script as 95% was done via ChatGPT.
    As far as the BASE-64/G-ZIP wrapping, that code was mine and originally
    came from my previous python obfuscation script which has now been made
    private and is obsolete.
