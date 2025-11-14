# Document Automation System

**Status**: 🚧 In Progress
**Started**: November 14, 2025
**Goal**: Auto-generate PowerPoint decks and Excel workbooks from business intelligence analysis

---

## 🎯 Vision

Transform the Business Intelligence Orchestrator from text-only recommendations to a full document automation system that delivers:
- **PowerPoint presentations** (Executive Summary decks)
- **Excel workbooks** (Analysis workbooks with data, charts, scenarios)
- **Professional deliverables** ready for ValtricAI clients

---

## 🏗️ Architecture Principles

### 1. **Opinionated Templates > Ad-hoc Generation**

**PowerPoint: Executive Summary Deck**
- 10-15 slides
- Sections: Context, Key Findings, Metrics, Risks, Recommendations, Next Steps
- Valtric-branded (title slide, color palette, typography)

**Excel/CSV: Analysis Workbook**
- 2-5 sheets depending on use case
- Tabs: "Executive Summary," "Raw Data," "Calculations," "Charts," "Assumptions"
- All formulas deterministic, no "AI guessed this number"

### 2. **Separation of Concerns**

```
┌─────────────────────────────────────────────────────────────┐
│                    What DeepSeek Handles                    │
├─────────────────────────────────────────────────────────────┤
│ ✓ Slide outline (titles, ordering, section structure)      │
│ ✓ Narrative text (bullets, paragraphs, speaker notes)      │
│ ✓ Explanations ("why this matters")                        │
│ ✓ Recommendations and insights                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                What Code/Templates Handle                   │
├─────────────────────────────────────────────────────────────┤
│ ✓ Layout (slide masters, fonts, colors, branding)          │
│ ✓ All calculations (numpy/pandas)                          │
│ ✓ Chart generation (matplotlib)                            │
│ ✓ Data injection (from canonical JSON)                     │
│ ✓ Formulas (Excel deterministic calculations)              │
│ ✓ File rendering (PowerPoint/Excel generation)             │
└─────────────────────────────────────────────────────────────┘
```

**Rule:** DeepSeek never makes up numbers. Code owns all data.

### 3. **Explicit Triggers, Not Automatic Spam**

❌ **NOT this:** Every query creates files (chaos)

✅ **This:**
- **Explicit user commands:**
  ```
  "Summarize this into a client deck"
  "Generate the workbook for this analysis"
  ```

- **Workflow milestones:**
  ```
  After "Ops Audit" workflow → System offers: "Generate report + deck?"
  ```

Keeps files meaningful, avoids clutter.

---

## 🔄 Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     DOCUMENT GENERATION PIPELINE                 │
└──────────────────────────────────────────────────────────────────┘

1. Intent / Request
   ├─ User: "Create a PowerPoint on this pricing experiment"
   └─ Or: Workflow reaches "ready for deliverables" state

2. Planner Agent (DeepSeek)
   ├─ Reads internal JSON of the analysis
   ├─ Designs slide outline:
   │  └─ Section titles, slide count, narrative arc
   └─ Designs workbook structure:
      └─ Which sheets, which tables, which scenario breakdowns

3. Content Agent (DeepSeek)
   ├─ Fills in text for each section:
   │  └─ Slide summaries, bullets, short explanations
   └─ Executive summary for first slide and first sheet

4. Renderer (Your Code)
   ├─ Templating engine that:
   │  ├─ Maps outline + text → PowerPoint template
   │  ├─ Maps structured data → Excel/CSV
   │  └─ Generates charts (Matplotlib) and injects into slides
   └─ Saves files or returns download links

5. Post-checks (Validation)
   ├─ All numbers in text have corresponding JSON entries
   ├─ No "TBD" or placeholder text remains
   └─ File size, sheet count, slide count within expected bounds
