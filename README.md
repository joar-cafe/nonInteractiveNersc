# nonInteractiveNersc
running in NERSC non interactively.

If one tries to run treecorr (tc) under desc-x kernel in cori, a messy error pops up. So, Joe Z, kindly suggested us to use a docker image of txPipe he built. To use this image it is mandatory to pull it with shifter

       shifterimg pull joezuntz/txpipe
   
this needs to be run only once, that's why it's not in the bash file. Once pulled joe's image we can use it with srun and shifter as

     srun -n 4 -c 8 shifter --env OMP_NUM_THREAD=8 --image=joezuntz/txpipe python my_program.py

or put it inside a bash file as done with haswell.sh.

** here are some quick notes of docker/shifter to customize images https://confluence.slac.stanford.edu/pages/viewpage.action?pageId=271587499
