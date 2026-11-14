from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False

# Paths
ROOT = Path(__file__).resolve().parent.parent  # pyMV code folder.
data_dir = ROOT / "data"
results_dir = ROOT / "figures"


def plot_tests(exp_dir, save_fig=False):
    fig, axes = plt.subplots(2, 3, figsize=[9, 6])
    axes = axes.flatten()

    # Fast encoding speed plots

    # Plot FPS vs. number of cameras
    n_cams_dir = exp_dir / "fps_n_cameras"
    plot_test_result(n_cams_dir, palette="RdYlBu_r", ax=axes[0])

    # Plots FPS vs downsampling factor
    downsample_dir = exp_dir / "fps_downsampling"
    plot_test_result(downsample_dir, palette="Dark2_r", ax=axes[1])

    # Plot FPS vs compression standard
    compression_dir = exp_dir / "fps_comp_standard"
    plot_test_result(compression_dir, palette="tab10", ax=axes[2])

    # Slow encoding speed plots

    # Plot FPS vs. number of cameras
    n_cams_dir = exp_dir / "fps_n_cameras_slow"
    plot_test_result(n_cams_dir, palette="RdYlBu_r", ax=axes[3])

    # Plots FPS vs downsampling factor
    downsample_dir = exp_dir / "fps_downsampling_slow"
    plot_test_result(downsample_dir, palette="Dark2_r", ax=axes[4])

    # Plot FPS vs compression standard
    compression_dir = exp_dir / "fps_comp_standard_slow"
    plot_test_result(compression_dir, palette="tab10", ax=axes[5])


    fig.tight_layout()
    for ax, label in zip(axes, "ABCDEF"):
        ax.text(-0.15, 0.95, label, transform=ax.transAxes, fontsize=12, fontweight="bold", ha="right", va="bottom")

    if save_fig:
        save_path = results_dir / f"{exp_dir.name}.pdf"
        fig.savefig(save_path.resolve())

    plt.show()


def plot_test_result(test_dir, x=None, hue=None, palette="tab10", show_plot=False, save_path=None, ax=None):
    """Plot performance metrics from the results.tsv file in a test data directory.
    By default the first sweep parameter is used for the x-axis, the second sweep parameter
    is used for the hue, and the y-axis is percent_dropped_frames.
    """
    # Load test parameters
    test_params_path = test_dir / "test_parameters.json"
    with open(test_params_path, "r") as f:
        test_params = json.load(f)
    sweep_params = list(test_params["parameter_sweeps"].keys())
    if x is None:
        x = sweep_params[0]
    if hue is None:
        hue = sweep_params[1] if len(sweep_params) > 1 else None
    # Load data table.
    results_path = test_dir / "results.tsv"
    df = pd.read_csv(results_path.resolve(), sep="\t")
    # Check frame count from openCV matches that from the metadata file.
    if not df["openCV_frame_count"].equals(df["recorded_frames"]):
        print("Warning: Frame count from openCV does not match that from the metadata file.")
    # Make plot
    if ax is None:
        fig = plt.figure(1, figsize=[4, 4])
        ax = fig.add_subplot(1, 1, 1)
    sns.lineplot(data=df, x=x, y="percent_dropped_frames", hue=hue, marker="o", palette=palette, ax=ax)
    ax.axhline(y=0, color="k", linewidth=0.5)
    ax.set_ylabel("Dropped Frames (%)")
    ax.set_xlabel("FPS" if x == "fps" else x)
    ax.set_xticks(df[x].unique())
    if save_path:
        plt.savefig(save_path.resolve())
    if show_plot:
        plt.show()


if __name__ == "__main__":
    plot_tests(data_dir / "i7-9700-RTX2060" , save_fig=True)
    plot_tests(data_dir / "i7-6700-RTXA400" , save_fig=True)