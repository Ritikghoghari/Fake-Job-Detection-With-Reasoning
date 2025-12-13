def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: #e2e8f0; /* Light text for dark mode */
            background-color: #0f172a; /* Dark Slate background */
        }
        
        .stApp {
            background-color: #0f172a;
            background-image: radial-gradient(#1e293b 1px, transparent 1px);
            background-size: 24px 24px;
        }

        /* Card Styling - Dark Mode */
        .custom-card {
            background: #1e293b; /* Slate-800 */
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            border: 1px solid #334155; /* Slate-700 */
            margin-bottom: 24px;
        }
        
        .custom-card h3 {
            margin-top: 0;
            color: #f8fafc;
            font-weight: 700;
        }
        
        /* Text Colors */
        p, div, span {
            color: #cbd5e1; /* Slate-300 */
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
             color: #f8fafc !important;
        }
        
        h1 {
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }

        /* Status Badges - Dark Mode Adapted */
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 18px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 1.2rem;
            color: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .status-real { background-color: #15803d; border: 1px solid #22c55e; color: #dcfce7; }
        .status-fake { background-color: #b91c1c; border: 1px solid #f87171; color: #fee2e2; }
        .status-suspicious { background-color: #c2410c; border: 1px solid #fb923c; color: #ffedd5; }
        .status-info { background-color: #0369a1; border: 1px solid #38bdf8; color: #e0f2fe; }

        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }
        
        .metric-item {
            background: #0f172a; /* Slate-900 */
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #334155;
        }
        
        .metric-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: #f8fafc;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: #94a3b8;
            text-transform: uppercase;
            font-weight: 700;
            margin-top: 6px;
        }

        /* Progress Bar Custom */
        .tamper-wrapper {
            background: #334155;
            border-radius: 8px;
            height: 12px;
            width: 100%;
            margin-top: 8px;
            overflow: hidden;
            border: 1px solid #475569;
        }
        .tamper-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
            border-radius: 8px;
            transition: width 0.5s ease;
        }
        .tamper-fill.high {
            background: linear-gradient(90deg, #ef4444, #f87171);
        }

        /* Keywords */
        .keyword-tag {
            background: #450a0a; /* Dark red bg */
            border: 1px solid #7f1d1d;
            color: #fca5a5;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            margin: 0 6px 6px 0;
            display: inline-block;
            font-weight: 600;
        }
        
        /* Input area focus */
        .stTextArea textarea {
            background-color: #1e293b;
            border: 1px solid #334155;
            color: #f8fafc;
        }
        .stTextArea textarea:focus {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.3) !important;
        }
        .stTextArea label {
            color: #e2e8f0 !important;
        }
        
        /* Primary Button */
        div.stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: 1px solid #1e40af;
            padding: 0.7rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.2s;
            width: 100%;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -3px rgba(37, 99, 235, 0.4);
            border-color: #60a5fa;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a; 
        }
        ::-webkit-scrollbar-thumb {
            background: #475569; 
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b; 
        }
    </style>
    """