```

---

## 📊 Canonical JSON Schema

### Agent Output Format

All agents must output structured JSON (not just text):

```json
{
  "query": "What are my SaaS unit economics?",
  "agent": "financial",
  "timestamp": "2025-11-14T21:30:00Z",

  "findings": {
    "executive_summary": "Your unit economics are healthy with a 3:1 LTV:CAC ratio...",

    "metrics": {
      "CAC": {
        "value": 5000,
        "unit": "USD",
        "confidence": "high",
        "source": "calculation"
      },
      "LTV": {
        "value": 15000,
        "unit": "USD",
        "confidence": "high",
        "source": "calculation"
      },
      "payback_months": {
        "value": 12,
        "unit": "months",
        "confidence": "medium",
        "source": "industry_benchmark"
      },
      "churn_rate": {
        "value": 5,
        "unit": "percent",
        "confidence": "medium",
        "source": "assumption"
      }
    },

    "data_tables": [
      {
        "name": "monthly_cohorts",
        "description": "Monthly cohort retention analysis",
        "columns": ["month", "customers", "revenue", "churn"],
        "rows": [
          [1, 100, 10000, 5],
          [2, 95, 9500, 4],
          [3, 91, 9100, 3]
        ]
      }
    ],

    "chart_specs": [
      {
        "type": "bar",
        "title": "CAC vs LTV Comparison",
        "x_label": "Metric",
        "y_label": "Value (USD)",
        "x_data": ["CAC", "LTV"],
        "y_data": [5000, 15000],
        "colors": ["#E74C3C", "#2ECC71"]
      },
      {
        "type": "line",
        "title": "Monthly Recurring Revenue Projection",
        "x_label": "Month",
        "y_label": "MRR (USD)",
        "x_data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "y_data": [10000, 9500, 9100, 9200, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000]
      }
    ],

    "narrative": "Your SaaS unit economics show a healthy 3:1 LTV:CAC ratio, which is above the recommended 3:1 threshold. With a 12-month payback period, you're recovering customer acquisition costs within an acceptable timeframe...",

    "key_findings": [
      "LTV:CAC ratio is 3:1, indicating healthy unit economics",
      "12-month payback period is within industry standards",
      "5% monthly churn rate is slightly high for B2B SaaS",
      "MRR showing steady 5% month-over-month growth"
    ],

    "risks": [
      "Churn rate of 5% could erode LTV over time",
      "CAC trending upward due to increased competition",
      "Assumptions based on limited historical data"
    ],

    "recommendations": [
      {
        "title": "Reduce churn rate to 3%",
        "priority": "high",
        "impact": "Would increase LTV by 40% ($15k → $21k)",
        "action_items": [
          "Implement customer success program",
          "Add quarterly business reviews",
          "Build churn prediction model"
        ]
      },
      {
        "title": "Optimize CAC through content marketing",
        "priority": "medium",
        "impact": "Could reduce CAC by 20% ($5k → $4k)",
        "action_items": [
          "Launch SEO content strategy",
          "Build organic lead funnel",
          "Reduce paid ad dependency"
        ]
      }
    ]
  },

  "research_citations": [
    {
      "title": "SaaS Metrics 2.0",
      "authors": ["David Skok"],
      "year": 2015,
      "url": "https://www.forentrepreneurs.com/saas-metrics-2/",
      "relevance": "Industry benchmarks for LTV:CAC ratio"
    }
  ],

  "metadata": {
    "confidence": "high",
    "model": "DeepSeek-V3.2-Exp (Chat)",
    "tokens_used": 2500,
    "cost_usd": 0.002,
    "processing_time_seconds": 3.5
  }
}
```

---

## 📑 PowerPoint Template Structure

### Slide Outline (10-15 slides)

```
┌─────────────────────────────────────────────────────────────┐
│ Slide 1: Title Slide                                       │
│   - Valtric branding                                        │
│   - Query/topic                                             │
│   - Date, prepared for [Client]                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 2: Executive Summary                                 │
│   - 1-page overview                                         │
│   - 3-5 key takeaways                                       │
│   - High-level recommendation                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 3: Context                                            │
│   - What was asked                                          │
│   - Why it matters                                          │
│   - Scope of analysis                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 4: Key Findings                                       │
│   - 3-5 bullet points                                       │
│   - Data-backed insights                                    │
│   - Visual hierarchy                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slides 5-8: Detailed Analysis                               │
│   - Metrics (with charts)                                   │
│   - Supporting data tables                                  │
│   - Visual storytelling                                     │
│   - Research citations                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 9: Risks & Considerations                             │
│   - Potential downsides                                     │
│   - Assumptions made                                        │
│   - Confidence levels                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 10: Recommendations                                   │
│   - Prioritized action items                                │
│   - Expected impact                                         │
│   - Implementation timeline                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 11: Next Steps                                        │
│   - Immediate actions                                       │
│   - 30/60/90 day roadmap                                    │
│   - Success metrics                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slide 12: Appendix                                          │
│   - Methodology                                             │
│   - Sources and citations                                   │
│   - Additional data                                         │
└─────────────────────────────────────────────────────────────┘
```

### Valtric Branding (Placeholder)

```python
VALTRIC_THEME = {
    "primary_color": "#2C3E50",      # Dark blue-gray
    "secondary_color": "#3498DB",    # Blue
    "accent_color": "#E74C3C",       # Red for highlights
    "success_color": "#2ECC71",      # Green for positive metrics
    "warning_color": "#F39C12",      # Orange for warnings
    "text_color": "#2C3E50",         # Dark text
    "background_color": "#FFFFFF",   # White background

    "title_font": "Montserrat",
    "body_font": "Open Sans",
    "title_size": 32,
    "heading_size": 24,
    "body_size": 14
}
```

---

## 📊 Excel Workbook Structure

### Sheet Layout (2-5 sheets)

```
┌─────────────────────────────────────────────────────────────┐
│ Sheet 1: Executive Summary                                  │
│   - High-level metrics (KPIs)                               │
│   - Dashboard-style layout                                  │
│   - Key findings (text)                                     │
│   - Top recommendations                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Sheet 2: Raw Data                                           │
│   - Agent outputs (structured)                              │
│   - Research papers and citations                           │
│   - Original query and context                              │
│   - Timestamp, model, cost metadata                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Sheet 3: Calculations                                       │
│   - All formulas (deterministic)                            │
│   - Scenario analysis (Base / Upside / Downside)            │
│   - Sensitivity tables                                      │
│   - Derived metrics                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Sheet 4: Charts & Visuals                                   │
│   - Chart data tables                                       │
│   - Embedded charts (from matplotlib)                       │
│   - Visual summaries                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Sheet 5: Assumptions & Sources                              │
│   - All assumptions documented                              │
│   - Confidence levels                                       │
│   - Research citations (APA format)                         │
│   - Model limitations                                       │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles for Excel

