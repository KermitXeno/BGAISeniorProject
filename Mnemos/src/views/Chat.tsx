import React, { useState, useRef, useCallback } from "react";
import { useDropzone } from 'react-dropzone';
import { medicalAPI, MRIAnalysisResult, BiomarkerAnalysisResult, BiomarkerData, formatConfidence, getConfidenceColor, getSeverityLevel } from '../utils/api';

interface Message {
  id: string;
  sender: "user" | "ai";
  text: string;
  timestamp: Date;
  files?: File[];
  analysisResult?: MRIAnalysisResult | BiomarkerAnalysisResult;
  analysisType?: 'mri' | 'biomarker';
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'ai',
      text: 'Hello! I\'m here to help you understand your medical reports. You can upload MRI scans or ask me any questions about your health data.',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showBiomarkerForm, setShowBiomarkerForm] = useState(false);
  const [biomarkerData, setBiomarkerData] = useState<BiomarkerData>({
    gender: 0,
    age: 65,
    education: 12,
    ses: 2,
    mmse: 28,
    cdr: 0,
    etiv: 1500,
    nwbv: 0.8
  });

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setUploadedFiles(prev => [...prev, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
      'application/dicom': ['.dcm'],
      'application/octet-stream': ['.dicom']
    },
    multiple: true,
    noClick: true
  });

  const handleSend = async () => {
    if (input.trim() === "" && uploadedFiles.length === 0) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      sender: "user",
      text: input,
      timestamp: new Date(),
      files: uploadedFiles.length > 0 ? uploadedFiles : undefined
    };

    setMessages(prev => [...prev, newMessage]);
    setInput("");
    const filesToAnalyze = [...uploadedFiles];
    setUploadedFiles([]);
    setIsTyping(true);
    setIsAnalyzing(true);

    try {
      // Check if we have medical image files to analyze
      const imageFiles = filesToAnalyze.filter(file => 
        file.type.startsWith('image/') || file.name.toLowerCase().includes('.dcm')
      );

      if (imageFiles.length > 0) {
        // Analyze the first image file
        const analysisResult = await medicalAPI.analyzeMRI(imageFiles[0]);
        
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          sender: "ai",
          text: `I've analyzed your MRI scan. Here are the findings:

**Diagnosis**: ${analysisResult.prediction}
**Confidence**: ${formatConfidence(analysisResult.confidence)}

**Detailed Analysis**:
${Object.entries(analysisResult.all_scores)
  .map(([condition, score]) => `• ${condition}: ${formatConfidence(score)}`)
  .join('\n')}

Based on these results, ${getSeverityLevel(analysisResult.prediction) === 'low' 
  ? 'the scan shows minimal concerns. Continue with regular monitoring and follow your doctor\'s recommendations.'
  : getSeverityLevel(analysisResult.prediction) === 'medium'
  ? 'there are some findings that warrant attention. Please discuss these results with your healthcare provider for next steps.'
  : 'the scan shows significant findings. It\'s important to consult with your neurologist promptly for comprehensive evaluation and treatment planning.'
}

Would you like me to explain any specific aspects of these findings or answer any questions about your results?`,
          timestamp: new Date(),
          analysisResult,
          analysisType: 'mri'
        };

        setMessages(prev => [...prev, aiResponse]);
      } else {
        // General AI response for text-only messages
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          sender: "ai",
          text: input.toLowerCase().includes('biomarker') || input.toLowerCase().includes('blood') 
            ? "I can help analyze biomarker data! Please use the 'Biomarker Analysis' button below to enter your lab values, and I'll provide insights about cognitive health indicators."
            : "I understand your question. Let me help you with that. For detailed medical analysis, you can:\n\n• Upload MRI scans for brain imaging analysis\n• Use the biomarker analysis for lab results\n• Ask specific questions about your medical reports\n\nWhat would you like to explore?",
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, aiResponse]);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: "I'm sorry, there was an error analyzing your file. Please make sure the image is a valid medical scan (JPEG, PNG, or DICOM format) and try again. If the problem persists, please check that the AI analysis service is running.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
      setIsAnalyzing(false);
    }
  };

  const handleBiomarkerAnalysis = async () => {
    setIsAnalyzing(true);
    setIsTyping(true);
    setShowBiomarkerForm(false);

    // Add user message with biomarker data
    const userMessage: Message = {
      id: Date.now().toString(),
      sender: "user",
      text: `Biomarker Analysis Request:
• Gender: ${biomarkerData.gender === 0 ? 'Male' : 'Female'}
• Age: ${biomarkerData.age} years
• Education: ${biomarkerData.education} years
• Socioeconomic Status: ${biomarkerData.ses}
• MMSE Score: ${biomarkerData.mmse}/30
• CDR: ${biomarkerData.cdr}
• ETIV: ${biomarkerData.etiv}
• NWBV: ${biomarkerData.nwbv}`,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const analysisResult = await medicalAPI.analyzeBiomarkers(biomarkerData);
      
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: `I've analyzed your biomarker data. Here are the findings:

**Cognitive Assessment**: ${analysisResult.prediction}
**Confidence**: ${formatConfidence(analysisResult.confidence)}

**Detailed Probability Scores**:
${Object.entries(analysisResult.all_scores)
  .map(([condition, score]) => `• ${condition}: ${formatConfidence(score)}`)
  .join('\n')}

**Key Insights**:
• **MMSE Score (${biomarkerData.mmse}/30)**: ${biomarkerData.mmse >= 28 ? 'Excellent cognitive function' : biomarkerData.mmse >= 24 ? 'Mild cognitive concerns' : 'Significant cognitive concerns - please consult your physician'}
• **CDR Rating (${biomarkerData.cdr})**: ${biomarkerData.cdr === 0 ? 'No dementia symptoms' : biomarkerData.cdr === 0.5 ? 'Very mild symptoms' : 'Clinical attention needed'}
• **Brain Volume (NWBV: ${biomarkerData.nwbv})**: ${biomarkerData.nwbv >= 0.8 ? 'Normal brain volume' : 'Reduced brain volume detected'}

**Recommendations**:
${getSeverityLevel(analysisResult.prediction) === 'low' 
  ? '• Continue regular health monitoring\n• Maintain healthy lifestyle habits\n• Regular cognitive assessments'
  : getSeverityLevel(analysisResult.prediction) === 'medium'
  ? '• Schedule follow-up with neurologist\n• Consider cognitive training exercises\n• Monitor symptoms closely'
  : '• Urgent consultation with neurologist recommended\n• Comprehensive neuropsychological evaluation\n• Discuss treatment options with healthcare team'
}

Would you like me to explain any of these biomarkers or discuss what these results mean for cognitive health?`,
        timestamp: new Date(),
        analysisResult,
        analysisType: 'biomarker'
      };

      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Biomarker analysis error:', error);
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: "I'm sorry, there was an error analyzing your biomarker data. Please check that all values are entered correctly and that the AI analysis service is running. You can try again or contact support if the issue persists.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
      setIsAnalyzing(false);
    }
  };

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-background py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-primary rounded-full shadow-primary mb-4">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold mb-2 text-gradient-primary">
            AI Medical Assistant
          </h1>
          <p className="text-lg text-slate-600">
            Upload your medical scans and chat with our AI for personalized insights
          </p>
        </div>

        {/* Chat Container */}
        <div className="card max-w-4xl mx-auto">
          {/* Messages Area */}
          <div className="h-96 overflow-y-auto mb-6 space-y-4 p-4 bg-gradient-to-b from-background to-secondary-50 rounded-lg border border-secondary-200/30">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"} animate-slide-up`}
              >
                <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                  message.sender === "user"
                    ? "bg-primary-500 text-white rounded-br-sm"
                    : "bg-white border border-secondary-200 text-slate-700 rounded-bl-sm shadow-sm"
                }`}>
                  {message.files && message.files.length > 0 && (
                    <div className="mb-2 space-y-1">
                      {message.files.map((file, index) => (
                        <div key={index} className="flex items-center space-x-2 text-xs opacity-90">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                          </svg>
                          <span className="truncate">{file.name}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  <p className="text-sm leading-relaxed">{message.text}</p>
                  <p className={`text-xs mt-2 ${
                    message.sender === "user" ? "text-white/70" : "text-slate-400"
                  }`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            ))}
            
            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start animate-fade-in">
                <div className="bg-white border border-secondary-200 px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-secondary-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-secondary-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-secondary-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* File Upload Area */}
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-4 mb-4 transition-all duration-200 ${
              isDragActive 
                ? 'border-primary-500 bg-primary-50' 
                : 'border-secondary-300 hover:border-primary-400 hover:bg-secondary-50'
            } ${uploadedFiles.length > 0 ? 'border-accent-400 bg-accent-50' : ''}`}
          >
            <input {...getInputProps()} />
            
            {uploadedFiles.length > 0 ? (
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-sm text-accent-600 font-medium">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>{uploadedFiles.length} file(s) ready to send</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {uploadedFiles.map((file, index) => (
                    <div key={index} className="flex items-center space-x-2 bg-white px-3 py-1 rounded-full border border-accent-200 text-xs">
                      <span className="truncate max-w-32">{file.name}</span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          removeFile(index);
                        }}
                        className="text-red-400 hover:text-red-600 transition-colors duration-200"
                      >
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center">
                <svg className="w-8 h-8 mx-auto text-secondary-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <p className="text-sm text-slate-600">
                  {isDragActive ? "Drop files here..." : "Drag & drop medical files here, or click to browse"}
                </p>
                <p className="text-xs text-slate-400 mt-1">
                  Supports: DICOM (.dcm), JPEG, PNG
                </p>
              </div>
            )}
          </div>

          {/* Biomarker Analysis Form */}
          {showBiomarkerForm && (
            <div className="bg-gradient-to-r from-secondary-50 to-accent-50 border border-secondary-200 rounded-lg p-6 mb-4">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-slate-700 flex items-center space-x-2">
                  <svg className="w-5 h-5 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                  <span>Biomarker Analysis</span>
                </h3>
                <button
                  onClick={() => setShowBiomarkerForm(false)}
                  className="text-slate-400 hover:text-slate-600 transition-colors duration-200"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Gender</label>
                  <select
                    value={biomarkerData.gender}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, gender: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value={0}>Male</option>
                    <option value={1}>Female</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Age (years)</label>
                  <input
                    type="number"
                    value={biomarkerData.age}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, age: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    min="18" max="120"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Education (years)</label>
                  <input
                    type="number"
                    value={biomarkerData.education}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, education: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    min="0" max="30"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">SES</label>
                  <input
                    type="number"
                    value={biomarkerData.ses}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, ses: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    min="1" max="5" step="0.1"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">MMSE Score</label>
                  <input
                    type="number"
                    value={biomarkerData.mmse}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, mmse: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    min="0" max="30"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">CDR</label>
                  <select
                    value={biomarkerData.cdr}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, cdr: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value={0}>0 (Normal)</option>
                    <option value={0.5}>0.5 (Very Mild)</option>
                    <option value={1}>1 (Mild)</option>
                    <option value={2}>2 (Moderate)</option>
                    <option value={3}>3 (Severe)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">eTIV</label>
                  <input
                    type="number"
                    value={biomarkerData.etiv}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, etiv: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    min="1000" max="2500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">nWBV</label>
                  <input
                    type="number"
                    value={biomarkerData.nwbv}
                    onChange={(e) => setBiomarkerData(prev => ({ ...prev, nwbv: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-secondary-200 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    min="0.5" max="1.0" step="0.001"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowBiomarkerForm(false)}
                  className="btn-outline btn-sm"
                >
                  Cancel
                </button>
                <button
                  onClick={handleBiomarkerAnalysis}
                  disabled={isAnalyzing}
                  className="btn-primary btn-sm flex items-center space-x-2"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      <span>Analyze</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="flex space-x-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about your medical reports or describe your symptoms..."
                className="input pr-12 text-sm"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
              />
              <button
                onClick={() => (document.querySelector('input[type="file"]') as HTMLInputElement)?.click()}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-secondary-400 hover:text-primary-500 transition-colors duration-200"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
              </button>
            </div>
            <button
              onClick={handleSend}
              disabled={input.trim() === "" && uploadedFiles.length === 0}
              className="btn-primary px-6 py-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-primary hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              <span className="hidden sm:inline">Send</span>
            </button>
            <button
              onClick={() => setShowBiomarkerForm(!showBiomarkerForm)}
              className="btn-secondary px-4 py-2 flex items-center space-x-2 shadow-secondary hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
              title="Biomarker Analysis"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
              <span className="hidden md:inline">Biomarkers</span>
            </button>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="card text-center hover:shadow-primary transition-all duration-300 transform hover:-translate-y-1">
            <div className="w-12 h-12 bg-primary-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-700 mb-2">Smart Analysis</h3>
            <p className="text-slate-600 text-sm">AI-powered interpretation of medical scans and reports</p>
          </div>

          <div className="card text-center hover:shadow-accent transition-all duration-300 transform hover:-translate-y-1">
            <div className="w-12 h-12 bg-secondary-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-700 mb-2">Easy Conversations</h3>
            <p className="text-slate-600 text-sm">Natural language chat interface for medical questions</p>
          </div>

          <div className="card text-center hover:shadow-accent transition-all duration-300 transform hover:-translate-y-1">
            <div className="w-12 h-12 bg-accent-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <svg className="w-6 h-6 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-700 mb-2">Secure & Private</h3>
            <p className="text-slate-600 text-sm">HIPAA-compliant data handling and encryption</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;