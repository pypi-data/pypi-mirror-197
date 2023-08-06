def boxplot_show(df, sp_num):
    import matplotlib.pyplot as plt
    import seaborn as sns
    count = 1
    for i in sp_num:
        # установка размера для графиков
        plt.figure(figsize=(20, 20))
        # построение боксплотов для каждого числового атрибута
        plt.title(i)
        plt.subplot(5, 5, count)
        sns.boxplot(x=df[i])
        count += 1
    plt.show()

def histplot_show(df, sp_num):
    import matplotlib.pyplot as plt
    import seaborn as sns
    count = 1
    for i in sp_num:
        # установка размера для графиков
        plt.figure(figsize=(20, 20))
        # построение боксплотов для каждого числового атрибута
        plt.title(i)
        plt.subplot(5, 5, count)
        sns.hist(x=df[i])
        count += 1
    plt.show()

def distplot_show(df, sp_num):
    import matplotlib.pyplot as plt
    import seaborn as sns
    count = 1
    for i in sp_num:
        # установка размера для графиков
        plt.figure(figsize=(20, 20))
        # построение боксплотов для каждого числового атрибута
        plt.title(i)
        plt.subplot(5, 5, count)
        sns.hist(x=df[i])
        count += 1
    plt.show()
