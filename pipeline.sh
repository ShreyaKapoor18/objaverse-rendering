python3 scripts/download_objaverse.py
python3 scripts/distributed.py --num_gpus 1 --workers_per_gpu 1 --input_models_path input_models_path.json
python3 scripts/assign_to_categories.py
python3 scripts/view_categories.py