# E-commerce Conversion Funnel Analysis

**SyntecxHub Data Analytics Internship — Project 3**

### 🌐 Live Dashboard
[View Live Dashboard](https://ecommerce-conversion-funnel-analysi.vercel.app/)

## Project overview

This project analyzes e-commerce event data to measure movement through the conversion funnel from browsing to purchase. The notebook includes data quality checks, funnel and drop-off metrics, device/channel/product-category comparisons, visualizations, and business recommendations.

## Live Dashboard

[View Live Dashboard](https://ecommerce-conversion-funnel-analysi.vercel.app/)

## Business problem

Potential customers leave at each step between browsing and purchasing. The business needs to understand how many sessions reach each stage, where losses are greatest, and which segments perform better so that conversion improvements can be prioritized.

## Objectives

- Inspect the supplied event dataset and check for missing and duplicate records.
- Measure the number of sessions reaching each funnel stage.
- Calculate overall and stage-to-stage conversion and drop-off rates.
- Identify the largest funnel losses and compare performance by device, channel, and product category.
- Present data-grounded business insights and recommendations.

## Tools used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Dataset description

The supplied `funnel_analysis_data.csv` contains **21,663 event records** and **10 columns** for **10,000 unique users and 10,000 unique sessions**. The recorded dates span **2025-10-01 through 2025-10-31**. The notebook reports no missing values and no duplicate rows.

| Column | Description |
| --- | --- |
| `User_ID` | User identifier |
| `Session_ID` | Session identifier |
| `Event` | Funnel event recorded |
| `Timestamp` | Event timestamp |
| `Device` | Device category |
| `Region` | Geographic region |
| `Channel` | Acquisition channel |
| `Product_Category` | Product category |
| `Revenue` | Revenue recorded for the event |
| `Bounce_Flag` | Bounce indicator |

## Funnel stages and conversion rates

Rates in the **Overall conversion** column use Browse sessions (10,000) as the denominator. **Stage-to-stage conversion** uses the preceding stage as its denominator.

| Funnel stage | Sessions | Overall conversion | Stage-to-stage conversion | Drop-off from prior stage | Drop-off rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Browse | 10,000 | 100.00% | — | — | — |
| Add to Cart | 7,059 | 70.59% | 70.59% | 2,941 | 29.41% |
| Checkout | 3,524 | 35.24% | 49.92% | 3,535 | 50.08% |
| Purchase | 1,080 | 10.80% | 30.65% | 2,444 | 69.35% |

The overall Browse-to-Purchase conversion rate is **10.80%**.

## Drop-off analysis and bottlenecks

- **Largest loss by session count:** Add to Cart → Checkout, with **3,535 sessions** lost (a **50.08%** drop-off from Add to Cart).
- **Largest drop-off rate and weakest stage-to-stage conversion:** Checkout → Purchase, with **2,444 sessions** lost, a **69.35%** drop-off and a **30.65%** conversion rate.
- Browse → Add to Cart loses **2,941 sessions** (a **29.41%** drop-off).

The cart-to-checkout transition has the greatest absolute loss, while the checkout-to-purchase transition has the highest proportional loss. Both represent opportunities for improvement.

## Visualizations

The original chart images below were exported from the notebook's existing executed outputs. The consolidated dashboard is generated from the supplied CSV by `create_dashboard.py`:

- [E-commerce funnel dashboard](visualizations/ecommerce_funnel_dashboard.png)
- [E-commerce conversion funnel](visualizations/ecommerce-conversion-funnel.png)
- [Stage-to-stage conversion](visualizations/stage-to-stage-conversion.png)
- [Session drop-off by transition](visualizations/funnel-drop-off.png)
- [Overall conversion by acquisition channel](visualizations/conversion-by-channel.png)
- [Overall conversion by product category](visualizations/conversion-by-product-category.png)
- [Purchase revenue distribution](visualizations/purchase-revenue-distribution.png)

## Static website dashboard

A separate responsive presentation website is available in `dashboard/`. It presents the verified analysis results and is a static frontend: no backend, authentication, or dashboard framework is required.

To serve the project locally from the project root:

```powershell
.\.venv\Scripts\python.exe -m http.server 8000
```

Open [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/) in a browser. For Vercel, select `dashboard` as the project root; the static entry point and Vercel configuration are included there. The site is not deployed.

## Actual key findings and business insights

- The funnel records **10,000 Browse**, **7,059 Add to Cart**, **3,524 Checkout**, and **1,080 Purchase** sessions.
- **Tablet** has the highest device-level overall conversion at **11.52%** (Mobile: **11.03%**; Desktop: **9.85%**).
- **Email** has the highest channel-level overall conversion at **11.21%** (Google Ads: **10.90%**; Social Media: **10.86%**; Organic: **10.23%**).
- **Electronics** has the highest product-category overall conversion at **11.19%** (Fashion: **10.96%**; Home: **10.92%**; Sports: **10.75%**; Beauty: **10.16%**).
- Purchase events total **$1,176,405.78** in revenue, with an average order value of **$1,089.26**.

These are findings from the supplied dataset and notebook; they should not be interpreted as proof of why any segment performs differently.

## Recommendations

- Improve the cart transition by clarifying cart contents and pricing, showing delivery charges and estimated arrival times earlier, and making the checkout call to action prominent.
- Reduce checkout abandonment by simplifying the process, offering guest checkout and multiple payment methods, minimizing form fields, and surfacing trust, returns, and delivery information near the purchase action.
- Investigate the stronger tablet, email, and Electronics results by comparing landing pages, offers, and user intent across segments; test successful patterns in weaker segments.
- Use A/B tests to measure changes in Add-to-Cart, Checkout, and Purchase conversion.

## Conclusion

The supplied data shows a **10.80% Browse-to-Purchase conversion rate**. The biggest loss by count occurs from Add to Cart to Checkout, and the weakest transition rate occurs from Checkout to Purchase. Prioritizing cart clarity and checkout simplicity, then evaluating changes with testing, is consistent with the observed funnel results.

## Project structure

```text
ecommerce-conversion-funnel-analysis/
├── Ecommerce_Conversion_Funnel_Analysis.ipynb
├── funnel_analysis_data.csv
├── create_dashboard.py
├── README.md
├── requirements.txt
├── .gitignore
├── dashboard/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── vercel.json
│   └── assets/
│       └── favicon.svg
├── visualizations/
│   ├── ecommerce-conversion-funnel.png
│   ├── ecommerce_funnel_dashboard.png
│   ├── stage-to-stage-conversion.png
│   ├── funnel-drop-off.png
│   ├── conversion-by-channel.png
│   ├── conversion-by-product-category.png
│   └── purchase-revenue-distribution.png
└── screenshots/
```

## How to run the notebook

From the project root, activate the existing `.venv` environment and install the listed dependencies if needed:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Then launch Jupyter and open the notebook:

```powershell
jupyter notebook Ecommerce_Conversion_Funnel_Analysis.ipynb
```

Select the `.venv` Python kernel if Jupyter prompts for a kernel. The notebook reads `funnel_analysis_data.csv` from the project root, so keep the notebook and CSV together.

To regenerate the dashboard image from the dataset without running or modifying the notebook:

```powershell
python create_dashboard.py
```

## Author

KUDUKA APPASI VAISHNAVI

GitHub: https://github.com/kavaishnavi7
