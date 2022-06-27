#!/bin/bash

# python lasso_main_slurm.py -m GeneLasso -hp 0.00001 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 37 -r 03:50:00 # 3
# python lasso_main_slurm.py -m GeneLasso -hp 0.0001 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 0.001 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 0.01 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 0.1 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 1 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 10 -trnd Microarray -tstd Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00

# python lasso_main_slurm.py -m GeneLasso -hp 0.00001 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 2 -r 03:50:00 # 34 still need to run
# python lasso_main_slurm.py -m GeneLasso -hp 0.0001 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 10 -r 03:50:00 # 31
# python lasso_main_slurm.py -m GeneLasso -hp 0.001 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 37 -r 03:50:00 # 13
# python lasso_main_slurm.py -m GeneLasso -hp 0.01 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 37 -r 03:50:00 # 3
# python lasso_main_slurm.py -m GeneLasso -hp 0.1 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 1 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 10 -trnd Microarray -tstd Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done

# python lasso_main_slurm.py -m GeneLasso -hp 0.000001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 75 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 0.00001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 0.0001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 0.001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 0.01 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 0.1 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 1 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00
# python lasso_main_slurm.py -m GeneLasso -hp 10 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs LINCS -b no  -mem 100G -nm 150 -r 03:50:00

# python lasso_main_slurm.py -m GeneLasso -hp 0.00001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 3 -r 03:50:00 # 34 still need to run
# python lasso_main_slurm.py -m GeneLasso -hp 0.0001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 10 -r 03:50:00 # 31
# python lasso_main_slurm.py -m GeneLasso -hp 0.001 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 37 -r 03:50:00 # 19
# python lasso_main_slurm.py -m GeneLasso -hp 0.01 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 0.1 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 1 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done
# python lasso_main_slurm.py -m GeneLasso -hp 10 -trnd RNAseq -tstd RNAseq-Microarray -s Val -gs GPL96-570 -b no  -mem 100G -nm 150 -r 03:50:00 # done
