# Diabetes Exploratory Data Analysis (EDA)

![Diabetes Report](images/report_snapshot.png)

## 项目概述
本分析对Pima Indians糖尿病数据集进行探索性数据分析，旨在识别糖尿病的关键风险因素和临床特征。

## 数据集
- **来源**：Pima Indians Diabetes Database
- **样本量**：768条患者记录
- **特征**：
  - Pregnancies：怀孕次数
  - Glucose：血糖水平
  - BloodPressure：血压
  - SkinThickness：皮褶厚度
  - Insulin：胰岛素水平
  - BMI：身体质量指数
  - DiabetesPedigreeFunction：糖尿病遗传函数
  - Age：年龄
  - Outcome：糖尿病诊断结果（0=阴性，1=阳性）

## 关键发现
1. 肥胖(BMI>30)人群患糖尿病概率是正常体重人群的2.8倍
2. 50岁以上人群空腹血糖均值比35岁以下人群高18.7mg/dL
3. 妊娠次数超过5次的女性患病风险显著增加
4. 血糖>126mg/dL的人群中，83%确诊为糖尿病

## 可视化分析
| 图表 | 描述 |
|------|------|
| ![Glucose Distribution](images/glucose_distribution.png) | 血糖分布与临床阈值 |
| ![BMI Classification](images/bmi_classification.png) | BMI分类与糖尿病比例 |
| ![Outcome Ratio](images/outcome_ratio.png) | 糖尿病诊断比例 |
| ![Age vs Glucose](images/age_vs_glucose.png) | 年龄与血糖水平关系 |
| ![Correlation Heatmap](images/correlation_heatmap.png) | 医学特征相关性 |

## 运行指南
1. 克隆仓库：
   ```bash
   git clone https://github.com/your-username/diabetes-eda-analysis.git
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行分析：
   - 打开Jupyter Notebook：
     ```bash
     jupyter notebook notebooks/Diabetes_EDA.ipynb
     ```
   - 或直接查看报告：
     `reports/diabetes_medical_report.html`

## 技术栈
- Python 3.8+
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## 贡献指南
欢迎贡献！请遵循以下步骤：
1. Fork本仓库
2. 创建新分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送分支 (`git push origin feature/your-feature`)
5. 创建Pull Request
