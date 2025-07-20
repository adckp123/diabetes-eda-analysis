# ===== src/visualization.py =====
import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import matplotlib.font_manager as fm


# === 文本渲染函数 ===
def create_text_image(text, font_size=20, width=300, height=50, bg_color=(255, 255, 255)):
    """创建文本图像 - 改进版本"""
    # 创建空白图像
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)

    # 字体路径映射
    font_mapping = {
        'DejaVu Sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        'WenQuanYi Micro Hei': '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        'SimHei': '/usr/share/fonts/truetype/droid/DroidSansFallback.ttf',
        'TakaoPGothic': '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
    }

    font = None
    for font_name, path in font_mapping.items():
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except:
                continue

    # 回退机制
    if font is None:
        try:
            font = ImageFont.truetype("simhei.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arialuni.ttf", font_size)
            except:
                font = ImageFont.load_default()

    # 文本位置计算
    try:
        bbox = d.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # 确保文本在图像范围内
        x = max(0, min(x, width - text_width))
        y = max(0, min(y, height - text_height))
    except:
        # 估算位置
        x = (width - len(text) * font_size * 0.6) // 2
        y = (height - font_size * 1.2) // 2

    # 绘制文本
    d.text((x, y), text, font=font, fill=(0, 0, 0))
    return np.array(img)


def add_text_to_plot(ax, text, x, y, width=0.2, height=0.05, font_size=12, bg_color=(255, 255, 255)):
    """在图表中添加文本 - 透明背景版"""
    text_img = create_text_image(text, font_size,
                                 width=int(width * 1000),
                                 height=int(height * 1000),
                                 bg_color=bg_color)

    # 创建OffsetImage
    imagebox = OffsetImage(text_img, zoom=0.7)
    imagebox.image.axes = ax

    # 添加到图表
    ab = AnnotationBbox(imagebox, (x, y),
                        xycoords='data',
                        frameon=False,
                        box_alignment=(0.5, 0.5))
    ax.add_artist(ab)


# === 图表工具函数 ===
def plot_to_base64(plot_func):
    """将图表转换为Base64编码"""
    buf = BytesIO()
    plot_func()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close()
    buf.seek(0)
    return f'data:image/png;base64,{base64.b64encode(buf.read()).decode("utf-8")}'


def setup_chinese_font():
    """设置中文字体支持 - 使用Kaggle内置字体"""
    try:
        # 使用Kaggle实际存在的字体
        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        if os.path.exists(font_path):
            # 注册字体
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
            return font_prop

        # 添加更多中文字体选项
        possible_fonts = [
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
            '/usr/share/fonts/truetype/droid/DroidSansFallback.ttf'
        ]

        for font_path in possible_fonts:
            if os.path.exists(font_path):
                font_prop = fm.FontProperties(fname=font_path)
                plt.rcParams['font.family'] = 'sans-serif'
                plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
                return font_prop

        # 最终回退到支持中文的字体
        plt.rcParams['font.family'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
        return None
    except Exception as e:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
        return None


# === 专业医学图表函数 ===
def plot_glucose_distribution(df):
    """血糖分布图 - 使用英文标签"""
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 使用专业医学颜色
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

    # 绘制分布图
    sns.histplot(df['Glucose'], kde=True, bins=25, color=colors[0], alpha=0.7)

    # 添加医学阈值线
    plt.axvline(70, color='#1f77b4', linestyle='--', linewidth=1.5)
    plt.axvline(100, color='#ff7f0e', linestyle='--', linewidth=1.5)
    plt.axvline(126, color='#d62728', linestyle='--', linewidth=1.5)

    # 添加文本标签
    add_text_to_plot(ax, "Fasting Glucose Distribution (mg/dL)", 0.5, 1.05, width=0.4, font_size=16)
    add_text_to_plot(ax, "Glucose (mg/dL)", 0.5, -0.1, width=0.2, font_size=12)
    add_text_to_plot(ax, "Frequency", -0.1, 0.5, width=0.1, height=0.3, font_size=12)

    # 确保阈值标签位置一致
    y_pos = plt.ylim()[1] * 0.85
    add_text_to_plot(ax, "Hypoglycemia Threshold", 70, y_pos, width=0.15, font_size=12)
    add_text_to_plot(ax, "Normal Upper Limit", 100, y_pos, width=0.15, font_size=12)
    add_text_to_plot(ax, "Diabetes Threshold", 126, y_pos, width=0.15, font_size=12)

    # 添加自动布局调整
    plt.tight_layout()
    sns.despine()


def plot_bmi_distribution(df):
    """BMI分类分布图 - 使用英文标签"""
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 设置颜色
    palette = {'Underweight': '#66c2a5', 'Normal': '#fc8d62', 'Overweight': '#8da0cb', 'Obese': '#e78ac3'}

    # 计算每个类别的比例
    bmi_counts = df['BMI_Class'].value_counts().sort_index()
    bmi_percent = bmi_counts / bmi_counts.sum() * 100

    # 绘制条形图
    barplot = sns.barplot(x=bmi_counts.index, y=bmi_counts.values, palette=palette, alpha=0.85)

    # 添加数值标签
    for i, v in enumerate(bmi_counts.values):
        plt.text(i, v + 5, f"{v} ({bmi_percent[i]:.1f}%)",
                 ha='center', fontsize=12, color='black')

    # 添加标题和标签
    plt.title("BMI Classification Distribution", fontsize=16, pad=20)
    plt.xlabel("BMI Class", fontsize=12)
    plt.ylabel("Count", fontsize=12)

    # 设置y轴范围
    plt.ylim(0, max(bmi_counts.values) * 1.2)

    # 添加网格线
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    sns.despine()
    plt.xticks(rotation=15, ha='right')


def plot_diabetes_outcome(df):
    """糖尿病比例图 - 使用英文标签"""
    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    # 计算比例
    outcome_counts = df['Outcome'].value_counts()
    labels = ['Healthy', 'Diabetes']
    colors = ['#66c2a5', '#fc8d62']
    explode = (0, 0.1)

    # 绘制饼图
    wedges, texts, autotexts = plt.pie(outcome_counts, explode=explode, colors=colors,
                                       shadow=True, startangle=90,
                                       autopct='%1.1f%%', textprops={'color': 'black', 'fontsize': 12})

    # 添加标题
    plt.title("Diabetes Diagnosis Proportion", fontsize=16, pad=20)

    # 添加图例
    plt.legend(wedges, [f"{label}: {count} ({percent:.1f}%)"
                        for label, count, percent in zip(labels, outcome_counts, outcome_counts / len(df) * 100)],
               title="Diagnosis",
               loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))

    # 添加中心圆
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.axis('equal')


