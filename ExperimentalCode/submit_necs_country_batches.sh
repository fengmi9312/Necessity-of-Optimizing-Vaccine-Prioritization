#!/bin/bash

set -Eeuo pipefail

script="${1:?Usage: $0 <sbatch_script> [batch_size] [max_running_per_batch]}"
batch_size="${2:-10}"
max_running="${3:-5}"
total_tasks=400

if [[ ! -f "$script" ]]; then
    echo "Batch script does not exist: $script" >&2
    exit 1
fi

for ((start=0; start<total_tasks; start+=batch_size)); do
    end=$((start + batch_size - 1))
    if (( end >= total_tasks )); then
        end=$((total_tasks - 1))
    fi

    echo "Submitting ${script}: array ${start}-${end}%${max_running}"
    job_id=$(sbatch --parsable --array="${start}-${end}%${max_running}" "$script")
    job_id="${job_id%%_*}"
    echo "Submitted job ${job_id}"

    while squeue -h -j "$job_id" | grep -q .; do
        sleep 60
    done

    echo "Job ${job_id} finished"
done

echo "All batches submitted and finished for ${script}"
