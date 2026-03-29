import base64
import mimetypes
import os
import re


def extract_substitutions(html: str) -> set:
    return set(re.findall(r'\{(\w+)\}', html))


def extract_cids(html: str) -> set:
    return set(re.findall(r'cid:(\w+)', html))


def render_body_with_inline_images(body: str, images: dict, img_dir: str) -> str:
    """Replace cid:X references with base64 data URIs using files from img_dir."""
    result = body
    for cid_name, filename in images.items():
        path = os.path.join(img_dir, filename)
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as f:
            data = f.read()
        mime, _ = mimetypes.guess_type(filename)
        if not mime:
            mime = "application/octet-stream"
        b64 = base64.b64encode(data).decode()
        result = result.replace(f"cid:{cid_name}", f"data:{mime};base64,{b64}")
    return result