def plot_age_glucose_relation(df):
    """年龄与血糖关系图 - 使用英文标签"""
    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # 设置颜色
    palette = {'Young': '#66c2a5', 'Middle-aged': '#fc8d62', 'Elderly': '#8da0cb'}

    # 绘制箱线图
    sns.boxplot(x='Age_Group', y='Glucose', data=df, order=['Young', 'Middle-aged', 'Elderly'],
                palette=palette, width=0.6, showfliers=False)

    # 添加散点图显示数据分布
    sns.stripplot(x='Age_Group', y='Glucose', data=df, order=['Young', 'Middle-aged', 'Elderly'],
                  color='#333333', alpha=0.3, size=4, jitter=True)

    # 计算并添加均值线
    means = df.groupby('Age_Group')['Glucose'].mean().values
    for i, mean_val in enumerate(means):
        plt.plot([i - 0.3, i + 0.3], [mean_val, mean_val],
                 linestyle='--', linewidth=2, color='#d62728')
        # 添加英文标签
        add_text_to_plot(ax, f"Mean: {mean_val:.1f}", i + 0.35, mean_val, width=0.15, font_size=10)

    # 添加标题和标签 - 使用英文
    add_text_to_plot(ax, "Glucose Levels by Age Group", 0.5, 1.05, width=0.4, font_size=16)
    add_text_to_plot(ax, "Age Group", 0.5, -0.1, width=0.15, font_size=12)
    add_text_to_plot(ax, "Glucose (mg/dL)", -0.1, 0.5, width=0.15, height=0.3, font_size=12)

    # 添加网格线
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    sns.despine()


def plot_feature_correlation(df):
    """特征相关性图 - 使用英文标签"""
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 计算相关系数
    numeric_cols = df.select_dtypes(include=['number']).columns
    corr_matrix = df[numeric_cols].corr()

    # 创建热力图
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
                cmap='coolwarm', vmin=-1, vmax=1,
                linewidths=0.5, linecolor='white',
                cbar_kws={'shrink': 0.8})

    # 添加标题 - 使用英文
    add_text_to_plot(ax, "Feature Correlation", 0.5, 1.05, width=0.3, font_size=16)

    # 添加轴标签 - 使用英文
    for i, col in enumerate(corr_matrix.columns):
        add_text_to_plot(ax, col, i + 0.5, -0.5, width=0.15, font_size=10)
        add_text_to_plot(ax, col, -0.5, i + 0.5, width=0.15, height=0.1, font_size=10)