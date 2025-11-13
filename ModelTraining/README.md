# 🏥 Mnemos AI Model Training Guide

## Quick Start (Test the Integration First)

### 1. Test with Mock API (Immediate Testing)
```bash
# Navigate to ModelTraining directory
cd ModelTraining

# Install minimal dependencies for testing
pip install flask flask-cors numpy

# Run test API (uses mock predictions)
python ModelAPI_test.py
```

Then test your frontend at http://localhost:3000 - it will work with mock AI responses!

---

## Full Setup (Real AI Models)

### 2. Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Or install manually:
pip install tensorflow keras numpy pandas matplotlib scikit-learn flask flask-cors pillow
```

### 3. Set Up Training Data

#### For MRI Model:
1. Download Alzheimer's MRI dataset (or use your own medical images)
2. Organize data structure:
```
ModelTraining/AMRI/data/Combined Dataset/
├── train/
│   ├── Mild Impairment/
│   ├── Moderate Impairment/
│   ├── No Impairment/
│   └── Very Mild Impairment/
└── test/
    ├── Mild Impairment/
    ├── Moderate Impairment/
    ├── No Impairment/
    └── Very Mild Impairment/
```

#### For Biomarker Model:
1. Place CSV files in `ModelTraining/BIOFM/data/`:
   - `oasis_longitudinal.csv`
   - `oasis_cross-sectional.csv` (optional)

### 4. Train the Models

#### Option A: Automated Setup
```bash
# Run the setup script (recommended)
python setup_models.py
```

#### Option B: Manual Training
```bash
# Train MRI model (30-60 minutes)
cd AMRI
python TrainMRI.py

# Train Biomarker model (5-15 minutes)
cd ../BIOFM
python TrainBIO.py

# Return to main directory
cd ..
```

### 5. Run the Real API
```bash
# After training is complete
python ModelAPI.py
```

---

## 🔧 Troubleshooting

### Common Issues:

1. **"No module named 'tensorflow'"**
   ```bash
   pip install tensorflow>=2.13.0
   ```

2. **"No module named 'flask_cors'"**
   ```bash
   pip install flask-cors
   ```

3. **CUDA/GPU Issues**
   ```bash
   # For CPU-only (slower but more compatible)
   pip install tensorflow-cpu
   ```

4. **Memory Issues During Training**
   - Reduce batch size in training scripts
   - Close other applications
   - Use CPU version if GPU memory is limited

5. **Data Not Found Errors**
   - Check data directory structure
   - Ensure CSV files are in correct locations
   - Verify image file formats (JPG, PNG supported)

---

## 🎯 Testing Your Setup

### 1. API Health Check:
```bash
# Test if API is running
curl http://localhost:5000/health
```

### 2. Frontend Integration:
1. Start your React app: `npm run dev`
2. Go to Chat page
3. Try uploading an image or using biomarker form
4. Check browser developer console for any errors

### 3. Direct API Testing:
```bash
# Test MRI endpoint (replace with actual image file)
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5000/predictMRI

# Test Biomarker endpoint
curl -X POST -H "Content-Type: application/json" \
     -d '{"data": [0, 75, 12, 2.0, 18.0, 1479, 0.657, 1.187]}' \
     http://localhost:5000/predictBIO
```

---

## 📊 Model Information

### MRI Model (AMRIGENETV1.keras):
- **Input**: 128x128 RGB images
- **Architecture**: CNN with transfer learning
- **Output**: 4 classes (No/Very Mild/Mild/Moderate Impairment)
- **Training Time**: ~30-60 minutes

### Biomarker Model (BIOFMGENETV1.keras):
- **Input**: 8 numerical features
  1. Gender (0=Male, 1=Female)
  2. Age (years)
  3. Education (years)
  4. Socioeconomic Status (1-5)
  5. MMSE Score (0-30)
  6. CDR (0, 0.5, 1, 2, 3)
  7. eTIV (Total Intracranial Volume)
  8. nWBV (Normalized Whole Brain Volume)
- **Architecture**: Dense neural network
- **Output**: 4 classes (No/Very Mild/Mild/Moderate Impairment)
- **Training Time**: ~5-15 minutes

---

## 🚀 Production Deployment

For production use:
1. Use environment variables for configuration
2. Add authentication/authorization
3. Implement rate limiting
4. Use HTTPS
5. Add comprehensive logging
6. Consider model versioning
7. Add monitoring and health checks

---

## 📞 Support

If you encounter issues:
1. Check the error logs
2. Verify data directory structure
3. Ensure all dependencies are installed
4. Test with the mock API first
5. Check Python version compatibility (3.8+)