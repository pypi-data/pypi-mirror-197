import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from NMA_draggable_line import draggable_lines

def gating(path: str,
           path2: str) -> None:
    """
    Gets a dataframe with colonies,plots x and y positions and generates a user-defined gate. This gate is used to
    subset the dataframe. Returns a dataframe with user-defined subset.
    """

    df = pd.read_csv(path)

    sns.set_theme()

    df["X"] = df["X"].astype(int)
    df["Y"] = df["Y"].astype(int)

    x0 = df["X"].quantile(.05)
    xf = df["X"].quantile(.95)
    y0 = df["Y"].quantile(.05)
    yf = df["Y"].quantile(.95)

    x_quantile = df["X"].quantile(.2)
    y_quantile = df["Y"].quantile(.2)

    fig = plt.figure()
    ax = fig.add_subplot(sns.scatterplot(data=df, x="X", y="Y", palette='rainbow'))
    ax.set_title('Click once to move the lines. Click again to release')

    upper_line = draggable_lines(ax, 'h', int(yf), [int(df["X"].min() - x_quantile), int(df["X"].max() + x_quantile)])
    bottom_line = draggable_lines(ax, 'h', y0, [int(df["X"].min() - x_quantile), int(df["X"].max() + x_quantile)])
    left_line = draggable_lines(ax, 'v', x0, [int(df["Y"].min() - y_quantile), int(df["Y"].max() + y_quantile)])
    right_line = draggable_lines(ax, 'v', xf, [int(df["Y"].min() - y_quantile), int(df["Y"].max() + y_quantile)])

    plt.show(block=True)

    upper = upper_line.x
    bottom = bottom_line.x
    left = left_line.x
    right = right_line.x

    plt.close('all')

    df2 = df.loc[(df["X"] < upper) & (df["Y"] > bottom)]
    df2 = df2.loc[(df2["X"] < right) & (df2["X"] > left)]
    df2.to_csv(os.path.join(path2, 'Results.csv'))

    return print("complete!")



gating("/media/luiza/DATA/Doutorado/Apoptose/Results/Results.csv", "/home/luiza/Área de Trabalho")