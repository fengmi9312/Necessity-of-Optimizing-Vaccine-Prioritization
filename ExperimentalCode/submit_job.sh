#!/bin/bash
#SBATCH --job-name=mifeng_job        # Job name
#SBATCH --nodelist=hkbugpusrv[05]
#SBATCH --ntasks=20               # Total number of tasks
#SBATCH --cpus-per-task=1         # Number of CPUs per task


# Run the tasks
expr_name="necs_from_country_35"
task_param="United States"

for ((i=0; i<$SLURM_NTASKS; i++)); do
    srun --ntasks=1 --exclusive --cpus-per-task=$SLURM_CPUS_PER_TASK --nodes=1 python main.py $i $SLURM_NTASKS "$expr_name" "$task_param" &
done

wait