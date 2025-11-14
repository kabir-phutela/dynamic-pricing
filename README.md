# Dynamic Pricing Strategy  
*Forecasting product/service prices in real-time using market demand, customer behaviour, weather, and festival signals*

## 🚀 Project Overview  
This project implements a **data-driven dynamic pricing solution** using Python, machine learning (XGBoost), and cloud deployment. It enables businesses to adjust product or service prices in real time based on datasets of historical sales, weather metrics, festival events and competitor activity. The solution includes:  
- A trained ML model with an RMSE of **26.61** on the test set.  
- A **Flask API** for serving live pricing predictions.  
- A **Streamlit frontend** enabling intuitive user interaction.  
- A **Power BI dashboard** for visualizing actual vs. predicted prices and supporting data-driven decisions.

## 🛠 Technology Stack  
- **Languages / Frameworks:** Python, Jupyter Notebook  
- **ML Library:** XGBoost  
- **Web/API:** Flask  
- **Frontend UI:** Streamlit  
- **Visualization & Dashboard:** Power BI  
- **Cloud/Deployment:** AWS (Amazo
n Web Services)  
- **Supporting Tools:** Pandas, NumPy, Scikit-learn, Pickle for model serialization

## 🧭 Getting Started  
### 1. Clone the Repo  

1) git clone https://github.com/kabir-phutela/dynamic-pricing.git  
cd dynamic-pricing

2) 2. Set Up Virtual Environment & Install Dependencies
  
      python3 -m venv venv  
source venv/bin/activate     # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  


3) Running the Flask API

   python app.py  



