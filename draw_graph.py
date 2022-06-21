import json

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["legend.fontsize"] = "x-small"


def main():
    with open("main.log", "r") as stream:
        logs = [json.loads(line) for line in stream.readlines()]

    for i in range(0, len(logs), 2):
        assert (
            logs[i]["cpuinfo"]["brand_raw"]
            == logs[i + 1]["cpuinfo"]["brand_raw"]
        )
        assert not logs[i]["args"]["ftz"]
        assert logs[i + 1]["args"]["ftz"]

    colors = list(matplotlib.colors.TABLEAU_COLORS)
    alphas = [1.0, 0.5]
    titles = [
        "Normalized number",
        "Denormalized number",
        "NaN",
    ]
    metrics = [
        "task_normal.time.avg",
        "task_denormal.time.avg",
        "task_nan.time.avg",
    ]
    results = [
        "task_normal.result",
        "task_denormal.result",
        "task_nan.result",
    ]

    fig = plt.figure(figsize=(15, 5))
    overview = {}

    for i, (title, metric, result) in enumerate(zip(titles, metrics, results)):
        ax = fig.add_subplot(1, 3, i + 1)
        ax.set_title(title)
        ax.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        ax.grid(alpha=0.5, linestyle="--")
        ax.set_ylabel("Processing Time (ms)")

        for i, log in enumerate(logs):
            ax.bar(i, log[metric], color=colors[i // 2], alpha=alphas[i % 2])

            overview[log["cpuinfo"]["brand_raw"]] = overview.get(log["cpuinfo"]["brand_raw"], {})
            overview[log["cpuinfo"]["brand_raw"]][log["args"]["ftz"]] = overview[log["cpuinfo"]["brand_raw"]].get(log["args"]["ftz"], {})
            overview[log["cpuinfo"]["brand_raw"]][log["args"]["ftz"]][metric] = overview[log["cpuinfo"]["brand_raw"]][log["args"]["ftz"]].get(metric, {})
            overview[log["cpuinfo"]["brand_raw"]][log["args"]["ftz"]][metric] = log[metric]
            overview[log["cpuinfo"]["brand_raw"]][log["args"]["ftz"]][result] = log[result]

    print(json.dumps(overview, indent=2))

    labels = []
    for i, log in enumerate(logs):
        label = log["cpuinfo"]["brand_raw"]
        label += " (ftz/daz)" if log["args"]["ftz"] else ""
        labels.append(label)
    fig.legend(labels, loc="upper right")

    plt.show()


if __name__ == "__main__":
    main()
