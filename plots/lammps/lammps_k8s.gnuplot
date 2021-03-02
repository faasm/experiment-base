#!/usr/bin/gnuplot
set terminal postscript color eps enhanced font 22
set output 'lammps_k8s.eps'
set datafile separator " "
set multiplot layout 2,1
set xlabel "Number of MPI Processes"
set xrange [1:16]

# Draw arrows
PROC_PER_NODE = 5
MAX_PROCS = 16
do for [i = PROC_PER_NODE : MAX_PROCS : PROC_PER_NODE] \
{
    set arrow from i, graph 0 to i, graph 1 nohead dt 3
}

# Elapsed time plot
set title "{/Bold Elapsed Time} (".PROC_PER_NODE." procs. per pod)"
set ylabel "Time Elapsed [s]"
# set yrange [5:60]
set ytics 40
#set yrange [5:15]
cols = int(system('head -1 ../results/lammps_native_k8s.log | wc -w'))
cols_az = int(system('head -1 ../results/lammps_native_az_k8s.log | wc -w'))
plot '../results/lammps_native_k8s.log' \
       using 1:int(cols - 1) w lp pt 7 title 'Vanilla @ u-k8s' ,\
    '' using 1:int(cols - 1):cols w yerrorbars notitle ,\
    '../results/lammps_native_az_k8s.log' \
       using 1:int(cols_az - 1) w lp pt 7 title 'Vanilla @ k8s' ,\
    '' using 1:int(cols_az - 1):cols w yerrorbars notitle

# Speedup
set title "{/Bold Speedup}"
set ylabel "Speedup"
set ytics 4
ref = int(system("head -1 ../results/lammps_native_k8s.log | rev | cut -d' ' -f2 | rev"))
ref_az = int(system("head -1 ../results/lammps_native_az_k8s.log | rev | cut -d' ' -f2 | rev"))
plot '../results/lammps_native_k8s.log' \
        using 1:(ref/$5) w lp pt 7 title 'Vanilla @ u-k8s', \
    '../results/lammps_native_az_k8s.log' using 1:(ref_az/$5) w lp pt 7 \
                                                    title 'Vanilla @ k8s', \
    '../results/lammps_native_vms.log' using 1:(ref_az/$5) w lp pt 7 \
                                                    title 'Vanilla @ VMs', \
    '' using 1:1 w lp lt 2 notitle
    

!epstopdf 'lammps_k8s.eps'
!rm 'lammps_k8s.eps'
