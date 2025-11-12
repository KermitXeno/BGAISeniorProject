# Alzheimer's Assessment System - Startup Guide

## 🚀 Quick Start Guide

### 1. Start ML Model Service
```bash
cd ModelTraining
python ModelAPI.py
```
*Runs on: http://localhost:5000*

### 2. Start FastAPI Backend  
```bash
cd backend-api
uvicorn main:app --port 8001 --reload
```
*Runs on: http://localhost:8001*
*API Docs: http://localhost:8001/docs*

### 3. Start React Frontend
```bash
cd frontend
npm start
```
*Runs on: http://localhost:3000*

### 4. Test Complete System
```bash
python test_full_system.py
```

## 📊 System Architecture

```
[Frontend: React]     [Backend: FastAPI]     [ML Service: Flask]
http://localhost:3000 → http://localhost:8001 → http://localhost:5000
      ↓                      ↓                       ↓
  User Interface      API Layer & Validation    AI/ML Models
  - Dashboard         - Data Processing        - BIO Model  
  - BIO Form          - File Handling          - MRI Model
  - MRI Upload        - Error Handling         - Model Inference
  - Results Display   - Response Formatting    
```

## 🧬 BIO Model Testing

**Sample Data (Your Test Case):**
- Gender: Female (0)
- Age: 75 years  
- Education: 12 years
- SES: 2.0
- MMSE: 18.0
- eTIV: 1479
- nWBV: 0.657
- ASF: 1.187

## 🧠 MRI Model Testing

Use demo image: `ModelTraining/AMRI/demoIMG/MildImpairment (1).jpg`

## 🔧 Troubleshooting

### Port Conflicts
- Frontend: Change port in package.json
- Backend: Use `--port XXXX` flag
- ML Service: Edit ModelAPI.py port

### Backend Issues
```bash
cd backend-api
python test_backend_simple.py  # Test backend structure
python test_complete.py        # Test with ML service
```

### Frontend Issues  
```bash
cd frontend
npm install  # Reinstall dependencies
npm start    # Start dev server
```

### ML Service Issues
- Ensure Keras model files exist in ModelTraining/
- Run training scripts if models missing
- Check Python environment has required packages

## 📁 Project Structure

```
BGAISeniorProject/
├── frontend/           # React UI application
│   ├── src/components/ # UI components
│   ├── public/         # Static assets
│   └── package.json    # Dependencies
├── backend-api/        # FastAPI service
│   ├── app/           # API modules
│   ├── main.py        # FastAPI app
│   └── test_*.py      # Test scripts
├── ModelTraining/     # ML models & service
│   ├── ModelAPI.py    # Flask ML service
│   ├── BIOFM/         # BIO model files
│   └── AMRI/          # MRI model files
└── test_full_system.py # Complete system test
```

## 🎯 Usage Workflow

1. **Access Dashboard**: Open http://localhost:3000
2. **Select Model**: Choose BIO or MRI analysis
3. **Input Data**: Fill form or upload image
4. **Get Results**: View AI analysis results
5. **Medical Review**: Consult healthcare professional

## ⚕️ Medical Disclaimer

This system is for research and educational purposes. Results should not replace professional medical diagnosis or treatment decisions.