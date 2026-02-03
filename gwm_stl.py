"""Simple SynthSeg label-map -> STL (defaults to left/right white+gray matter).

Defaults assume SynthSeg label-map output with FreeSurfer-style labels:
- 3  = left cerebral cortex (gray)
- 42 = right cerebral cortex (gray)

Example:
    python gm_stl.py --nii "C:\path\to\seg.nii"

This writes two files next to the input NIfTI:
    seg_left.stl  (left white+gray matter)
    seg_right.stl (right white+gray matter)

Resampling note:
- By default we do NOT resample (downsample factor = 1).
- If you want a smoother / less detailed STL, use --downsample 2 (or 3).
    This reduces voxel resolution before marching cubes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np


def load_nifti(path: str | Path) -> tuple[np.ndarray, tuple[float, float, float]]:
    """Load NIfTI volume and return (data, voxel_sizes_mm)."""
    import nibabel as nib

    nii = nib.load(str(path))
    data = np.asanyarray(nii.dataobj)  # keeps integer labels for label maps
    zooms = nii.header.get_zooms()[:3]
    voxel_sizes = (float(zooms[0]), float(zooms[1]), float(zooms[2]))
    return data, voxel_sizes


def make_label_mask(data: np.ndarray, labels: Sequence[int]) -> np.ndarray:
    """Create a boolean mask for the given label values."""
    return np.isin(data, np.asarray(labels, dtype=data.dtype))


def nifti_base_name(path: str | Path) -> str:
    """Return base name without .nii/.nii.gz suffix."""
    p = Path(path)
    name = p.name
    if name.lower().endswith(".nii.gz"):
        return name[:-7]
    if name.lower().endswith(".nii"):
        return name[:-4]
    return p.stem


def keep_largest_component(mask: np.ndarray) -> np.ndarray:
    """Remove small disconnected islands by keeping only the biggest component."""
    from skimage.measure import label as cc_label

    lab = cc_label(mask.astype(bool), connectivity=1)
    if lab.max() == 0:
        return mask.astype(bool)
    counts = np.bincount(lab.ravel())
    counts[0] = 0
    return lab == int(counts.argmax())


def downsample_nearest(mask: np.ndarray, factor: int) -> np.ndarray:
    """Downsample a binary mask by striding.

    factor=2 keeps every 2nd voxel along each axis.
    This tends to smooth small folds/details (and makes a smaller STL).
    """
    if factor <= 1:
        return mask.astype(bool)
    return mask[::factor, ::factor, ::factor].astype(bool)


def mask_to_stl(
    mask: np.ndarray,
    voxel_sizes_mm: tuple[float, float, float],
    out_path: str | Path,
    smooth_iters: int,
    scale_factor: float,
):
    """Convert mask to STL using marching cubes."""
    from skimage import measure
    import trimesh

    verts, faces, _, _ = measure.marching_cubes(
        mask.astype(np.uint8),
        level=0.5,
        spacing=voxel_sizes_mm,
        allow_degenerate=False,
    )

    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=True)

    if smooth_iters and smooth_iters > 0:
        try:
            trimesh.smoothing.filter_humphrey(mesh, iterations=int(smooth_iters))
        except Exception:
            # If smoothing isn't available in this trimesh build, keep the raw mesh.
            pass

    if scale_factor and float(scale_factor) != 1.0:
        mesh.apply_scale(float(scale_factor))

    mesh.export(str(out_path))


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(
        description="Convert a SynthSeg label map to an STL."
    )
    p.add_argument("--nii", required=True, help="Input SynthSeg segmentation (.nii/.nii.gz)")
    p.add_argument(
        "--left-labels",
        nargs="+",
        type=int,
        default=[2, 3],
        help="Labels for LEFT STL (default: 2 3 = left WM + left cortex)",
    )
    p.add_argument(
        "--right-labels",
        nargs="+",
        type=int,
        default=[41, 42],
        help="Labels for RIGHT STL (default: 41 42 = right WM + right cortex)",
    )
    p.add_argument(
        "--downsample",
        type=int,
        default=1,
        help="Downsample factor (default: 1). Use 2 or 3 for smoother/less-detailed STL.",
    )
    p.add_argument(
        "--scale",
        type=float,
        default=0.125,
        help="Scale factor applied to the exported STL geometry (default: 0.125)",
    )
    p.add_argument("--smooth-iters", type=int, default=25, help="Smoothing iterations (default: 25)")
    p.add_argument("--keep-largest", action="store_true", help="Keep only largest connected component")
    p.add_argument("--no-keep-largest", action="store_true", help="Do not remove small islands")

    args = p.parse_args()

    keep_largest = True
    if args.no_keep_largest:
        keep_largest = False
    if args.keep_largest:
        keep_largest = True

    data, voxel_sizes = load_nifti(args.nii)
    left_mask = make_label_mask(data, args.left_labels)
    right_mask = make_label_mask(data, args.right_labels)

    if args.downsample > 1:
        # Smoother / less detailed / smaller STL
        left_mask = downsample_nearest(left_mask, int(args.downsample))
        right_mask = downsample_nearest(right_mask, int(args.downsample))
        voxel_sizes = tuple(v * float(args.downsample) for v in voxel_sizes)

    if keep_largest:
        left_mask = keep_largest_component(left_mask)
        right_mask = keep_largest_component(right_mask)

    in_path = Path(args.nii)
    out_dir = in_path.parent
    base = nifti_base_name(in_path)
    out_left = out_dir / f"{base}_left.stl"
    out_right = out_dir / f"{base}_right.stl"
    out_dir.mkdir(parents=True, exist_ok=True)

    mask_to_stl(left_mask, voxel_sizes, out_left, smooth_iters=args.smooth_iters, scale_factor=args.scale)
    print(f"Wrote: {out_left}")
    mask_to_stl(right_mask, voxel_sizes, out_right, smooth_iters=args.smooth_iters, scale_factor=args.scale)
    print(f"Wrote: {out_right}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
