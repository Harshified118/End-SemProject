import zipfile
import xml.etree.ElementTree as ET
import copy
import os

# Register all namespaces found in PRD_Template_Corrected.docx
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
    'w16': 'http://schemas.microsoft.com/office/word/2018/wordml',
    'w16cex': 'http://schemas.microsoft.com/office/word/2018/wordml/cex',
    'w16cid': 'http://schemas.microsoft.com/office/word/2016/wordml/cid',
    'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
    'cx': 'http://schemas.microsoft.com/office/drawing/2014/chartex',
    'cx1': 'http://schemas.microsoft.com/office/drawing/2015/9/8/chartex',
    'cx2': 'http://schemas.microsoft.com/office/drawing/2015/10/21/chartex',
    'cx3': 'http://schemas.microsoft.com/office/drawing/2016/5/9/chartex',
    'cx4': 'http://schemas.microsoft.com/office/drawing/2016/5/10/chartex',
    'cx5': 'http://schemas.microsoft.com/office/drawing/2016/5/11/chartex',
    'cx6': 'http://schemas.microsoft.com/office/drawing/2016/5/12/chartex',
    'cx7': 'http://schemas.microsoft.com/office/drawing/2016/5/13/chartex',
    'cx8': 'http://schemas.microsoft.com/office/drawing/2016/5/14/chartex',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'aink': 'http://schemas.microsoft.com/office/drawing/2016/ink',
    'am3d': 'http://schemas.microsoft.com/office/drawing/2017/model3d',
    'o': 'urn:schemas-microsoft-com:office:office',
    'oel': 'http://schemas.microsoft.com/office/2019/extlst',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'v': 'urn:schemas-microsoft-com:vml',
    'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w10': 'urn:schemas-microsoft-com:office:word',
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

W_NS = NAMESPACES['w']

