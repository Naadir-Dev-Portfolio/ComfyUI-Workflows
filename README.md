# ComfyUI-Workflows

A growing collection of [ComfyUI](https://github.com/comfyanonymous/ComfyUI) workflows and Python automation scripts for AI image generation pipelines.

ComfyUI is a node-based interface for Stable Diffusion — workflows are fully modular, reproducible JSON graphs that chain models, samplers, LoRAs, upscalers, and post-processing together.

---

## What's in here

| Folder | Contents |
|--------|----------|
| `workflows/` | Exported ComfyUI workflow JSON files — load directly into ComfyUI |
| `automation/` | Python scripts for batch processing, queue automation, and API integration |

---

## Workflows

### `workflows/basic_txt2img.json`
Standard text-to-image pipeline — SDXL base, KSampler, VAE decode. Starting point for all custom builds.

### `workflows/img2img_upscale.json`
Image-to-image with 4x upscale via ESRGAN. Designed for high-res output from low-res sketches or references.

---

## Automation Scripts

### `automation/batch_queue.py`
Submits multiple prompts to the ComfyUI API (`/prompt` endpoint) in sequence, with configurable delay and output folder organisation.

```python
python batch_queue.py --prompts prompts.txt --output ./output --delay 2
```

### `automation/watch_and_rename.py`
Watches the ComfyUI output folder, auto-renames generated images from the cryptic default UUID filenames to a readable `YYYYMMDD_prompt_seed.png` format.

---

## Setup

1. Install and run [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
2. Load any `.json` from `workflows/` via ComfyUI's **Load** button
3. For automation scripts: `pip install requests watchdog`

---

## Tech

- **ComfyUI** — node-based Stable Diffusion UI
- **Python** — batch queue and file automation via the ComfyUI REST API
- **Models used** — SDXL, ESRGAN 4x, custom LoRAs (not included)

---

## Author

**Naadir** · [Portfolio](https://naadir-dev-portfolio.github.io) · [GitHub](https://github.com/Naadir-Dev-Portfolio)