1. **No AI-generated numbers in formulas**
   - All calculations must be deterministic
   - Formulas reference cells, not hardcoded values
   - Clear audit trail

2. **Scenarios always explicit**
   - Base case (most likely)
   - Upside case (optimistic)
   - Downside case (conservative)

3. **Color coding**
   - Green: Positive metrics, above target
   - Red: Negative metrics, below target
   - Yellow: Warning, needs attention
   - Gray: Assumptions, external data

---

## 🛠️ Technology Stack

### Libraries

```python
# Document generation
python-pptx          # PowerPoint generation
openpyxl             # Excel generation
reportlab            # PDF generation (future)

# Data & visualization
numpy                # Calculations
pandas               # Data manipulation
matplotlib           # Chart generation
seaborn              # Statistical visualizations (future)

# Utilities
jsonschema           # JSON validation
pydantic             # Data validation
Pillow               # Image processing
```

---

## 📋 Implementation Plan

### ✅ Phase 1: Foundation (2-3 hours)

**Goal:** Establish canonical JSON schema and structured outputs

**Tasks:**
- [ ] Create `src/schemas/agent_output.py` (Pydantic schema)
- [ ] Create `src/schemas/validators.py` (JSON validation)
- [ ] Update Financial Agent to output structured JSON
- [ ] Test and validate JSON output
- [ ] Document schema with examples

**Deliverables:**
- Pydantic models for agent outputs
- JSON schema validation
- Example outputs from Financial Agent

---

### ⏳ Phase 2: PowerPoint Generation (4-5 hours)

**Goal:** Generate branded PowerPoint decks from agent JSON

**Tasks:**
- [ ] Create Valtric PowerPoint template
- [ ] Build `src/generators/powerpoint_generator.py`
- [ ] Create Planner agent (DeepSeek designs slide outline)
- [ ] Create Writer agent (DeepSeek fills in text)
- [ ] Build Renderer (JSON → PowerPoint)
- [ ] Add chart injection from matplotlib
- [ ] Test with sample Financial Agent output

**Deliverables:**
- Working PowerPoint generator
- Sample deck from real analysis
- Template file for customization

---

### ⏳ Phase 3: Excel Generation (3-4 hours)

**Goal:** Generate Analysis Workbooks from agent JSON

**Tasks:**
- [ ] Create Excel template structure
- [ ] Build `src/generators/excel_generator.py`
- [ ] Create data mappers (JSON → Excel sheets)
- [ ] Add deterministic formula generation
- [ ] Add chart embedding (matplotlib → Excel)
- [ ] Add scenario analysis (Base/Upside/Downside)
- [ ] Test with sample Financial Agent output

**Deliverables:**
- Working Excel generator
- Sample workbook from real analysis
- Template file for customization

---

### ⏳ Phase 4: Integration (2-3 hours)

**Goal:** Integrate into main orchestrator and API

**Tasks:**
- [ ] Add `/query/{id}/generate-deck` endpoint
- [ ] Add `/query/{id}/generate-workbook` endpoint
- [ ] Add file storage (local or S3)
- [ ] Add download link generation
- [ ] Add post-validation checks
- [ ] Update CLI to support document generation
- [ ] Test end-to-end workflow

**Deliverables:**
- API endpoints working
- CLI commands working
- Full integration test

---

### ⏳ Phase 5: Polish & Production (2-3 hours)

