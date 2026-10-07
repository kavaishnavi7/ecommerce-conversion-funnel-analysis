from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "funnel_analysis_data.csv"
OUTPUT_PATH = PROJECT_DIR / "visualizations" / "ecommerce_funnel_dashboard.png"
FUNNEL_STAGES = ["Browse", "Add to Cart", "Checkout", "Purchase"]


def main():
    data = pd.read_csv(DATA_PATH)
    required_columns = {"Session_ID", "Event", "Device"}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    stage_counts = (
        data.groupby("Event")["Session_ID"]
        .nunique()
        .reindex(FUNNEL_STAGES, fill_value=0)
    )
    if (stage_counts == 0).any():
        missing_stages = stage_counts[stage_counts == 0].index.tolist()
        raise ValueError(f"Dataset has no sessions for funnel stages: {missing_stages}")

    stage_values = stage_counts.to_numpy(dtype=int)
    overall_conversion = stage_values[-1] / stage_values[0] * 100
    stage_conversion = stage_values[1:] / stage_values[:-1] * 100
    drop_off_counts = stage_values[:-1] - stage_values[1:]
    drop_off_rates = drop_off_counts / stage_values[:-1] * 100

    device_funnel = data.pivot_table(
        index="Device",
        columns="Event",
        values="Session_ID",
        aggfunc="nunique",
        fill_value=0,
    )
    device_funnel = device_funnel.reindex(columns=FUNNEL_STAGES, fill_value=0)
    device_funnel = device_funnel.loc[device_funnel["Browse"] > 0]
    device_funnel["Conversion"] = (
        device_funnel["Purchase"] / device_funnel["Browse"] * 100
    )
    device_funnel = device_funnel.sort_values("Conversion", ascending=True)

    sns.set_theme(style="whitegrid", font="DejaVu Sans")
    navy = "#17324D"
    blue = "#3B82A0"
    teal = "#13A89E"
    gold = "#E7A83E"
    coral = "#D96C5F"
    ink = "#243447"
    muted = "#66788A"
    light = "#F3F6F9"
    stage_colors = [navy, blue, teal, gold]

    fig = plt.figure(figsize=(16, 11), facecolor=light)
    grid = fig.add_gridspec(
        nrows=4,
        ncols=2,
        height_ratios=[0.52, 1.0, 3.1, 2.6],
        width_ratios=[1.12, 1.0],
        left=0.055,
        right=0.97,
        top=0.95,
        bottom=0.09,
        hspace=0.4,
        wspace=0.34,
    )

    title_ax = fig.add_subplot(grid[0, :])
    title_ax.axis("off")
    title_ax.text(
        0,
        0.78,
        "E-commerce Conversion Funnel",
        fontsize=24,
        fontweight="bold",
        color=navy,
        transform=title_ax.transAxes,
    )
    title_ax.text(
        0,
        0.18,
        "Session progression, conversion efficiency, and device performance",
        fontsize=11,
        color=muted,
        transform=title_ax.transAxes,
    )

    kpi_grid = grid[1, :].subgridspec(1, 5, wspace=0.1)
    kpis = [
        ("BROWSE / VISITORS", f"{stage_values[0]:,}", blue),
        ("ADD TO CART", f"{stage_values[1]:,}", teal),
        ("CHECKOUT", f"{stage_values[2]:,}", gold),
        ("PURCHASES", f"{stage_values[3]:,}", coral),
        ("OVERALL CONVERSION", f"{overall_conversion:.2f}%", navy),
    ]
    for position, (label, value, color) in enumerate(kpis):
        ax = fig.add_subplot(kpi_grid[0, position])
        ax.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_color("#E1E8EF")
            spine.set_linewidth(0.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(
            0.08,
            0.73,
            label,
            transform=ax.transAxes,
            fontsize=8.5,
            fontweight="bold",
            color=muted,
            va="center",
        )
        ax.text(
            0.08,
            0.31,
            value,
            transform=ax.transAxes,
            fontsize=21,
            fontweight="bold",
            color=color,
            va="center",
        )

    funnel_ax = fig.add_subplot(grid[2, 0])
    funnel_ax.set_facecolor("white")
    funnel_ax.set_title("Funnel volume", loc="left", fontsize=14, fontweight="bold", color=navy, pad=14)
    y_positions = np.arange(len(FUNNEL_STAGES))
    widths = stage_values / stage_values[0]
    left_edges = (1 - widths) / 2
    for y, width, left_edge, color in zip(y_positions, widths, left_edges, stage_colors):
        funnel_ax.barh(y, width, left=left_edge, height=0.58, color=color, zorder=3)
        funnel_ax.text(
            1.04,
            y,
            f"{stage_values[y]:,}  |  {stage_values[y] / stage_values[0] * 100:.2f}%",
            ha="left",
            va="center",
            color=ink,
            fontsize=9.5,
            fontweight="bold",
            clip_on=False,
        )
    funnel_ax.set_xlim(0, 1.42)
    funnel_ax.set_ylim(len(FUNNEL_STAGES) - 0.5, -0.5)
    funnel_ax.set_yticks(y_positions, FUNNEL_STAGES)
    funnel_ax.set_xticks([])
    funnel_ax.tick_params(axis="y", labelsize=9, colors=ink, length=0, pad=8)
    funnel_ax.set_xlabel("Session count  |  share of Browse (%)", color=muted, labelpad=10)
    funnel_ax.grid(False)
    sns.despine(ax=funnel_ax, left=True, bottom=True)

    conversion_ax = fig.add_subplot(grid[2, 1])
    conversion_ax.set_facecolor("white")
    conversion_ax.set_title(
        "Stage-to-stage conversion", loc="left", fontsize=14, fontweight="bold", color=navy, pad=14
    )
    transitions = [
        "Browse → Cart",
        "Add to Cart → Checkout",
        "Checkout → Purchase",
    ]
    conv_y = np.arange(len(transitions))
    bars = conversion_ax.barh(
        conv_y,
        stage_conversion,
        color=[blue, teal, gold],
        height=0.55,
        zorder=3,
    )
    conversion_ax.set_yticks(conv_y, transitions)
    conversion_ax.invert_yaxis()
    conversion_ax.set_xlim(0, 100)
    conversion_ax.set_xlabel("Sessions advancing to next stage (%)", color=muted)
    conversion_ax.set_xticks(np.arange(0, 101, 20))
    conversion_ax.tick_params(axis="y", labelsize=9, colors=ink)
    conversion_ax.tick_params(axis="x", labelsize=8, colors=muted)
    conversion_ax.grid(axis="x", color="#E7EDF2", zorder=0)
    conversion_ax.grid(axis="y", visible=False)
    for bar, rate in zip(bars, stage_conversion):
        conversion_ax.text(
            rate + 1.5,
            bar.get_y() + bar.get_height() / 2,
            f"{rate:.2f}%",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=ink,
        )
    sns.despine(ax=conversion_ax, left=True, bottom=True)

    drop_ax = fig.add_subplot(grid[3, 0])
    drop_ax.set_facecolor("white")
    drop_ax.set_title(
        "Stage drop-off", loc="left", fontsize=14, fontweight="bold", color=navy, pad=14
    )
    drop_y = np.arange(len(transitions))
    drop_bars = drop_ax.barh(
        drop_y,
        drop_off_counts,
        color=[blue, teal, coral],
        height=0.55,
        zorder=3,
    )
    drop_ax.set_yticks(drop_y, transitions)
    drop_ax.invert_yaxis()
    drop_ax.set_xlim(0, max(drop_off_counts) * 1.55)
    drop_ax.set_xlabel("Sessions lost from previous stage", color=muted)
    drop_ax.tick_params(axis="y", labelsize=9, colors=ink)
    drop_ax.tick_params(axis="x", labelsize=8, colors=muted)
    drop_ax.grid(axis="x", color="#E7EDF2", zorder=0)
    drop_ax.grid(axis="y", visible=False)
    for bar, count, rate in zip(drop_bars, drop_off_counts, drop_off_rates):
        drop_ax.text(
            count + max(drop_off_counts) * 0.025,
            bar.get_y() + bar.get_height() / 2,
            f"{count:,}  |  {rate:.2f}%",
            va="center",
            fontsize=9,
            fontweight="bold",
            color=ink,
        )
    sns.despine(ax=drop_ax, left=True, bottom=True)

    device_ax = fig.add_subplot(grid[3, 1])
    device_ax.set_facecolor("white")
    device_ax.set_title(
        "Overall conversion by device",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color=navy,
        pad=14,
    )
    device_y = np.arange(len(device_funnel))
    device_bars = device_ax.barh(
        device_y,
        device_funnel["Conversion"].to_numpy(),
        color=[blue, teal, gold][: len(device_funnel)],
        height=0.55,
        zorder=3,
    )
    device_ax.set_yticks(device_y, device_funnel.index.astype(str))
    device_ax.set_xlim(0, max(device_funnel["Conversion"]) * 1.42)
    device_ax.set_xlabel("Purchase sessions / Browse sessions (%)", color=muted)
    device_ax.tick_params(axis="y", labelsize=9, colors=ink)
    device_ax.tick_params(axis="x", labelsize=8, colors=muted)
    device_ax.grid(axis="x", color="#E7EDF2", zorder=0)
    device_ax.grid(axis="y", visible=False)
    for bar, (device, row) in zip(device_bars, device_funnel.iterrows()):
        device_ax.text(
            row["Conversion"] + 0.12,
            bar.get_y() + bar.get_height() / 2,
            f'{row["Conversion"]:.2f}%  ({int(row["Purchase"]):,}/{int(row["Browse"]):,})',
            va="center",
            fontsize=9,
            fontweight="bold",
            color=ink,
        )
    sns.despine(ax=device_ax, left=True, bottom=True)

    fig.text(
        0.97,
        0.012,
        "Source: funnel_analysis_data.csv  |  Rates calculated from unique sessions",
        ha="right",
        fontsize=8,
        color=muted,
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print(f"Dashboard saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
