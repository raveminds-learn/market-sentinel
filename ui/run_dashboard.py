#!/usr/bin/env python3
"""
Quick launcher for the Market Sentinel Dashboard
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit dashboard"""
    try:
        print("🚀 Starting Market Sentinel Dashboard...")
        print("📊 Opening in your default web browser...")

        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dashboard_path = os.path.join(script_dir, 'dashboard.py')

        # Launch Streamlit
        cmd = [sys.executable, '-m', 'streamlit', 'run', dashboard_path]
        subprocess.run(cmd, cwd=os.path.dirname(script_dir))

    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("\n💡 Make sure you have installed all requirements:")
        print("   pip install streamlit plotly matplotlib sentence-transformers lancedb pandas duckdb")

if __name__ == "__main__":
    main()