**Goal:** Production-ready document automation

**Tasks:**
- [ ] Add error handling and retry logic
- [ ] Add progress indicators
- [ ] Add document caching (reuse generated docs)
- [ ] Add customization options (branding, templates)
- [ ] Add monitoring and logging
- [ ] Create user documentation
- [ ] Performance testing

**Deliverables:**
- Production-ready system
- User guide
- Performance benchmarks

---

## 🚀 Usage Examples

### API Usage

```bash
# Generate PowerPoint deck
curl -X POST http://localhost:8000/query/123/generate-deck \
  -H "Content-Type: application/json" \
  -d '{"template": "executive_summary", "branding": "valtric"}'

# Response:
{
  "status": "success",
  "file_path": "/outputs/query_123_deck.pptx",
  "download_url": "http://localhost:8000/downloads/abc123",
  "slides": 12,
  "size_mb": 2.3,
  "generated_at": "2025-11-14T21:45:00Z"
}

# Generate Excel workbook
curl -X POST http://localhost:8000/query/123/generate-workbook

# Response:
{
  "status": "success",
  "file_path": "/outputs/query_123_workbook.xlsx",
  "download_url": "http://localhost:8000/downloads/def456",
  "sheets": 5,
  "size_mb": 1.8,
  "generated_at": "2025-11-14T21:46:00Z"
}
```

### CLI Usage

```bash
# Interactive mode
python cli.py

> "What are my SaaS unit economics?"
[Analysis runs...]

> "Generate deck"
✓ PowerPoint deck created: outputs/saas_unit_economics_deck.pptx

> "Generate workbook"
✓ Excel workbook created: outputs/saas_unit_economics_workbook.xlsx

# Command mode
python cli.py --query "SaaS unit economics" --generate-deck --generate-workbook
```

### Python SDK Usage

```python
from src.langgraph_orchestrator import LangGraphOrchestrator
from src.generators.powerpoint_generator import PowerPointGenerator
from src.generators.excel_generator import ExcelGenerator

# Run analysis
orchestrator = LangGraphOrchestrator()
result = orchestrator.orchestrate("What are my SaaS unit economics?")

# Generate PowerPoint
ppt_gen = PowerPointGenerator()
deck_path = ppt_gen.generate(
    agent_output=result,
    template="executive_summary",
    branding="valtric"
)
print(f"Deck created: {deck_path}")

# Generate Excel
excel_gen = ExcelGenerator()
workbook_path = excel_gen.generate(
    agent_output=result,
    include_scenarios=True
)
print(f"Workbook created: {workbook_path}")
```

---

## 🎯 Success Criteria

### Minimum Viable Product (MVP)

- [ ] Financial Agent outputs valid JSON
- [ ] Can generate 12-slide PowerPoint from Financial Agent output
- [ ] Can generate 5-sheet Excel workbook from Financial Agent output
- [ ] Charts render correctly in both formats
- [ ] All numbers in documents match JSON source
- [ ] No placeholder text ("TBD") in outputs
- [ ] Files open correctly in MS Office and Google Workspace

### Production Ready

- [ ] All 4 agents output structured JSON
- [ ] API endpoints respond within 10 seconds
- [ ] Documents cached and reusable
- [ ] Error handling for edge cases
- [ ] User can customize branding
- [ ] Monitoring and logging in place
- [ ] User documentation complete

---

## 📊 Progress Tracking

| Phase | Status | Started | Completed | Notes |
|-------|--------|---------|-----------|-------|
| **Phase 1: Foundation** | ✅ Complete | 2025-11-14 | 2025-11-14 | JSON schema + Financial Agent updated |
| **Phase 2: PowerPoint** | ⏳ Not Started | - | - | - |
| **Phase 3: Excel** | ⏳ Not Started | - | - | - |
| **Phase 4: Integration** | ⏳ Not Started | - | - | - |
| **Phase 5: Polish** | ⏳ Not Started | - | - | - |

---

## 🔍 Open Questions

1. **Branding:** What are the actual Valtric brand colors and fonts?
2. **Storage:** Local filesystem or cloud storage (S3/Azure)?
3. **Authentication:** Should document downloads be authenticated?
4. **Versioning:** Keep history of generated documents?
5. **Customization:** How much template customization should users have?

---

## 📚 Resources

- [python-pptx documentation](https://python-pptx.readthedocs.io/)
- [openpyxl documentation](https://openpyxl.readthedocs.io/)
- [Matplotlib documentation](https://matplotlib.org/stable/contents.html)
- [Pydantic documentation](https://docs.pydantic.dev/)

---

**Last Updated:** November 14, 2025
**Next Review:** After Phase 1 completion
