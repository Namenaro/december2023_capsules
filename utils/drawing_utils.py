import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero

def make_arrows(axs):
    axs.xaxis.set_ticks_position('bottom')
    axs.yaxis.set_ticks_position('left')

    # make arrows
    axs.spines['left'].set_position('zero')
    axs.spines['right'].set_visible(False)
    axs.spines['bottom'].set_position('zero')
    axs.spines['top'].set_visible(False)
    axs.xaxis.set_ticks_position('bottom')
    axs.yaxis.set_ticks_position('left')
    axs.plot((1), (0), ls="", marker=">", ms=10, color="k",
             transform=axs.get_yaxis_transform(), clip_on=False)
    axs.plot((0), (1), ls="", marker="^", ms=10, color="k",
             transform=axs.get_xaxis_transform(), clip_on=False)



def draw_ECG(ax, signal):
    ax.plot(signal, color='black', alpha=0.2, label="ECG")
    make_arrows(ax)
    ax.set_xticks(range(0, len(signal),5))
    ax.grid(which='major', axis='both', linestyle='--', alpha=0.75)
    ax.plot(signal, 'o', label='vals', color="black",  markersize=2)


def draw_vertical_line(ax, x, y, color=None, label=None):
    if color is None:
        color = 'red'
    ax.vlines(x=x, ymin=0, ymax=y, colors=color, lw=2, alpha=0.5, label=label)


class PointsCloudDrawer:
    def __init__(self, xs, ys, names):
        self.xs = xs
        self.ys = ys
        self.names = names

        self.ws = list([self.ys[i] + self.xs[i] for i in range(len(names))])

    def draw_on_01(self, ax):
        ax.scatter(self.xs, self.ys, alpha=0.5, s=7)
        for i, txt in enumerate(self.names):
            ax.annotate(txt, (self.xs[i], self.ys[i]),  fontsize=7)
        ax.set_xlim([-0.1, 1.1])
        ax.set_ylim([-0.1, 1.1])

    def get_top_n_indices(self, n):
        top_indixes = sorted(range(len(self.ws)), key=lambda i: self.ws[i], reverse=True)[:n]
        return top_indixes
