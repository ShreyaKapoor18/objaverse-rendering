#!/bin/bash -l
#
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=3
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --partition=a40
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/test_distribution_load_slurm.%j.out


unset SLURM_EXPORT_ENV

module load git
conda init
conda activate pyobjaverse
for i in {0..4}
do
    srun ~/blender/blender-3.3.1-linux-x64/blender -b -P ~/git/objaverse-rendering/scripts_custom/test_distribution_load_cluster.py --\
    --filename list_lvis_$i.txt --output_filename ~/git/objaverse-rendering/count_lvis_$i.npy
    sleep 200
done
wait # in order to keep all the background processes in check!
# these processes in check are all correct