import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
from pathlib import Path
import jupyter_black
import fire, os

jupyter_black.load(line_length=120)
sns.set_style("ticks")


os.makedirs("../figures", exist_ok=True)


def main(
    # Save directory
    save_dir="./figures/",
    test_name="maze-right",  # "photometry-1"
    data_folder=Path(".") / "data",
    # Camera Settings Parameters
    DOWNSAMPLING_FACTOR=2,
    CAMERA_UPDATE_RATE=20,
    UPDATES_PER_DISPLAY=1,
    CRF=23,
    ENCODERING_SPEED="fast",
    COMPRESSION_STANDARD="h265",
    FPS=60,
    NUMBER_CAMERAS=6,
):
    # Load the data
    results_df = data_folder / test_name / "results.tsv"
    df = pd.read_csv(results_df.resolve(), sep="\t")
    # Convert 'duration' and 'real_duration' to datetime format
    df["duration"] = pd.to_timedelta(df["duration"])
    df["percent_dropped_frames"] = ((df["dropped_frames"]) / (df["FPS"] * df["duration"].dt.total_seconds())) * 100
    # Figure Title
    fig, axes = plt.subplots(1, 4)
    fig.set_size_inches(16, 3.2)
    # Panel Labels
    panel_labels = ["A", "B", "C", "D"]
    for idx, ax in enumerate(axes):
        ax.text(
            -0.12,
            1.12,
            panel_labels[idx],
            transform=ax.transAxes,
            fontsize=16,
            fontweight="bold",
            va="top",
            ha="right",
        )

    # Adjust spacing between rows
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    # Camera Config Settings
    n_cameras_unique = df["experiment_config_n_cameras"].nunique()
    rainbow_palette_cameras = [cm.rainbow(i / max(n_cameras_unique - 1, 1)) for i in range(n_cameras_unique)]

    # FPS plot with rainbow palette for number of cameras
    axes[0].set_title("Frame per second\n vs\n Dropped Frames (%)")
    lineplot_fps = sns.lineplot(
        ax=axes[0],
        data=df[
            (df["downsampling_factor"] == DOWNSAMPLING_FACTOR)
            & (df["application_config_gui_config_camera_update_rate"] == CAMERA_UPDATE_RATE)
            & (df["application_config_gui_config_camera_updates_per_display_update"] == UPDATES_PER_DISPLAY)
            & (df["application_config_ffmpeg_config_crf"] == CRF)
            & (df["application_config_ffmpeg_config_encoding_speed"] == ENCODERING_SPEED)
            & (df["application_config_ffmpeg_config_compression_standard"] == COMPRESSION_STANDARD)
        ],
        x="FPS",
        y="percent_dropped_frames",
        hue="experiment_config_n_cameras",
        marker="o",
        legend=True,
        palette=rainbow_palette_cameras,
    )
    if lineplot_fps.legend_ is not None:
        lineplot_fps.legend_.set_title("Number of Cameras")
    axes[0].set_xlabel("FPS")
    axes[0].set_ylabel("Dropped Frames (%)")
    # GUI Settings

    axes[1].set_title(f"Downsampling Factor\n vs\n Dropped Frames ({NUMBER_CAMERAS} Cameras)")
    n_downsampling_unique = df["downsampling_factor"].nunique()
    rainbow_palette_downsampling = [
        cm.rainbow(i / max(n_downsampling_unique - 1, 1)) for i in range(n_downsampling_unique)
    ]
    lineplot_downsampling = sns.lineplot(
        ax=axes[1],
        data=df[
            (df["experiment_config_n_cameras"] == NUMBER_CAMERAS)
            & (df["application_config_gui_config_camera_update_rate"] == CAMERA_UPDATE_RATE)
            & (df["application_config_gui_config_camera_updates_per_display_update"] == UPDATES_PER_DISPLAY)
            & (df["application_config_ffmpeg_config_crf"] == CRF)
            & (df["application_config_ffmpeg_config_encoding_speed"] == ENCODERING_SPEED)
            & (df["application_config_ffmpeg_config_compression_standard"] == COMPRESSION_STANDARD)
        ],
        x="FPS",
        y="percent_dropped_frames",
        hue="downsampling_factor",
        marker="o",
        legend=True,
        palette=rainbow_palette_downsampling,
    )
    if lineplot_downsampling.legend_ is not None:
        lineplot_downsampling.legend_.set_title("Downsampling Factor")
    axes[1].set_xlabel("FPS")
    axes[1].set_ylabel("Dropped Frames (%)")

    axes[2].set_title(f"Camera Updates per Display Update\n vs\n Dropped Frames (%) ({NUMBER_CAMERAS} Cameras)")
    lineplot_updates_per_display = sns.lineplot(
        ax=axes[2],
        data=df[
            (df["experiment_config_n_cameras"] == NUMBER_CAMERAS)
            & (df["downsampling_factor"] == DOWNSAMPLING_FACTOR)
            & (df["application_config_gui_config_camera_update_rate"] == CAMERA_UPDATE_RATE)
            & (df["application_config_ffmpeg_config_crf"] == CRF)
            & (df["application_config_ffmpeg_config_encoding_speed"] == ENCODERING_SPEED)
            & (df["application_config_ffmpeg_config_compression_standard"] == COMPRESSION_STANDARD)
        ],
        x="FPS",
        y="percent_dropped_frames",
        hue="application_config_gui_config_camera_updates_per_display_update",
        marker="o",
        legend=True,
    )
    if lineplot_updates_per_display.legend_ is not None:
        lineplot_updates_per_display.legend_.set_title("Updates per Display update")
    axes[2].set_xlabel("FPS")
    axes[2].set_ylabel("Dropped Frames (%)")

    axes[3].set_title(f"Compression Standard \nvs \nNumber of Cameras  ({NUMBER_CAMERAS} Cameras)")
    lineplot_compression = sns.lineplot(
        ax=axes[3],
        data=df[
            (df["experiment_config_n_cameras"] == NUMBER_CAMERAS)
            & (df["downsampling_factor"] == DOWNSAMPLING_FACTOR)
            & (df["application_config_gui_config_camera_update_rate"] == CAMERA_UPDATE_RATE)
            & (df["application_config_gui_config_camera_updates_per_display_update"] == UPDATES_PER_DISPLAY)
            & (df["application_config_ffmpeg_config_crf"] == CRF)
            & (df["application_config_ffmpeg_config_encoding_speed"] == ENCODERING_SPEED)
        ],
        x="FPS",
        y="percent_dropped_frames",
        hue="application_config_ffmpeg_config_compression_standard",
        marker="o",
        legend=True,
    )
    if lineplot_compression.legend_ is not None:
        lineplot_compression.legend_.set_title("Compression standard")
    axes[3].set_xlabel("FPS")
    axes[3].set_ylabel("Dropped Frames (%)")

    fig.savefig(str(Path(save_dir) / ("figure-" + test_name + ".png")), bbox_inches="tight", dpi=150)


if __name__ == "__main__":
    fire.Fire(main)
