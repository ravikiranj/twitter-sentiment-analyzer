# Special comment lines to the grid engine start
# with #$ and they should contain the command-line arguments for the
# qsub command.  See 'man qsub' for more options.
#
#$ -S /bin/bash
#$ -pe smp 8
#$ -o /home/ravikirn/tmp/$JOB_NAME.$JOB_ID
#$ -j y
#$ -cwd
# The above arguments mean:
#       -S /bin/bash : Run this set of jobs using /bin/bash
#       -tc 8 : Run only at most 8 jobs at a time.  ** Use -tc 100 if you submit more
#       -o : Put the output files in ~/tmp, named by job name and ID, and task ID
#       -j y : Join the error and output files for each job
#       -cwd : Run the job in the Current Working Directory (where the script is)

# The following are among the useful environment variables set when each
# job is run:
#       $SGE_TASK_ID : Which job I am from the above range
#       $SGE_TASK_LAST : Last number from the above range
#               (Equal to the number of tasks if range starts with 1
#                and has a stride of 1.)

python2.6 /home/ravikirn/coursework/data-mining/bass_analyze.py svm
