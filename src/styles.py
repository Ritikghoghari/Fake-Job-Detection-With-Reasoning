def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        .stApp {
            background: #f8fafc;
            background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
            background-size: 20px 20px;
            color: #1e293b;
        }

        /* Card Styling */
        .custom-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #f1f5f9;
            margin-bottom: 20px;
        }
        
        .custom-card h2, .custom-card h3 {
            margin-top: 0;
        }

        /* Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 6px 16px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: 1rem;
        }

        .status-real { background-color: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .status-fake { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
        .status-suspicious { background-color: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }
        .status-info { background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }

        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }
        
        .metric-item {
            background: #f8fafc;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: #64748b;
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 4px;
        }

        /* Progress Bar Custom */
        .tamper-wrapper {
            background: #e2e8f0;
            border-radius: 8px;
            height: 10px;
            width: 100%;
            margin-top: 8px;
            overflow: hidden;
        }
        .tamper-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #2563eb);
            border-radius: 8px;
            transition: width 0.5s ease;
        }
        .tamper-fill.high {
            background: linear-gradient(90deg, #ef4444, #dc2626);
        }

        /* Keywords */
        .keyword-tag {
            background: #fff1f2;
            border: 1px solid #fecaca;
            color: #be123c;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            margin: 0 6px 6px 0;
            display: inline-block;
            font-weight: 500;
        }
        
        /* Typography overrides */
        h1 {
            background: linear-gradient(to right, #0f172a, #334155);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }
        
        /* Input area focus */
        .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* Primary Button */
        div.stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            padding: 0.6rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
            transition: all 0.2s;
            width: 100%;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
            border: none;
        }
    </style>
    """
