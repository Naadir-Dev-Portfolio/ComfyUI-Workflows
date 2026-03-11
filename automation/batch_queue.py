"""
ComfyUI Batch Queue
-------------------
Submits a list of prompts to the ComfyUI API in sequence.
Usage: python batch_queue.py --prompts prompts.txt --output ./output --delay 2
"""

import json
import time
import uuid
import argparse
import requests
from pathlib import Path

COMFY_URL = "http://127.0.0.1:8188"


def load_workflow(workflow_path: str) -> dict:
    with open(workflow_path, "r") as f:
        return json.load(f)


def inject_prompt(workflow: dict, prompt_text: str, seed: int = None) -> dict:
    """Injects a text prompt and optional seed into a workflow graph."""
    wf = json.loads(json.dumps(workflow))  # deep copy
    for node_id, node in wf.items():
        if node.get("class_type") == "CLIPTextEncode":
            if "positive" in str(node.get("_meta", {}).get("title", "")).lower():
                node["inputs"]["text"] = prompt_text
        if node.get("class_type") == "KSampler" and seed is not None:
            node["inputs"]["seed"] = seed
    return wf


def queue_prompt(workflow: dict) -> str:
    """Posts a workflow to the ComfyUI /prompt endpoint. Returns the prompt_id."""
    client_id = str(uuid.uuid4())
    payload = {"prompt": workflow, "client_id": client_id}
    response = requests.post(f"{COMFY_URL}/prompt", json=payload)
    response.raise_for_status()
    return response.json().get("prompt_id", "")


def run_batch(prompts_file: str, workflow_path: str, output_dir: str, delay: int):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    workflow = load_workflow(workflow_path)
    prompts = Path(prompts_file).read_text().strip().splitlines()
    prompts = [p.strip() for p in prompts if p.strip()]

    print(f"Queuing {len(prompts)} prompts...")

    for i, prompt in enumerate(prompts):
        seed = int(time.time()) + i
        wf = inject_prompt(workflow, prompt, seed=seed)
        prompt_id = queue_prompt(wf)
        print(f"[{i+1}/{len(prompts)}] Queued: '{prompt[:60]}...' → ID: {prompt_id}")
        time.sleep(delay)

    print("All prompts queued.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ComfyUI batch queue")
    parser.add_argument("--prompts", default="prompts.txt", help="Text file with one prompt per line")
    parser.add_argument("--workflow", default="../workflows/basic_txt2img.json", help="ComfyUI workflow JSON")
    parser.add_argument("--output", default="./output", help="Output folder")
    parser.add_argument("--delay", type=int, default=2, help="Seconds between submissions")
    args = parser.parse_args()

    run_batch(args.prompts, args.workflow, args.output, args.delay)