def make_para(runs_data, space_after='40', line_spacing='240', font_name='Aptos'):
    """
    runs_data: list of tuples: (text, is_bold, color, font_size, is_italic, is_code)
    """
    p = ET.Element(f'{{{W_NS}}}p')
    pPr = ET.SubElement(p, f'{{{W_NS}}}pPr')
    if space_after or line_spacing:
        s_attrib = {}
        if space_after:
            s_attrib[f'{{{W_NS}}}after'] = str(space_after)
        if line_spacing:
            s_attrib[f'{{{W_NS}}}line'] = str(line_spacing)
            s_attrib[f'{{{W_NS}}}lineRule'] = 'auto'
        ET.SubElement(pPr, f'{{{W_NS}}}spacing', s_attrib)
        
    for r_info in runs_data:
        text = r_info[0]
        is_bold = r_info[1] if len(r_info) > 1 else False
        color = r_info[2] if len(r_info) > 2 else None
        sz = r_info[3] if len(r_info) > 3 else '17'
        is_italic = r_info[4] if len(r_info) > 4 else False
        is_code = r_info[5] if len(r_info) > 5 else False

        r = ET.SubElement(p, f'{{{W_NS}}}r')
        rPr = ET.SubElement(r, f'{{{W_NS}}}rPr')
        
        f_name = 'Consolas' if is_code else font_name
        if f_name:
            ET.SubElement(rPr, f'{{{W_NS}}}rFonts', {
                f'{{{W_NS}}}ascii': f_name,
                f'{{{W_NS}}}hAnsi': f_name,
                f'{{{W_NS}}}cs': f_name
            })
        if is_bold:
            ET.SubElement(rPr, f'{{{W_NS}}}b')
        if is_italic:
            ET.SubElement(rPr, f'{{{W_NS}}}i')
        if color:
            ET.SubElement(rPr, f'{{{W_NS}}}color', {f'{{{W_NS}}}val': color})
        if sz:
            ET.SubElement(rPr, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': str(sz)})
            
        t = ET.SubElement(r, f'{{{W_NS}}}t')
        if text.startswith(' ') or text.endswith(' ') or '  ' in text or '\n' in text:
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
        
    return p

def set_cell_content(tc, paragraphs_data, font_name='Aptos'):
    for child in list(tc):
        if child.tag.endswith('tcPr'):
            continue
        tc.remove(child)
        
    for p_runs in paragraphs_data:
        p = make_para(p_runs, font_name=font_name)
        tc.append(p)

def set_cell_simple(tc, text, is_bold=False, color=None, sz='17', font_name='Aptos'):
    lines = text.split('\n')
    paras = []
    for line in lines:
        paras.append([(line, is_bold, color, sz, False, False)])
    set_cell_content(tc, paras, font_name=font_name)

def update_callout_box(tbl, title, body_items, font_name='Aptos'):
    tc = tbl.find(f'.//{{{W_NS}}}tc')
    for child in list(tc):
        if child.tag.endswith('tcPr'):
            continue
        tc.remove(child)
        
    p_title = make_para([(title, True, '17324D', '18', False, False)], space_after='60', font_name=font_name)
    tc.append(p_title)
    
    for item in body_items:
        if isinstance(item, str):
            p_elem = make_para([(item, False, None, '18', False, False)], space_after='60', line_spacing='252', font_name=font_name)
            tc.append(p_elem)
        elif isinstance(item, tuple) and item[0] == 'code':
            for line in item[1].split('\n'):
                p_elem = make_para([(line, False, '17324D', '15', False, True)], space_after='10', line_spacing='200')
                tc.append(p_elem)
        elif isinstance(item, list):
            p_elem = make_para(item, space_after='60', line_spacing='252', font_name=font_name)
            tc.append(p_elem)

def populate_table_rows(tbl, data_rows, bold_first_col=True, font_name='Aptos'):
    rows = tbl.findall(f'{{{W_NS}}}tr')
    header_row = rows[0]
    
    r1 = copy.deepcopy(rows[1])
    r2 = copy.deepcopy(rows[2]) if len(rows) > 2 else copy.deepcopy(rows[1])
    
    for tc in r1.findall(f'{{{W_NS}}}tc'):
        tcPr = tc.find(f'{{{W_NS}}}tcPr')
        if tcPr is not None:
            shd = tcPr.find(f'{{{W_NS}}}shd')
            if shd is not None and shd.attrib.get(f'{{{W_NS}}}fill', '').upper() == 'F6F8FA':
                tcPr.remove(shd)
                
    for tc in r2.findall(f'{{{W_NS}}}tc'):
        tcPr = tc.find(f'{{{W_NS}}}tcPr')
        if tcPr is not None:
            shd = tcPr.find(f'{{{W_NS}}}shd')
            if shd is None:
                shd = ET.SubElement(tcPr, f'{{{W_NS}}}shd', {
                    f'{{{W_NS}}}val': 'clear',
                    f'{{{W_NS}}}color': 'auto',
                    f'{{{W_NS}}}fill': 'F6F8FA'
                })
            else:
                shd.set(f'{{{W_NS}}}fill', 'F6F8FA')
                
    for r in rows[1:]:
        tbl.remove(r)
        
    for r_idx, row_values in enumerate(data_rows):
        template_r = r1 if (r_idx % 2 == 0) else r2
        new_r = copy.deepcopy(template_r)
        tcs = new_r.findall(f'{{{W_NS}}}tc')
        
        for c_idx, val in enumerate(row_values):
            if c_idx < len(tcs):
                tc = tcs[c_idx]
                if isinstance(val, str):
                    is_bold = bold_first_col and (c_idx == 0)
                    color = '17324D' if is_bold else None
                    set_cell_simple(tc, val, is_bold=is_bold, color=color, sz='17', font_name=font_name)
                elif isinstance(val, list):
                    if val and isinstance(val[0], list):
                        set_cell_content(tc, val, font_name=font_name)
                    else:
                        set_cell_content(tc, [val], font_name=font_name)
        tbl.append(new_r)

def build_docx():
    template_path = 'PRD_Template_Corrected.docx'
    output_root = 'PRD_DropOrCop_Group_G.docx'
    output_docs = 'docs/PRD_DropOrCop_Group_G.docx'
    output_updated = 'Updated_PRD_DropOrCop_Group_G.docx'
    
    with zipfile.ZipFile(template_path, 'r') as z_in:
        all_files = {name: z_in.read(name) for name in z_in.namelist()}
        
    tree = ET.fromstring(all_files['word/document.xml'])
    body = tree.find(f'{{{W_NS}}}body')
    
    # Title paragraph
    p1 = body[1]
    t1 = p1.find(f'.//{{{W_NS}}}t')
    if t1 is not None and t1.text == 'PROJECT REQUIREMENTSDOCUMENT (PRD)':
        t1.text = 'PROJECT REQUIREMENTS DOCUMENT (PRD)'
        
    # Table 5: Document Metadata
    tbl5 = body[5]
    tbl5_rows = tbl5.findall(f'{{{W_NS}}}tr')
    set_cell_simple(tbl5_rows[4].findall(f'{{{W_NS}}}tc')[1], 'Department of Computer Science & Engineering', is_bold=False, sz='17')
    set_cell_simple(tbl5_rows[5].findall(f'{{{W_NS}}}tc')[1], 'B.Tech in Computer Science & Engineering / End-Semester Project Assessment (November 2026)', is_bold=False, sz='17')
    set_cell_simple(tbl5_rows[6].findall(f'{{{W_NS}}}tc')[1], 'Revised Working Draft for Faculty Approval (Resubmission Draft - 16 November 2026)', is_bold=False, sz='17')
    
    # Table 17: Team and Project Details
    tbl17 = body[17]
    tbl17_data = [
        ['Group ID', 'Group G'],
        ['Assigned project title', 'DropOrCop: Sneaker & Streetwear Resale Profit Predictor'],
        ['Programme / Course / Semester', 'B.Tech in Computer Science & Engineering / End-Semester Assessment (November 2026)'],
        ['Faculty mentor', '[To be assigned by Faculty / Department Allocation]'],
        ['Team leader / coordinator', 'Harsh Kumar (Sl. No. 31)'],
        ['PRD Submission Date', '16-11-2026 (Resubmission Draft)'],
    ]
    populate_table_rows(tbl17, tbl17_data, bold_first_col=True)
    
    # Table 20: Team Member Register
    tbl20 = body[20]
    tbl20_data = [
        ['1', [[('Harsh Kumar', True, '17324D', '17'), (' (Sl. No. 31)', False, None, '17')]], 'Team Leader & ML Lead: Data Ingestion, Feature Preprocessing & Single-Model Pipeline (Phases 1, 2, 3)'],
        ['2', [[('Anamika Ghosh', True, '17324D', '17'), (' (Sl. No. 32)', False, None, '17')]], 'Evaluation Lead: Test set evaluation (MAPE/MAE) & sample verification checks (Phase 4)'],
        ['3', [[('[Vacant / Unallocated]', True, '777777', '17'), (' (Sl. No. 33)', False, '777777', '17')]], 'Shared Group Support & Integration Testing (Phase 7)'],
        ['4', [[('Sinthoiba Kangjam', True, '17324D', '17'), (' (Sl. No. 34)', False, None, '17')]], 'API & Backend Lead: High-throughput FastAPI microservice (/predict, /health, /brands), Pydantic validation, CORS, model serving (Phase 5)'],
        ['5', [[('Himesh Vaskar', True, '17324D', '17'), (' (Sl. No. 35)', False, None, '17')]], 'Frontend / UI Lead: React & Vite responsive dashboard, sample catalog, product search, save/unsave session state, product detail preview (Phase 6)'],
    ]
    populate_table_rows(tbl20, tbl20_data, bold_first_col=True)
    
    # Table 25: 1. Project Summary
    tbl25 = body[25]
    summary_text = (
        "DropOrCop is a machine-learning web application that uses historical sneaker transaction data to estimate "
        "a sneaker's resale price and determine its potential profit or loss against retail cost. Using historical secondary "
        "market transaction records from StockX (covering Nike x Off-White and Adidas Yeezy releases), the pipeline cleans "
        "price string formatting, calculates the elapsed release duration (days_since_release), and encodes core sneaker "
        "attributes (brand, shoe_size, retail_price). A single, robust RandomForestRegressor ensemble is trained to predict "
        "the estimated resale price. From this prediction, estimated net profit or loss is calculated as (Estimated Resale Price - Retail Price). "
        "The trained model is serialized into models/best_model.joblib for zero-latency inference via a lightweight FastAPI backend "
        "(developed by Sinthoiba Kangjam) exposing RESTful /predict, /brands, and /health endpoints. "
        "A responsive React and Vite frontend (developed by Himesh Vaskar) provides a modern dark-mode user interface, sample sneaker "
        "catalog, real-time product search by brand/model/colourway, browser-session save/unsave interactions, and detail previews. "
        "Sample catalog figures are transparently labeled as illustrative during early prototype demonstration. "
        "Advanced comparative modeling (e.g., Gradient Boosting) and extensive hyperparameter grid searching are retained as optional enhancements."
    )
    update_callout_box(tbl25, "1. Project Summary (Data & ML Pipeline Perspective)", [summary_text])
    
    # Table 29: 2. Background and Problem Statement
    tbl29 = body[29]
    bg_text = (
        "Limited-edition sneakers frequently trade on secondary marketplaces at prices significantly higher or lower than "
        "their original retail prices. Buyers and casual collectors often struggle to gauge whether an upcoming drop will appreciate "
        "or depreciate, risking financial loss when paying retail for drops that drop below retail price. DropOrCop addresses this "
        "problem by training a regression model on historical secondary market transactions to estimate future resale values and "
        "provide an immediate, data-backed profit or loss forecast prior to purchase."
    )
    update_callout_box(tbl29, "2. Background and Problem Statement", [bg_text])
    
    # Section 3: Overall Aim (P32)
    p32 = body[32]
    for child in list(p32):
        p32.remove(child)
    pPr32 = ET.SubElement(p32, f'{{{W_NS}}}pPr')
    ET.SubElement(pPr32, f'{{{W_NS}}}spacing', {f'{{{W_NS}}}before': '60', f'{{{W_NS}}}after': '120'})
    
    r_aim_lbl = ET.SubElement(p32, f'{{{W_NS}}}r')
    rPr_lbl = ET.SubElement(r_aim_lbl, f'{{{W_NS}}}rPr')
    ET.SubElement(rPr_lbl, f'{{{W_NS}}}b')
    ET.SubElement(rPr_lbl, f'{{{W_NS}}}color', {f'{{{W_NS}}}val': '17324D'})
    ET.SubElement(rPr_lbl, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': '18'})
    t_lbl = ET.SubElement(r_aim_lbl, f'{{{W_NS}}}t')
    t_lbl.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t_lbl.text = 'Overall Aim: '
    
    r_aim_val = ET.SubElement(p32, f'{{{W_NS}}}r')
    rPr_val = ET.SubElement(r_aim_val, f'{{{W_NS}}}rPr')
    ET.SubElement(rPr_val, f'{{{W_NS}}}i')
    ET.SubElement(rPr_val, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': '18'})
    t_val = ET.SubElement(r_aim_val, f'{{{W_NS}}}t')
    t_val.text = '"The aim of DropOrCop is to make a simple website that uses past sneaker sales to estimate a sneaker’s resale price and possible profit or loss."'

    # Table 33: Objectives
    tbl33 = body[33]
    tbl33_data = [
        ['O1', [
            [('Data Ingestion & Cleaning (Phase 1): ', True, '17324D', '17'),
             ('Ingest historical StockX records, scrub currency characters ($, commas), cast prices to numeric, compute days_since_release, and remove invalid entries.', False, None, '17')],
            [('Measurable Success Indicator: ', True, '17324D', '17'),
             ('Clean dataset saved to data/processed/clean_stockx.csv with 0 string artifacts and verified numerical price columns.', False, None, '17')]
        ]],
        ['O2', [
            [('Feature Preprocessing & Single Model Training (Phases 2 & 3): ', True, '17324D', '17'),
             ('Prepare features (brand, retail_price, shoe_size, days_since_release) and train a single RandomForestRegressor predicting resale price.', False, None, '17')],
            [('Measurable Success Indicator: ', True, '17324D', '17'),
             ('Model successfully trains in < 2 minutes with cross-validated R² > 0.70 and exported inference artifact models/best_model.joblib.', False, None, '17')]
        ]],
        ['O3', [
            [('Export & Evaluation Handoff (Phase 4): ', True, '17324D', '17'),
             ('Export serialized model pipeline and a test set sample check table for downstream API integration and evaluation.', False, None, '17')],
            [('Measurable Success Indicator: ', True, '17324D', '17'),
             ('models/best_model.joblib loads and predicts in < 50 ms; data/processed/test_predictions.csv generated with true vs. predicted prices.', False, None, '17')]
        ]],
        ['O4', [
            [('Backend API Microservice (Phase 5 | Sinthoiba Kangjam): ', True, '17324D', '17'),
             ('Deploy high-throughput FastAPI service in api/main.py with /predict, /health, /brands endpoints, CORS middleware, and Pydantic validation.', False, None, '17')],
            [('Measurable Success Indicator: ', True, '17324D', '17'),
             ('API responds in < 50 ms with validated JSON containing estimated resale price and COP/DROP verdict calculation; Swagger /docs live.', False, None, '17')]
        ]],
        ['O5', [
            [('Frontend User Interface (Phase 6 | Himesh Vaskar): ', True, '17324D', '17'),
             ('Develop responsive React and Vite web client featuring dark-mode dashboard, sample sneaker catalog, real-time search, save/unsave state, and detail preview.', False, None, '17')],
            [('Measurable Success Indicator: ', True, '17324D', '17'),
             ('UI renders seamlessly across desktop and mobile screens, executes client-side search across brand/model/colourway, and labels sample figures as illustrative.', False, None, '17')]
        ]],
    ]
    populate_table_rows(tbl33, tbl33_data, bold_first_col=True)
    
    # Table 36: Included in scope
    tbl36 = body[36]
    tbl36_data = [
        [[
            [('1. Data Cleaning (src/data_prep.py | Harsh Kumar): ', True, '17324D', '17'),
             ('Parsing StockX 2019 dataset (data/raw/), stripping currency formatting ($ and commas), casting to float64, calculating elapsed time days_since_release = (Order Date - Release Date), and filtering non-physical records (Sale Price <= 0, days_since_release >= 0).', False, None, '17')]
        ]],
        [[
            [('2. Feature Preprocessing & Baseline Pipeline (src/train.py | Harsh Kumar): ', True, '17324D', '17'),
             ('Handling categorical features (brand) using standard scikit-learn OneHotEncoder; scaling continuous inputs (retail_price, days_since_release, shoe_size) using StandardScaler.', False, None, '17')]
        ]],
        [[
            [('3. Single Model Training & Architecture (src/train.py | Harsh Kumar): ', True, '17324D', '17'),
             ('Training a single, robust baseline Random Forest Regressor (RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)) predicting resale price directly without complex target transformations.', False, None, '17')]
        ]],
        [[
            [('4. Model Serialization & Downstream Handoff (Harsh Kumar): ', True, '17324D', '17'),
             ('Serializing the trained pipeline to models/best_model.joblib (< 50 ms latency); exporting 18,871 holdout test predictions to data/processed/test_predictions.csv for downstream evaluation.', False, None, '17')]
        ]],
        [[
            [('5. Model Evaluation & Verification (Phase 4 | Anamika Ghosh): ', True, '17324D', '17'),
             ('Benchmarking test predictions on unseen holdout data via MAPE, MAE, and R²; generating residual diagnostic distributions.', False, None, '17')]
        ]],
        [[
            [('6. Backend REST API Service (Phase 5 | Sinthoiba Kangjam): ', True, '17324D', '17'),
             ('High-performance FastAPI service (api/main.py) exposing /predict (POST), /brands (GET), and /health (GET) endpoints with strict Pydantic schema validation, CORS headers, and automatic OpenAPI /docs.', False, None, '17')]
        ]],
        [[
            [('7. Modern Responsive UI (Phase 6 | Himesh Vaskar): ', True, '17324D', '17'),
             ('React and Vite frontend application (src/App.jsx, src/components, src/styles/global.css) with responsive dashboard, sample sneaker catalog, search by brand/model/colourway, browser-session save/unsave state, product detail preview, and Lucide React icons.', False, None, '17')]
        ]],
        [[
            [('8. Sample Catalog Data & Illustrative Labeling (Phase 6 | Himesh Vaskar): ', True, '17324D', '17'),
             ('Catalog display initialized with four sample product records featuring illustrative retail/resale prices and market changes; clearly labeled as illustrative prototypes without claiming live connected predictions.', False, None, '17')]
        ]],
        [[
            [('9. Optional Enhancements (Non-Core / Time-Permitting): ', True, '17324D', '17'),
             ('Benchmarking against GradientBoostingRegressor (src/model_comparison.py), hyperparameter grid search (GridSearchCV), and granular silhouette target encoding.', False, None, '17')]
        ]],
    ]
    populate_table_rows(tbl36, tbl36_data, bold_first_col=False)
    
    # Paragraph 38: Assumptions, constraints, dependencies
    p38 = body[38]
    for child in list(p38):
        p38.remove(child)
    pPr38 = ET.SubElement(p38, f'{{{W_NS}}}pPr')
    ET.SubElement(pPr38, f'{{{W_NS}}}spacing', {f'{{{W_NS}}}before': '60', f'{{{W_NS}}}after': '100'})
    
    r38_lbl = ET.SubElement(p38, f'{{{W_NS}}}r')
    rPr38_lbl = ET.SubElement(r38_lbl, f'{{{W_NS}}}rPr')
    ET.SubElement(rPr38_lbl, f'{{{W_NS}}}b')
    ET.SubElement(rPr38_lbl, f'{{{W_NS}}}color', {f'{{{W_NS}}}val': '17324D'})
    ET.SubElement(rPr38_lbl, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': '17'})
    t38_lbl = ET.SubElement(r38_lbl, f'{{{W_NS}}}t')
    t38_lbl.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t38_lbl.text = 'Assumptions, Constraints & Dependencies: '
    
    r38_val = ET.SubElement(p38, f'{{{W_NS}}}r')
    rPr38_val = ET.SubElement(r38_val, f'{{{W_NS}}}rPr')
    ET.SubElement(rPr38_val, f'{{{W_NS}}}sz', {f'{{{W_NS}}}val': '17'})
    t38_val = ET.SubElement(r38_val, f'{{{W_NS}}}t')
    t38_val.text = (
        '1) Dataset: Pre-collected Kaggle StockX 2019 dataset (no live scraping required). '
        '2) Timeframe: 3-day development window (16–18 Nov 2026); requirements prioritized to ensure working demonstration. '
        '3) Hardware & Serving: Fully self-contained local execution (Localhost FastAPI :8000 + Vite :5173) with zero paid external cloud dependencies or API keys required. '
        '4) Libraries: Python 3.10+, pandas, numpy, scikit-learn, joblib, fastapi, uvicorn; Node.js, React, Vite, Lucide React. '
        '5) Frontend Data Status: Frontend uses 4 sample sneaker records with illustrative prices; live model inference is served independently via FastAPI /predict endpoint.'
    )
    
    # Table 43: 5.1 Functional requirements
    tbl43 = body[43]
    tbl43_data = [
        ['FR-01', 'The data ingestion script shall clean raw StockX transaction data into valid numerical types and compute days_since_release.', 'Must', 'Running python src/data_prep.py produces clean_stockx.csv with zero nulls and correct data types.'],
        ['FR-02', 'The system shall train a single RandomForestRegressor pipeline predicting sneaker resale price directly.', 'Must', 'python src/train.py trains the pipeline and logs train/test evaluation metrics without errors.'],
        ['FR-03', 'The system shall export the trained pipeline as a self-contained joblib file.', 'Must', 'models/best_model.joblib exists on disk; loading the file and passing a test dictionary returns an estimated resale price within 50 ms.'],
        ['FR-04', 'The system shall generate a sample verification dataset with actual vs. predicted values.', 'Must', 'data/processed/test_predictions.csv contains columns [actual_resale_price, predicted_resale_price, retail_price, profit_or_loss].'],
        ['FR-05', 'The backend API shall expose REST endpoints (/predict, /brands, /health) with strict Pydantic validation schemas and CORS.', 'Must', 'FastAPI service loads best_model.joblib, returns predicted resale price and verdict in < 50 ms, and passes automated health check.'],
        ['FR-06', 'The frontend shall display sneaker products in a responsive catalog with sample product records.', 'Must', 'React and Vite client renders sneaker cards displaying name, brand, retail/resale figures, and status badges in a grid.'],
        ['FR-07', 'The frontend shall enable searching and filtering products by brand, model, or colourway.', 'Must', 'Typing into search input immediately filters the displayed product catalog without page reload.'],
        ['FR-08', 'The frontend shall allow users to save and unsave products during the browser session.', 'Should', 'Clicking the bookmark/save icon toggles the saved state and updates the active session counter.'],
        ['FR-09', 'The frontend shall open a product detail preview modal with item specifications and illustrative metrics.', 'Must', 'Clicking a product opens a preview modal with granular details, clearly labeled as illustrative prototype data.'],
        ['FR-10', 'The frontend shall provide fully responsive layouts for mobile, tablet, and desktop screens.', 'Must', 'CSS flexbox/grid layout adapts cleanly to screen widths from 375px to 1920px without horizontal scroll breaking.'],
        ['FR-11', 'The evaluation module shall benchmark predictions and calculate MAPE, MAE, and R² scores on unseen test data.', 'Should', 'Evaluation script executes on test_predictions.csv and reports validation error metrics.'],
        ['FR-12', '(Optional Enhancement) The system may compare the primary model against GradientBoostingRegressor.', 'Could', 'Optional script src/model_comparison.py outputs comparative MAPE/MAE scores.'],
    ]
    populate_table_rows(tbl43, tbl43_data, bold_first_col=True)
    
    # Table 46: 5.2 Non-functional requirements
    tbl46 = body[46]
    tbl46_data = [
        ['Usability', 'Clean and consistent user flow; readable labels, high-contrast typography, intuitive search, Lucide React icons, and illustrative disclaimer notices.'],
        ['Performance', 'Single-instance ML inference latency < 50 ms (actual: 0.07 ms). FastAPI round-trip response < 100 ms. Vite frontend dev server starts in < 500 ms with sub-second HMR.'],
        ['Reliability', 'Frontend and backend handle missing fields, invalid types, out-of-range dates, and API network disconnects gracefully with descriptive fallback banners, avoiding crashes.'],
        ['Security and privacy', 'Fully anonymized public dataset containing zero personal identifiable information (PII). No user logins, passwords, or secrets stored in client-side code.'],
        ['Compatibility', 'Web application fully functional across modern desktop and mobile browsers (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge). Compatible with standard Python 3.10+ and Node.js environments.'],
        ['Maintainability', 'Codebase adopts modular directory structure (src/data_prep.py, src/train.py, api/main.py, src/App.jsx, src/components/, src/styles/global.css), clean component separation, and comprehensive documentation.'],
    ]
    populate_table_rows(tbl46, tbl46_data, bold_first_col=True)
    
    # Table 70: 6. Proposed solution and system design
    tbl70 = body[70]
    diagram_ascii = (
        "[StockX Data] ──> [src/data_prep.py: Cleaning] ──> [Feature Scaling & Encoding]\n"
        "                                                              │\n"
        "                                                              ▼\n"
        "                                              [Single RandomForestRegressor]\n"
        "                                                              │\n"
        "                                                              ▼\n"
        "                                            [Export: models/best_model.joblib]\n"
        "                                                              │\n"
        "                                ┌─────────────────────────────┴─────────────────────────────┐\n"
        "                                ▼                                                           ▼\n"
        "                 [FastAPI: /predict endpoint]                               [Test Sample CSV: test_predictions.csv]\n"
        "                 (Sinthoiba - Phase 5)                                      (Anamika - Phase 4)\n"
        "                                │\n"
        "                                ▼\n"
        "                 [React + Vite Frontend]\n"
        "                 - Sneaker Catalog & Search\n"
        "                 - Session Save/Unsave State\n"
        "                 - Product Detail Preview\n"
        "                 (Himesh - Phase 6)"
    )
    
    arch_items = [
        ('code', diagram_ascii),
        [('1. Offline Data & ML Training Pipeline (Phases 1-3 | Harsh Kumar): ', True, '17324D', '17'),
         ('Ingests raw StockX records, cleans currency string formatting, computes days_since_release, encodes categorical brand features via OneHotEncoder, scales continuous inputs via StandardScaler, trains a robust single RandomForestRegressor, and serializes the winning pipeline to models/best_model.joblib alongside holdout test_predictions.csv.', False, None, '17')],
        [('2. Model Evaluation Layer (Phase 4 | Anamika Ghosh): ', True, '17324D', '17'),
         ('Loads test_predictions.csv, computes cross-validated evaluation metrics (MAPE, MAE, RMSE, R²), and inspects sample verification checks to validate model generalization.', False, None, '17')],
        [('3. Backend Microservice Layer (Phase 5 | Sinthoiba Kangjam): ', True, '17324D', '17'),
         ('Lightweight FastAPI service in api/main.py exposing /predict, /brands, and /health endpoints. Features CORS middleware for frontend integration, automatic Pydantic request/response validation schemas (PredictRequest, PredictResponse), joblib model loading, sub-50ms inference, and automated OpenAPI documentation at /docs.', False, None, '17')],
        [('4. Frontend UI Layer (Phase 6 | Himesh Vaskar): ', True, '17324D', '17'),
         ('Modern, responsive dashboard built with React and Vite (src/App.jsx, src/components, src/styles/global.css) utilizing Lucide React icons. Features include a sneaker catalog displaying product cards, real-time search across brand/model/colourway, browser-session save/unsave interaction state, and a product detail preview modal. Note: The frontend currently operates on four sample product records with illustrative prices and market metrics, transparently labeled as illustrative during early prototype stages.', False, None, '17')],
    ]
    update_callout_box(tbl70, "6. Proposed Solution and System Design", arch_items)
    
    # Table 73: 6.1 Modules and responsibilities
    tbl73 = body[73]
    tbl73_data = [
        ['Data Ingestion & Cleaning (Phase 1)', 'Ingest StockX dataset, clean currency strings, compute days_since_release, filter invalid prices', 'Harsh Kumar (Sl. No. 31)'],
        ['Feature Preprocessing & Model Training (Phases 2 & 3)', 'Preprocess features (OneHotEncoder for brand, StandardScaler), train single RandomForestRegressor, export best_model.joblib', 'Harsh Kumar (Sl. No. 31)'],
        ['Model Evaluation & Verification (Phase 4)', 'Compute MAPE, MAE, R² scores, perform residual diagnostics on test_predictions.csv', 'Anamika Ghosh (Sl. No. 32)'],
        ['Backend / API Serving (Phase 5)', 'FastAPI REST microservice (api/main.py), routes (/predict, /brands, /health), Pydantic validation schemas, CORS middleware, model serving', 'Sinthoiba Kangjam (Sl. No. 34)'],
        ['Frontend / UI (Phase 6)', 'React and Vite dashboard, responsive layout, sample sneaker catalog, search by brand/model/colourway, browser-session save/unsave, product detail preview (src/App.jsx, src/components, src/styles/global.css)', 'Himesh Vaskar (Sl. No. 35)'],
        ['Testing & Presentation Coordination (Phase 7)', 'End-to-end integration testing, presentation slide deck, viva demonstration', 'All Members (Group G)'],
    ]
    populate_table_rows(tbl73, tbl73_data, bold_first_col=True)
    
    # Table 78: 6.2 Technology stack
    tbl78 = body[78]
    tbl78_data = [
        ['Frontend Framework & UI', 'React, JavaScript, CSS', 'Component-driven UI, responsive state management, clean component modularity across navigation, search, and catalog cards'],
        ['Build & Development Tool', 'Vite', 'Ultra-fast Hot Module Replacement (HMR), instant local server startup, and optimized ES modules build pipeline'],
        ['UI Icons', 'Lucide React', 'Consistent, lightweight, accessible SVG icon set for navigation, bookmarking/saving, and action indicators'],
        ['Backend Framework & Server', 'Python 3.10+, FastAPI, Uvicorn', 'High-throughput asynchronous REST API framework with native Pydantic schema validation, CORS support, and automatic OpenAPI documentation'],
        ['ML & Data Processing', 'scikit-learn, pandas, NumPy', 'Vectorized tabular operations over 94,000 rows; robust tree-based RandomForestRegressor ensemble'],
        ['Model Serialization', 'joblib', 'Industry standard for serializing scikit-learn tree ensembles, allowing zero-overhead loading and sub-millisecond inference in FastAPI'],
        ['Development & Version Control', 'Visual Studio Code, Git, GitHub', 'Standardized cross-team development environment with branch-based version control and issue tracking'],
        ['Hosting & Serving (Local Setup)', 'Localhost ASGI (:8000) & Vite (:5173)', 'High reliability, zero external hosting latency, and 100% reproducible execution during academic demonstration'],
    ]
    populate_table_rows(tbl78, tbl78_data, bold_first_col=True)
    
    # Table 84: 7. Dataset, inputs and data management
    tbl84 = body[84]
    tbl84_data = [
        ['Dataset / source name', 'StockX Sneaker Data Contest Dataset (2019)'],
        ['Source URL / provider', 'https://www.kaggle.com/datasets/hudsonstuck/stockx-data-contest (Hosted publicly on Kaggle, originally released by StockX LLC)'],
        ['Access date and licence / usage terms', 'Access Date: 15 November 2026. Licence: Publicly accessible dataset on Kaggle released for educational, data contest, and academic research purposes. Intended strictly for student project demonstration.'],
        ['Privacy / safety measures', 'Fully anonymized historical secondary sales transactions across 99,956 sales. Contains no personally identifiable information (PII), customer names, payment details, or street addresses. Geographic data is restricted to US State level.'],
    ]
    populate_table_rows(tbl84, tbl84_data, bold_first_col=True)
    
    # Table 90: 8. Applied ML / algorithmic approach
    tbl90 = body[90]
    tbl90_data = [
        ['Problem type', 'Tabular regression predicting a single continuous target: Resale Price (P_resale). Target consistency: The model strictly predicts estimated Resale Price (P_resale); estimated net profit/loss is calculated downstream as (P_resale - P_retail).'],
        ['Preprocessing', '1. Currency string cleansing ($ and commas removed, cast to float64). 2. Temporal feature generation: days_since_release = (Order Date - Release Date). 3. Removal of invalid records (where Sale Price <= 0 or negative release days).'],
        ['Feature engineering', 'Categorical encoding for brand (One-Hot Encoding); standard scaling for continuous features (retail_price, shoe_size, days_since_release) assembled into an encapsulated scikit-learn pipeline.'],
        ['Baseline', '1. Naive baseline: P_resale = P_retail (assuming zero resale profit). 2. DummyRegressor predicting median historical resale price grouped by brand.'],
        ['Candidate model(s) / algorithm(s)', 'Primary Champion: Random Forest Regressor (RandomForestRegressor): A robust ensemble of 100 decision trees that handles non-linear relationships, resists overfitting, requires minimal parameter tuning, and trains in < 2 minutes (actual: 0.96s). (Optional enhancement: GradientBoostingRegressor benchmark).'],
        ['Training / validation plan', '80/20 train/test split with deterministic random seed (random_state=42). 5-fold cross-validation. Preprocessing fitted strictly on training split to eliminate data leakage.'],
        ['Evaluation metrics', 'Primary: Mean Absolute Percentage Error (MAPE) and R² Score. Secondary: Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) in USD ($).'],
        ['Model serving / integration', 'Winning pipeline serialized to models/best_model.joblib. Served via FastAPI /predict endpoint returning predictions in < 50 ms (actual: 0.07 ms). Note on Frontend: The React client currently uses four sample catalog records with illustrative metrics to validate UI/UX search and save interactions prior to live pipeline hookup.'],
        ['Limitations / responsible use', 'The estimate is based on historical StockX data from 2017–2019. It may not match today’s prices and is for a student project demonstration, not financial advice or a buy/sell recommendation.'],
    ]
    populate_table_rows(tbl90, tbl90_data, bold_first_col=True)
    
    # Table 99: 9. Team confirmation
    tbl99 = body[99]
    tbl99_data = [
        ['Harsh Kumar (Sl. No. 31)', '[Harsh Kumar]', '16-11-2026'],
        ['Anamika Ghosh (Sl. No. 32)', '[Anamika Ghosh]', '16-11-2026'],
        ['Sinthoiba Kangjam (Sl. No. 34)', '[Sinthoiba Kangjam]', '16-11-2026'],
        ['Himesh Vaskar (Sl. No. 35)', '[Himesh Vaskar]', '16-11-2026'],
        ['Group G Coordination', '[Team G Confirmation]', '16-11-2026'],
    ]
    populate_table_rows(tbl99, tbl99_data, bold_first_col=True)
    
    # Serialize back to XML
    xml_content = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    all_files['word/document.xml'] = xml_content
    
    for out_path in [output_root, output_docs, output_updated]:
        os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else '.', exist_ok=True)
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
            for fname, fcontent in all_files.items():
                z_out.writestr(fname, fcontent)
        print(f'Successfully generated: {out_path} ({os.path.getsize(out_path)} bytes)')

if __name__ == '__main__':
    build_docx()
