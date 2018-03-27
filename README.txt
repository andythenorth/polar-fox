This project provides a package of common assets which are used in vehicle newgrfs by andythenorth.

*Examples*

- cargos for inclusion in cargo table
- refits by label for different classes of vehicle
- sprites for cargo graphics
- graphics constants
- pixa graphics processing module

Extend as needed.

*Usage*

There is a single script that will assemble the distributed files and copy them to consumers.  This assumes a specific filesystem layout and is not intended to be portable.

	python bin/distribute.py

*Caveats*

1. Not everything is common.  Assets local to the newgrf are preferred, unless they are 100% identical across multiple newgrfs.
2. Eventually this might grow too big and unwieldy.  If it does, split it. 
