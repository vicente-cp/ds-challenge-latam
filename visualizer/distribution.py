from matplotlib import pyplot as plt

def dates_distribution(df_dates, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(20, 8), dpi=60)
    ax.bar(df_dates.index, df_dates)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_title(title, fontsize=16)
    fig.tight_layout()
    plt.show()
    
def general_distribution(x_data,count, xlabel, ylabel,  title, tick_rotation = False, scale = "linear"):
    fig, ax = plt.subplots(figsize=(20, 8), dpi=60)
    ax.bar(x_data, count)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_title(title, fontsize=16)
    if tick_rotation:
        plt.xticks(rotation=90)
    plt.yscale(scale)
    fig.tight_layout()
    plt.show()
    
