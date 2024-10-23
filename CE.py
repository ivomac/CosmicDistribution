#!/usr/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

plt.rcParams["font.family"] = "monospace"

cm0 = plt.colormaps["tab10"]
cm1 = plt.colormaps["tab20c"]
cm2 = plt.colormaps["Set2"]
cm3 = plt.colormaps["Dark2"]

C = {
    "Base": cm3(7),
    "Extended": cm0(1),
    "Reward": cm3(2),
    "Attack": cm0(3),
    "Negotiate": cm0(2),
    "Morph": cm2(5),
    "Reinforce": cm3(3),
    "Artifact": cm0(0),
}

Base_attacks = {
    "M": 1,
    "00": 1,
    "01": 1,
    "02": 0,
    "03": 0,
    "04": 4,
    "05": 1,
    "06": 7,
    "07": 1,
    "08": 7,
    "09": 1,
    "10": 4,
    "11": 1,
    "12": 2,
    "13": 1,
    "14": 2,
    "15": 1,
    "16": 0,
    "20": 2,
    "23": 1,
    "30": 1,
    "40": 1,
    "+2": 2,
    "+3": 3,
    "+5": 1,
}

Extended_attacks = {
    "M": 1,
    "00": 1,
    "02": 1,
    "04": 1,
    "06": 2,
    "08": 2,
    "10": 1,
    "12": 1,
    "14": 1,
    "20": 1,
    "30": 1,
    "+2": 2,
    "+4": 1,
    "+8": 1,
}

Reward_deck = {
    "A": 5,
    "Ri": 4,
    "N": 3,
    "M": 1,
    "+4": 1,
    "+5": 2,
    "+6": 1,
    "X0": 1,
    "X2": 2,
    "X3": 1,
    "-07": 1,
    "-04": 1,
    "-01": 1,
    "10": 3,
    "16": 1,
    "17": 1,
    "18": 1,
    "19": 1,
    "23": 1,
}

Extended_reward_deck = {
    "A": 5,
    "Ri": 4,
    "N": 4,
    "Re": 2,
    "M": 1,
    "+4": 1,
    "+X": 1,
    "X-": 1,
    "X1": 1,
    "X2": 2,
    "X4": 1,
    "I": 4,
}

Rejected_reward_deck = {
    "02/": 1,
    "03/": 1,
    "12/": 2,
    "21/": 1,
}

Base_pie = {
    "Negotiate": 15,
    "Attack": 39,
    "Morph": 1,
    "Artifact": 11,
    "Reinforce": 6,
}

Full_pie = {
    "Negotiate": 20,
    "Attack": 51,
    "Morph": 2,
    "Artifact": 15,
    "Reinforce": 10,
}

mfig = plt.figure(figsize=(7.07, 5))
figs = mfig.subfigures(2, 2)

for h in [0, 1]:
    keys = set(Base_attacks.keys())
    keys.update(Extended_attacks.keys())
    keys = sorted(keys)
    keys = ["M", *keys[:-1]]

    b = [Base_attacks.get(k, 0) for k in keys]
    e = [Extended_attacks.get(k, 0) for k in keys]

    fig = figs[0][h]
    ax = fig.subplots(1, 1)

    ax.bar(keys, b, label="Base", zorder=2, color=C["Base"])
    ax.bar(keys, e, bottom=b, label="Extended", zorder=1, color=C["Extended"])

    ticks = [2, 4, 6, 8, 10]
    ax.set_yticks(ticks)
    ax.set_yticklabels([str(j) for j in ticks])
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="tab:gray", linestyle="-", zorder=-1)

    x = ax.get_xticklabels()
    ticks_loc = ax.get_xticks()
    FL = mpl.ticker.FixedLocator(ticks_loc)
    ax.xaxis.set_major_locator(FL)
    ax.set_xticklabels(x, rotation=60, ha="center")

    ax.legend()

    ax.set_title("Cosmic deck attack distribution", fontweight="bold")

    fig = figs[1][h]
    axs = fig.subplots(1, 2)

    ax = axs[0]

    x, y = zip(*Full_pie.items())

    r = [1, 0.3]

    pie_props = dict(
        startangle=100,
        pctdistance=1.23,
        wedgeprops=dict(width=r[1], edgecolor="w"),
        textprops=dict(fontweight="bold"),
    )

    def func(pct, x, y):
        a = int(np.round(pct / 100.0 * np.sum(y)))
        return "{:}\n{:.0f}%".format(x[y.index(a)], pct)

    ax.set_prop_cycle(cycler("color", [C[i] for i in x]))
    patches, texts, pcts = ax.pie(
        y, autopct=lambda pct: func(pct, x, y), **pie_props, radius=r[0]
    )
    ax.axis("equal")
    for i, pct in enumerate(pcts):
        pct.set_color(patches[i].get_facecolor())

    x, y = zip(*Base_pie.items())

    ax.pie(y, **pie_props, radius=r[0] - r[1])
    ax.axis("equal")

    ax.text(-0.1, -0.25, "Base", fontweight="bold", color=C["Base"])
    ax.text(0.65, -0.9, "Extended", fontweight="bold", color=C["Extended"])

    ax = axs[1]

    Reward_deck = {
        k: Reward_deck.get(k, 0) + Extended_reward_deck.get(k, 0)
        for k in set(Reward_deck) | set(Extended_reward_deck)
    }

    keys = Reward_deck.keys()

    ordered = ["A", "Ri", "N", "Re", "M"]
    keys = [*ordered, *sorted(set(keys) - set(ordered))]

    y = [-Reward_deck[k] for k in keys]

    ax.set_yticklabels([])
    ax.set_yticks([])
    ax1 = ax.twinx()
    ax1.barh(keys, y, align="center", zorder=2, color=C["Reward"])

    ticks = range(0, -11, -1)
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(-s) for s in ticks])
    ax.grid(axis="x", color="tab:gray", linestyle="-", zorder=-1)

    ax.set_title("Reward deck", fontweight="bold")

mfig.savefig("CE.pdf")
