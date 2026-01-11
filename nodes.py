import torch
import numpy as np
from PIL import Image
import os
import folder_paths
import json

class MetadataStripper:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE",),
            "filename_prefix": ("STRING", {"default": "ComfyUI"}),
        }}

    RETURN_NAMES = ()
    RETURN_TYPES = ()

    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "Utilities"

    def save(self, image, filename_prefix="ComfyUI"):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, image[0].shape[1], image[0].shape[0]
        )

        results = list()

        for batch_number, img_tensor in enumerate(image):
            i = 255. * img_tensor.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            file = f"{filename}_{counter:05}_.png"

            img.save(os.path.join(full_output_folder, file), compress_level=4)

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

            counter += 1
        return { "ui": { "images": results } }

NODE_CLASS_MAPPINGS = {
    "MetadataStripper": MetadataStripper,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MetadataStripper": "Metadata Stripper (Save)",
}