#!/bin/bash
#SBATCH --job-name=necs_country_70
#SBATCH --partition=v6_384
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=24:00:00
#SBATCH --array=0-399%400
#SBATCH --output=necs_country_70_%A_%a.out
#SBATCH --error=necs_country_70_%A_%a.err

set -Eeuo pipefail

trap 'echo "[ERROR] line=$LINENO exit_code=$?" >&2' ERR

echo "===== SLURM INFO ====="
echo "SLURM_JOB_ID=${SLURM_JOB_ID:-NA}"
echo "SLURM_ARRAY_JOB_ID=${SLURM_ARRAY_JOB_ID:-NA}"
echo "SLURM_ARRAY_TASK_ID=${SLURM_ARRAY_TASK_ID:-NA}"
echo "SLURM_SUBMIT_DIR=${SLURM_SUBMIT_DIR:-NA}"
echo "SLURM_JOB_NODELIST=${SLURM_JOB_NODELIST:-NA}"
echo "hostname=$(hostname)"
echo "date=$(date)"

cd "$SLURM_SUBMIT_DIR"

echo "===== CURRENT DIR ====="
pwd
ls -lh main.py

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

n_chunks=40

country_id=$((SLURM_ARRAY_TASK_ID / n_chunks))
chunk_id=$((SLURM_ARRAY_TASK_ID % n_chunks))

task_param="${countries[$country_id]}"
expr_name="necs_from_country_70"

echo "===== TASK INFO ====="
echo "country_id=$country_id"
echo "chunk_id=$chunk_id"
echo "task_param=$task_param"
echo "expr_name=$expr_name"

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

echo "===== RUN MAIN ====="
python -u main.py "$chunk_id" "$n_chunks" "$expr_name" "$task_param"

echo "===== DONE ====="
echo "end=$(date)"
