import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.gridspec as gridspec


get_color = lambda x: 'g' if x < 0 else 'r'


def plot_volume(ax, df, count=50):
    ax.set_title('BTC Volume')
    colors = list((df['open'] - df['close']).apply(get_color)) 
    plt.bar(df.index[:count], df['volume'][:count], color=colors[:count])


def plot_candlestick(ax, df, count=50, colorup='g', colordown='r'):
    ax.set_title('BTC Candlestick')
    ax.set_ylabel('price USD')
    width = 0.6
    offset = width / 2.0

    for time, row in df[:count].iterrows():
        if row['close'] >= row['open']:
            color = colorup
            lower = row['open']
            height = row['close'] - row['open']
        else:
            color = colordown
            lower = row['close']
            height = row['open'] - row['close']
        vline = Line2D(
            xdata=(time, time), ydata=(row['low'], row['high']),
            color=color,
            linewidth=0.5,
            antialiased=True,
        )
        rect = Rectangle(
            xy=(time - offset, lower),
            width=width,
            height=height,
            facecolor=color,
            edgecolor=color,
        )
        ax.add_line(vline)
        ax.add_patch(rect)

    ax.autoscale_view()


columns = ['open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
]

df = pd.read_csv('btc-prices.csv', names=columns)
df = df[columns[:6]]

# Define Axes
gs = gridspec.GridSpec(3, 1)
ax = plt.subplot(gs[:2, :])
ax_vol = plt.subplot(gs[2, :], sharex=ax)
plt.tight_layout(pad=2.0)

# Set Grid
ax.grid(axis="y")
ax_vol.grid(axis="y")

# Candlesticks
plot_candlestick(ax, df, 90)
ax.plot(df['close'].rolling(7).mean()[:90])
ax.plot(df['close'].rolling(25).mean()[:90])

# Volume
plot_volume(ax_vol, df, 90)
plt.savefig('candlestick.png', dpi=600)