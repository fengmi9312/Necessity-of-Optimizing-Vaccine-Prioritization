#!/bin/bash
#SBATCH --job-name=necs35_2country
#SBATCH --partition=v6_384
#SBATCH --nodes=1
#SBATCH --ntasks=80
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=24:00:00
#SBATCH --array=0-4%2
#SBATCH --output=necs_country_35_2country_%A_%a.out
#SBATCH --error=necs_country_35_2country_%A_%a.err

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
pair_id="$SLURM_ARRAY_TASK_ID"
first_country_id=$((pair_id * 2))
log_dir="two_country_logs/${expr_name}_pair_${pair_id}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
mkdir -p "$log_dir"

echo "===== TASK INFO ====="
echo "expr_name=$expr_name"
echo "pair_id=$pair_id"
echo "first_country_id=$first_country_id"
echo "n_chunks=$n_chunks"
echo "log_dir=$log_dir"

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

echo "===== RUN TWO COUNTRIES ====="
pids=()
failed=0

for country_offset in 0 1; do
    country_id=$((first_country_id + country_offset))
    task_param="${countries[$country_id]}"
    safe_country="${task_param// /_}"

    for ((file_idx=0; file_idx<n_chunks; file_idx++)); do
        task_key="${safe_country}_${file_idx}"
        echo "launch country_id=$country_id country=$task_param file_idx=$file_idx"
        srun --ntasks=1 --exclusive --cpus-per-task="$SLURM_CPUS_PER_TASK" --nodes=1 \
            python -u main.py "$file_idx" "$n_chunks" "$expr_name" "$task_param" \
            > "${log_dir}/${task_key}.out" \
            2> "${log_dir}/${task_key}.err" &
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
