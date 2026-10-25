"""
Autonomous Financial & Business Intelligence Agent
Implements autonomous tool selection, execution, and synthesis.
"""

import os
import json
from dotenv import load_dotenv
import tools

load_dotenv()

class FinancialIntelligenceAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                self.client = "gemini"
            except Exception as e:
                print(f"[Warning] Could not initialize Gemini API: {e}. Falling back to Autonomous Heuristic Engine.")
        else:
            print("[Notice] No GEMINI_API_KEY found. Running in Autonomous Heuristic Engine mode.")

    def run(self, user_prompt: str) -> str:
        """
        Executes the Autonomous Agent Loop:
        1. Thought: Analyze intent and plan steps.
        2. Action: Select and invoke appropriate financial tools.
        3. Observation: Process data results.
        4. Synthesis: Produce executive response.
        """
        print(f"\n[Agent] Received User Objective: \"{user_prompt}\"")
        prompt_lower = user_prompt.lower()

        # Step 1: Autonomous Tool Execution
        observations = {}

        # Determine which tools are needed based on objective
        if any(w in prompt_lower for w in ["kpi", "overview", "summary", "total", "performance", "high level"]):
            print("[Agent Action] Calling Tool: calculate_kpis()")
            observations["kpis"] = tools.calculate_kpis()

        if any(w in prompt_lower for w in ["product", "item", "hardware", "software"]):
            print("[Agent Action] Calling Tool: analyze_by_dimension('Product_Name')")
            observations["products"] = tools.analyze_by_dimension("Product_Name")

        if any(w in prompt_lower for w in ["region", "territory", "geography", "north", "south", "east", "west"]):
            print("[Agent Action] Calling Tool: analyze_by_dimension('Region')")
            observations["regions"] = tools.analyze_by_dimension("Region")

        if any(w in prompt_lower for w in ["category"]):
            print("[Agent Action] Calling Tool: analyze_by_dimension('Category')")
            observations["categories"] = tools.analyze_by_dimension("Category")

        # Fallback if no specific tool was triggered
        if not observations:
            print("[Agent Action] Defaulting to full KPI & Product analysis.")
            observations["kpis"] = tools.calculate_kpis()
            observations["products"] = tools.analyze_by_dimension("Product_Name")

        # Step 2: Synthesis
        if self.client == "gemini":
            response = self._synthesize_with_llm(user_prompt, observations)
        else:
            response = self._synthesize_heuristic(user_prompt, observations)

        # Step 3: Check if report export requested
        if any(w in prompt_lower for w in ["report", "export", "save", "document"]):
            save_msg = tools.export_executive_report("Executive_Financial_Report", response)
            print(f"[Agent Action] {save_msg}")

        return response

    def _synthesize_heuristic(self, query: str, observations: dict) -> str:
        """Structured synthesis when running in offline/local autonomous mode."""
        lines = []
        lines.append("## Executive Financial Analysis & Insights")
        lines.append(f"**Target Objective:** {query}\n")

        if "kpis" in observations:
            kpis = observations["kpis"]
            lines.append("### Key Financial Indicators (KPIs)")
            for k, v in kpis.items():
                clean_k = k.replace("_", " ")
                lines.append(f"- **{clean_k}**: {v}")
            lines.append("")

        if "products" in observations:
            lines.append("### Product-Wise Performance Breakdown")
            lines.append(observations["products"])
            lines.append("")

        if "regions" in observations:
            lines.append("### Regional Sales & Profitability")
            lines.append(observations["regions"])
            lines.append("")

        if "categories" in observations:
            lines.append("### Category Breakdown")
            lines.append(observations["categories"])
            lines.append("")

        lines.append("### Strategic Recommendations")
        lines.append("1. **Focus on High-Margin Products**: Emphasize items yielding > 40% margin to maximize net return.")
        lines.append("2. **Address Underperforming Regions**: Rebalance regional sales allocations toward high-growth territories.")
        lines.append("3. **Automate Continuous Auditing**: Implement recurring agentic sweeps to detect cost spikes proactively.")

        return "\n".join(lines)

    def _synthesize_with_llm(self, query: str, observations: dict) -> str:
        """Uses Gemini LLM to synthesize data insights into a business report."""
        prompt = f"""
You are an expert Senior Financial & Data Analytics Agent.
User Objective: {query}

Observed Tool Outputs:
{json.dumps(observations, indent=2)}

Please write a comprehensive, professional executive summary with:
1. Executive Summary
2. Core Findings & Financial Metrics
3. Risk or Opportunity Areas
4. Actionable Next Steps
"""
        response = self.model.generate_content(prompt)
        return response.text
