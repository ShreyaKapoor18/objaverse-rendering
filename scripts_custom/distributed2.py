import glob
import json
import multiprocessing
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

import boto3
import tyro
import wandb
from os.path import join

@dataclass
class Args:
    workers_per_gpu: int
    """number of workers per gpu"""

    input_models_path: str
    """Path to a json file containing a list of 3D object files"""

    upload_to_s3: bool = False
    """Whether to upload the rendered images to S3"""

    log_to_wandb: bool = False
    """Whether to log the progress to wandb"""

    num_gpus: int = -1
    """number of gpus to use. -1 means all available gpus"""
    
    output_dir: str
    """ The output directory to which we wanna write the renderings"""
    
    engine : str
    """ Which engine to use"""
    
    num_images: str
    """ Number of images"""
    
    camera_dist: str
    """ Camera distance for the renderer"""
    
    textures: bool
    """ If the renderings shall include textures or not"""
    
    script: str
    """ Which script to use"""


def worker(
    queue: multiprocessing.JoinableQueue,
    count: multiprocessing.Value,
    gpu: int,
    s3: Optional[boto3.client],
) -> None:
    while True:
        item = queue.get()
        if item is None:
            break

        # Perform some operation on the item
        print(item, gpu)
        command = (
            f"~/blender/blender-3.3.1-linux-x64/blender -b -P {args.script} --"
            f" --object_path {item}"
            f" --output_dir  {args.output_dir}" 
            f" --engine {args.engine}"
            f" --num_images {args.num_images}"
            f" --camera_dist {args.camera_dist}")
        if args.texture:
            command += f"--textures"
        subprocess.run(command, shell=True)
        # quit opening blender for each turn
        # after the object has been rendered then delete it, since we want to save the sample on the computer
        # this has already been ensured by the tmp objects folder
	

        with count.get_lock():
            count.value += 1

        queue.task_done()


if __name__ == "__main__":
    args = tyro.cli(Args)

    s3 = boto3.client("s3") if args.upload_to_s3 else None
    queue = multiprocessing.JoinableQueue()
    count = multiprocessing.Value("i", 0)

    if args.log_to_wandb:
        wandb.init(project="objaverse-rendering", entity="prior-ai2")

    # Start worker processes on each of the GPUs
    for gpu_i in range(args.num_gpus):
        # HOw does it find the gpu
        print('Entering the gpus loop')
        for worker_i in range(args.workers_per_gpu):
            worker_i = gpu_i * args.workers_per_gpu + worker_i
            process = multiprocessing.Process(
                target=worker, args=(queue, count, gpu_i, s3)
            )
            process.daemon = True
            process.start()

    # Add items to the queue
    with open(args.input_models_path, "r") as f:
        model_paths = json.load(f)
    for item in model_paths:
        queue.put(item)

    # update the wandb count
    if args.log_to_wandb:
        while True:
            time.sleep(5)
            wandb.log(
                {
                    "count": count.value,
                    "total": len(model_paths),
                    "progress": count.value / len(model_paths),
                }
            )
            if count.value == len(model_paths):
                break

    # Wait for all tasks to be completed
    queue.join()

    # Add sentinels to the queue to stop the worker processes
    for i in range(args.num_gpus * args.workers_per_gpu):
        queue.put(None)
