#!/bin/bash
#SBATCH --job-name=necs_populations
#SBATCH --partition=v6_384
#SBATCH --nodes=1
#SBATCH --ntasks=80
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=24:00:00
#SBATCH --array=0-19%20
#SBATCH --output=necs_populations_%A_%a.out
#SBATCH --error=necs_populations_%A_%a.err

set -Eeuo pipefail

trap 'echo "[ERROR] line=$LINENO exit_code=$?" >&2' ERR

echo "===== SLURM INFO ====="
echo "SLURM_JOB_ID=${SLURM_JOB_ID:-NA}"
echo "SLURM_ARRAY_JOB_ID=${SLURM_ARRAY_JOB_ID:-NA}"
echo "SLURM_ARRAY_TASK_ID=${SLURM_ARRAY_TASK_ID:-NA}"
echo "SLURM_SUBMIT_DIR=${SLURM_SUBMIT_DIR:-NA}"
echo "SLURM_NTASKS=${SLURM_NTASKS:-NA}"
echo "SLURM_CPUS_PER_TASK=${SLURM_CPUS_PER_TASK:-NA}"
echo "SLURM_JOB_NODELIST=${SLURM_JOB_NODELIST:-NA}"
echo "hostname=$(hostname)"
echo "date=$(date)"

script_dir="$SLURM_SUBMIT_DIR"
cd "$script_dir"

echo "===== PYTHON INFO ====="
source /public1/soft/modules/module.sh
module load miniforge/24.11
source /public1/soft/miniforge/24.11/etc/profile.d/conda.sh
conda activate "$HOME/.miniforge_venvs/necessity"

which python
python --version

expr_name="necs_from_populations"
task_param="param"
total_files=1600
files_per_group=40
groups_per_array_task=2
first_group_id=$((SLURM_ARRAY_TASK_ID * groups_per_array_task))
last_group_id=$((first_group_id + groups_per_array_task - 1))

log_root="$script_dir/populations_logs"
if [[ ! -d "$log_root" ]]; then
    echo "[ERROR] log root does not exist: $log_root" >&2
    echo "Create it first with: mkdir -p \"$log_root\"" >&2
    exit 1
fi
log_dir="${log_root}/${expr_name}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
mkdir -p "$log_dir"

echo "===== TASK INFO ====="
echo "script_dir=$script_dir"
echo "log_root=$log_root"
echo "expr_name=$expr_name"
echo "task_param=$task_param"
echo "total_files=$total_files"
echo "files_per_group=$files_per_group"
echo "groups_per_array_task=$groups_per_array_task"
echo "first_group_id=$first_group_id"
echo "last_group_id=$last_group_id"
echo "log_dir=$log_dir"

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

echo "===== RUN POPULATIONS ====="
pids=()
failed=0

for ((group_id=first_group_id; group_id<=last_group_id; group_id++)); do
    for ((within_group_idx=0; within_group_idx<files_per_group; within_group_idx++)); do
        file_idx=$((group_id * files_per_group + within_group_idx))
        echo "launch group_id=$group_id within_group_idx=$within_group_idx file_idx=$file_idx"
        srun --ntasks=1 --exclusive --cpus-per-task="$SLURM_CPUS_PER_TASK" --nodes=1 \
            python -u main.py "$file_idx" "$total_files" "$expr_name" "$task_param" \
            > "${log_dir}/file_${file_idx}.out" \
            2> "${log_dir}/file_${file_idx}.err" &
        pids+=("$!")
    done
done

for pid in "${pids[@]}"; do
    if ! wait "$pid"; then
        echo "[ERROR] child process pid=${pid} failed; see ${log_dir}" >&2
        failed=1
    fi
done

if (( failed )); then
    exit 1
fi

echo "===== DONE ====="
echo "end=$(date)"
