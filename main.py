"""
Main entry point for Autonomous Financial & Business Intelligence Agent.
Run this file to test the agent interactively or execute sample analyses.
"""

import sys
from agent import FinancialIntelligenceAgent

def main():
    print("=" * 65)
    print(" [*] AUTONOMOUS FINANCIAL & BUSINESS INTELLIGENCE AGENT")
    print("=" * 65)
    
    agent = FinancialIntelligenceAgent()
    
    print("\nRunning demonstration query:")
    sample_query = "Give me an executive overview of total revenue, KPIs, and product performance. Export a report."
    
    result = agent.run(sample_query)
    
    print("\n" + "=" * 65)
    print(" AGENT RESPONSE:")
    print("=" * 65)
    print(result)
    print("\n" + "=" * 65)
    print("Analysis complete. Check the 'reports/' folder for the output document.")
    print("=" * 65)

if __name__ == "__main__":
    main()

