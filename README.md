Product Segmentation via K-Means Clustering

This project demonstrates the use of the K-Means clustering algorithm to segment e-commerce products based on co-purchase behavior.

🎯 Objective

To identify natural product groupings based on transactional sales data (orders), and use this to build useful product segments for marketing, cross-selling, or catalog optimization.

🧰 Tools & Technologies

Python (pandas, itertools, scikit-learn)

Excel (.xlsx) for input/output

Matplotlib / Seaborn for basic plotting

🧠 Methodology

Each sales order (from CSV/XLSX) contains multiple product IDs.

For every product, we calculate co-occurrence with other products in the same order.

A co-purchase frequency matrix is built.

Cosine similarity is computed between product vectors.

K-Means clustering is used to assign each product to a segment.

📁 Files

python.przetwarzanie_e-commerce.py – core Python script performing clustering

E-commerce_hity_dobre_longtail_clean.xlsx – input file (not public)

README.md – this file

Screenshots – visual examples of the input/output and analysis

🧪 Sample Data

To respect confidentiality, real product IDs and order data are not included. The screenshots show output using anonymized or synthetic data.

📸 Sample Output

The following visualizations show sample clusters, purchase behavior mapping, and product labeling after segmentation.

📌 Due to company NDA, only fragments of sample outputs are presented in the form of screenshots.

🚀 Installation & Run

# 1. Clone the repository or download the files
# 2. Make sure you have the dependencies installed:
pip install pandas scikit-learn matplotlib

# 3. Run the Python script
python python.przetwarzanie_e-commerce.py

👤 Author

Bartosz Ceranek📧 bartosz.ceranek@gmail.com🔗 GitHub: bceranek

⚠️ Disclaimer

All visuals and screenshots are based on anonymized or synthetic data. No sensitive or proprietary information is shared.

💡 Business Value

Enables product clustering based on customer behavior.

Can assist in identifying bundles, categories or campaign groups.

Aids marketing and merchandising teams in targeting and positioning.

