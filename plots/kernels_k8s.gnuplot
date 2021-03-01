#!/usr/bin/gnuplot
set terminal postscript color eps enhanced font 22
set output 'kernels_k8s.eps'
set datafile separator " "
set xlabel "Number of MPI Processes"
set xrange [1:16]

# Draw arrows
PROC_PER_NODE = 5
MAX_PROCS = 16
NUM_KERNELS = 9
do for [i = PROC_PER_NODE : MAX_PROCS : PROC_PER_NODE] \
{
    set arrow from i, graph 0 to i, graph 1 nohead dt 3
}

# Routine to print line, very dodgy
get_legend(i) = system("head -1 ../results/kernels_native_k8s_line.dat | \
    cut -c 2- | tr ',' '\n' | sed '".int(i + 1)."q;d'")

# Elapsed time plot
set title "{/Bold Elapsed Time} (".PROC_PER_NODE." procs. per pod)"
set ylabel "Time Elapsed [ms]"
set ytics 40

plot for [i=0:8] '../results/kernels_native_k8s_line.dat' \
       using 1:($2 * 1000) every :::i::i w lp pt 7 title get_legend(i), \
     for [i=0:8] '../results/kernels_native_vms_line.dat' \
       using 1:($2 * 1000) every :::i::i w lp pt 7 dt 2 title get_legend(i) 

!epstopdf 'kernels_k8s.eps'
!rm 'kernels_k8s.eps'
