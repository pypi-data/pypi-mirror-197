# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(df, sp_num):
    import matplotlib.pyplot as plt
    import seaborn as sns
    count = 1
    for i in sp_num:
        # установка размера для графиков
        plt.figure(figsize=(20, 20))
        # построение боксплотов для каждого числового атрибута
        plt.subplot(4, 4, count)
        sns.boxplot(x=df[i])
        count += 1
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
