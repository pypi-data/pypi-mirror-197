# Jetsam
- True daemonizer using native C calls  
- Currently only compatible with `*nix` file systems 
- <u>Extra Paranoid Edition</u> uses that **double fork magic!** 
> jetsam definition: floating debris ejected from a ship 

## C Extension 
To showcase a C library being used as a _native python module_

## Example 
```python
from jetsam import daemon
import time
import logging

@daemon
def stuff():
    logging.basicConfig(
        filename="logfile", 
        level=logging.DEBUG, 
        filemode="w"
    )
    while True:  # to simulate long running proc
        time.sleep(1)
        logging.debug("I am running headless!")

stuff()
print("stuff() returns immediately and is daemonized")
```
