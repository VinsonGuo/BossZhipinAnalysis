import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import imageio
from pylab import mpl
import re


def main():
    # 使matplotlib模块能显示中文
    mpl.rcParams['font.sans-serif'] = ['STFangsong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    # 计算出平均工资
    frames = [pd.read_csv("data/zhipin_android_jobs%s.csv" % i, encoding="utf-8") for i in range(1, 11)]
    df: pd.DataFrame = pd.concat(frames, ignore_index=True)
    df_salary = pd.DataFrame((re.sub(r'·\d+薪', "", i.replace("K", "")).split("-") for i in df['salary']),
                             index=df.index,
                             columns=['min_salary', 'max_salary'])
    df_salary['mean_salary'] = (df_salary['max_salary'].astype('int') + df_salary['min_salary'].astype('int')) / 2
    df['mean_salary'] = df_salary['mean_salary']
    df.to_excel("output/zhipin_android_draft.xls")

    # 平均工资描述统计
    df['mean_salary'].describe().to_excel("output/salary_desc.xls")

    counts = df['company_number'].value_counts()
    counts = pd.Series({
        '0-20人': counts['0-20人'],
        '20-99人': counts['20-99人'],
        '500-999人': counts['500-999人'],
        '1000-9999人': counts['1000-9999人'],
        '10000人以上': counts['10000人以上'],
    })
    draw_pie("company_number", counts, "公司规模比例")
    counts = df['education'].value_counts()
    draw_pie("education", counts, "学历要求")

    counts = df['exprience'].value_counts()
    draw_pie("exprience", counts, "工作经验要求")

    draw_salary_hist(df)

    draw_word_cloud(df)


def draw_salary_hist(df):
    plt.hist(df['mean_salary'], bins=16, edgecolor="black", alpha=0.7)
    plt.xlabel("工资(K)")
    # 显示纵轴标签
    plt.ylabel("频数")
    # 显示图标题
    plt.title("招聘平均工资分布直方图")
    plt.savefig('output/mean_salary_hist_chart.jpg', dpi=400)
    plt.show()


def draw_word_cloud(df):
    text = ''
    for line in df['company_name']:
        text += line + " "
    color_mask = imageio.imread('res/cloud.jpg')  # 设置背景图
    cloud = WordCloud(
        scale=4,
        font_path='PingFang.ttc',
        background_color='white',
        mask=color_mask,
        max_words=1000,
        max_font_size=100
    )
    word_cloud = cloud.generate(text)
    # 保存词云图片
    word_cloud.to_file('output/word_cloud.jpg')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


def draw_pie(name: str, data, title: str):
    plt.pie(data, labels=data.keys(), autopct='%2.1f%%')
    plt.title(title)
    plt.axis('equal')  # 使饼图为正圆形
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    plt.savefig('output/%s_pie_chart.jpg' % name, dpi=400)
    plt.show()


if __name__ == "__main__":
    main()
