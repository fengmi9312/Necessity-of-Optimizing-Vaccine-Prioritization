#!/bin/bash
#SBATCH --job-name=necs35_pack
#SBATCH --partition=v6_384
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=24:00:00
#SBATCH --output=necs_country_35_packed_%j.out
#SBATCH --error=necs_country_35_packed_%j.err

set -Eeuo pipefail

trap 'echo "[ERROR] line=$LINENO exit_code=$?" >&2' ERR

echo "===== SLURM INFO ====="
echo "SLURM_JOB_ID=${SLURM_JOB_ID:-NA}"
echo "SLURM_SUBMIT_DIR=${SLURM_SUBMIT_DIR:-NA}"
echo "SLURM_NTASKS=${SLURM_NTASKS:-NA}"
echo "SLURM_CPUS_PER_TASK=${SLURM_CPUS_PER_TASK:-NA}"
echo "SLURM_JOB_NODELIST=${SLURM_JOB_NODELIST:-NA}"
echo "hostname=$(hostname)"
echo "date=$(date)"

cd "$SLURM_SUBMIT_DIR"

echo "===== PYTHON INFO ====="
source /public1/soft/modules/module.sh
module load miniforge/24.11
source /public1/soft/miniforge/24.11/etc/profile.d/conda.sh
conda activate "$HOME/.miniforge_venvs/necessity"

which python
python --version

countries=(
  "United States"
  "United Kingdom"
  "France"
  "Germany"
  "Spain"
  "Japan"
  "Israel"
  "Austria"
  "Ireland"
  "South Korea"
)

expr_name="necs_from_country_35"
n_chunks=40
total_tasks=$((${#countries[@]} * n_chunks))
start_task="${START_TASK:-0}"
end_task="${END_TASK:-$((total_tasks - 1))}"
parallel_tasks="${SLURM_NTASKS:-20}"
log_dir="packed_logs/${expr_name}_${SLURM_JOB_ID}"
mkdir -p "$log_dir"

echo "===== TASK PLAN ====="
echo "expr_name=$expr_name"
echo "n_countries=${#countries[@]}"
echo "n_chunks=$n_chunks"
echo "total_tasks=$total_tasks"
echo "start_task=$start_task"
echo "end_task=$end_task"
echo "parallel_tasks=$parallel_tasks"
echo "log_dir=$log_dir"

for ((wave_start=start_task; wave_start<=end_task; wave_start+=parallel_tasks)); do
    wave_end=$((wave_start + parallel_tasks - 1))
    if (( wave_end > end_task )); then
        wave_end=$end_task
    fi

    echo "===== WAVE ${wave_start}-${wave_end} ====="
    for ((task_id=wave_start; task_id<=wave_end; task_id++)); do
        country_id=$((task_id / n_chunks))
        chunk_id=$((task_id % n_chunks))
        task_param="${countries[$country_id]}"
        safe_country="${task_param// /_}"

        echo "launch task_id=$task_id country=$task_param chunk=$chunk_id"
        srun --ntasks=1 --exclusive --cpus-per-task="$SLURM_CPUS_PER_TASK" --nodes=1 \
            python -u main.py "$chunk_id" "$n_chunks" "$expr_name" "$task_param" \
            > "${log_dir}/task_${task_id}_${safe_country}_${chunk_id}.out" \
            2> "${log_dir}/task_${task_id}_${safe_country}_${chunk_id}.err" &
    done
    wait
    echo "completed wave ${wave_start}-${wave_end} at $(date)"
done

echo "===== DONE ====="
echo "end=$(date)"
