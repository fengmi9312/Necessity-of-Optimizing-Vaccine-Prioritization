# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:55:46 2026

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt



def make_age_dist(
    idx: int,
    n: int,
    n_group: int,
    sigma_rel: float = 0.15,
) -> np.ndarray:
    """
    Generate an age distribution.

    idx = 0      -> concentrated in young age groups
    idx = n - 1  -> concentrated in old age groups

    sigma_rel controls relative spread on [0, 1].
    """
    if not 0 <= idx < n:
        raise ValueError("idx must be in range(n)")
    if n <= 1:
        raise ValueError("n must be greater than 1")
    if n_group <= 1:
        raise ValueError("n_group must be greater than 1")
    if sigma_rel <= 0:
        raise ValueError("sigma_rel must be positive")

    age_pos = np.linspace(0, 1, n_group)
    center = idx / (n - 1)

    weights = np.exp(-0.5 * ((age_pos - center) / sigma_rel) ** 2)
    age_dist = weights / weights.sum()

    return age_dist



def plot_age_dist_bar_5x8(
    n: int = 40,
    n_group: int = 8,
    sigma_rel: float = 0.15,
):
    x = np.arange(n_group)

    fig, axes = plt.subplots(
        nrows=5,
        ncols=8,
        figsize=(20, 10),
        sharex=True,
        sharey=True,
    )

    axes = axes.flatten()

    all_dists = [
        make_age_dist(idx=idx, n=n, n_group=n_group, sigma_rel=sigma_rel)
        for idx in range(n)
    ]

    ylim_max = max(dist.max() for dist in all_dists) * 1.15

    for idx, ax in enumerate(axes):
        age_dist = all_dists[idx]

        ax.bar(x, age_dist)
        ax.set_title(f"idx={idx}", fontsize=9)
        ax.set_ylim(0, ylim_max)
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        if idx % 8 == 0:
            ax.set_ylabel("Prop.")

        if idx >= 32:
            ax.set_xlabel("Age")
            ax.set_xticks(x)

    fig.suptitle(
        f"Age distributions, n={n}, n_group={n_group}, sigma_rel={sigma_rel}",
        fontsize=16,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    return fig, axes


fig, axes = plot_age_dist_bar_5x8(
    n=40,
    n_group=16,
    sigma_rel=0.75,
)

plt.show()