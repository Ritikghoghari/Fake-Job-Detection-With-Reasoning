def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: #0f172a; /* Darker default text */
        }
        
        .stApp {
            /* Slightly darker background to make white cards pop */
            background: #f1f5f9; 
            background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
            background-size: 24px 24px;
        }

        /* Card Styling - Reinforced contrast */
        .custom-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #e2e8f0; /* Darker border */
            margin-bottom: 24px;
        }
        
        .custom-card h3 {
            margin-top: 0;
            color: #1e293b;
            font-weight: 700;
        }
        
        /* Text Contrast Improvements */
        p, div {
            color: #334155; /* Slightly softer than black but readable */
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
             color: #0f172a !important;
        }

        /* Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 18px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .status-real { background-color: #dcfce7; color: #14532d; border: 1px solid #86efac; }
        .status-fake { background-color: #fee2e2; color: #7f1d1d; border: 1px solid #fca5a5; }
        .status-suspicious { background-color: #ffedd5; color: #7c2d12; border: 1px solid #fdba74; }
        .status-info { background-color: #e0f2fe; color: #0c4a6e; border: 1px solid #7dd3fc; }

        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }
        
        .metric-item {
            background: #f8fafc;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #cbd5e1; /* Stronger border */
        }
        
        .metric-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: #0f172a;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: #475569; /* Darker gray */
            text-transform: uppercase;
            font-weight: 700;
            margin-top: 6px;
        }

        /* Progress Bar Custom */
        .tamper-wrapper {
            background: #cbd5e1; /* Darker track */
            border-radius: 8px;
            height: 12px;
            width: 100%;
            margin-top: 8px;
            overflow: hidden;
            border: 1px solid #94a3b8;
        }
        .tamper-fill {
            height: 100%;
            background: linear-gradient(90deg, #2563eb, #1d4ed8);
            border-radius: 8px;
            transition: width 0.5s ease;
        }
        .tamper-fill.high {
            background: linear-gradient(90deg, #ef4444, #b91c1c);
        }

        /* Keywords */
        .keyword-tag {
            background: #fff1f2;
            border: 1px solid #fda4af;
            color: #881337;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            margin: 0 6px 6px 0;
            display: inline-block;
            font-weight: 600;
        }
        
        /* Typography overrides */
        h1 {
            color: #0f172a !important;
            font-weight: 800 !important;
        }
        
        /* Input area focus */
        .stTextArea textarea {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            color: #0f172a;
        }
        .stTextArea textarea:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        }
        
        /* Primary Button */
        div.stButton > button {
            background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%); /* Darker blue */
            color: white;
            border: 1px solid #172554;
            padding: 0.7rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.3);
            transition: all 0.2s;
            width: 100%;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -3px rgba(30, 58, 138, 0.4);
            background: linear-gradient(135deg, #1e3a8a 0%, #172554 100%);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9; 
        }
        ::-webkit-scrollbar-thumb {
            background: #94a3b8; 
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b; 
        }
    </style>
    """
