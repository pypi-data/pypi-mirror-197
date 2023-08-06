import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from src.draggable_line import draggable_lines
import os


def gating(path: str,
           path2: str,
           x: str = "X",
           y: str = "Y") -> None:
    """
    Gets a dataframe with colonies,plots x and y positions and generates a user-defined gate. This gate is used to
    subset the dataframe. Returns a dataframe with user-defined subset.
    """

    df = pd.read_csv(path)

    sns.set_theme()

    df[x] = df[x].astype(int)
    df[y] = df[y].astype(int)

    x0 = df[x].quantile(.05)
    xf = df[x].quantile(.95)
    y0 = df[y].quantile(.05)
    yf = df[y].quantile(.95)

    x_quantile = df[x].quantile(.2)
    y_quantile = df[y].quantile(.2)

    fig = plt.figure()
    ax = fig.add_subplot(sns.scatterplot(data=df, x=x, y=y, palette='rainbow'))
    ax.set_title('Click once to move the lines. Click again to release')

    upper_line = draggable_lines(ax, 'h', int(yf), [int(df[x].min() - x_quantile), int(df[x].max() + x_quantile)])
    bottom_line = draggable_lines(ax, 'h', y0, [int(df[x].min() - x_quantile), int(df[x].max() + x_quantile)])
    left_line = draggable_lines(ax, 'v', x0, [int(df[y].min() - y_quantile), int(df[y].max() + y_quantile)])
    right_line = draggable_lines(ax, 'v', xf, [int(df[y].min() - y_quantile), int(df[y].max() + y_quantile)])

    plt.show(block=True)

    upper = upper_line.x
    bottom = bottom_line.x
    left = left_line.x
    right = right_line.x

    plt.close('all')

    df2 = df.loc[(df[x] < upper) & (df[y] > bottom)]
    df2 = df2.loc[(df2[x] < right) & (df2[x] > left)]
    df2.to_csv(os.path.join(path2, 'Gated Results.csv'))

    return print("complete!")


#if __name__ == "__main__":
    gating("/home/luiza/PycharmProjects/Gating/tests/Results.csv", "/home/luiza/PycharmProjects/Gating/tests")
