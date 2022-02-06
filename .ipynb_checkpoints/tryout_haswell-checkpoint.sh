#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --constraint=haswell
srun -n 2 -c 4 shifter --env OMP_NUM_THREAD=8 --image=joezuntz/txpipe python comparisonWtc.py
