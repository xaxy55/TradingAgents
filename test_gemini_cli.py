#!/usr/bin/env python
"""Test script to verify Gemini CLI works with command-line arguments."""

import sys
import subprocess

# Test 1: Check if help works
print("=" * 60)
print("Test 1: Checking CLI help")
print("=" * 60)
result = subprocess.run(
    [sys.executable, "-m", "cli.main", "analyze", "--help"],
    capture_output=True,
    text=True,
    cwd="/workspaces/TradingAgents"
)
print(result.stdout)
if result.returncode == 0:
    print("✓ Help command works!")
else:
    print("✗ Help command failed!")
    print(result.stderr)

# Test 2: Verify default config has Gemini
print("\n" + "=" * 60)
print("Test 2: Checking default config")
print("=" * 60)
from tradingagents.default_config import DEFAULT_CONFIG
print(f"Default LLM Provider: {DEFAULT_CONFIG['llm_provider']}")
print(f"Default Deep Think LLM: {DEFAULT_CONFIG['deep_think_llm']}")
print(f"Default Quick Think LLM: {DEFAULT_CONFIG['quick_think_llm']}")
print(f"Backend URL: {DEFAULT_CONFIG['backend_url']}")

if DEFAULT_CONFIG['llm_provider'] == 'google':
    print("✓ Gemini is set as default!")
else:
    print("✗ Gemini is NOT set as default!")

# Test 3: Check CLI imports properly
print("\n" + "=" * 60)
print("Test 3: Checking CLI imports")
print("=" * 60)
try:
    from cli.main import app
    print("✓ CLI module imports successfully!")
except Exception as e:
    print(f"✗ CLI import failed: {e}")

# Test 4: Check utils have get_backend_url
print("\n" + "=" * 60)
print("Test 4: Checking get_backend_url function")
print("=" * 60)
try:
    from cli.utils import get_backend_url, PROVIDER_URLS
    print(f"Available providers: {list(PROVIDER_URLS.keys())}")
    print(f"Google backend URL: {get_backend_url('google')}")
    print("✓ get_backend_url function works!")
except Exception as e:
    print(f"✗ get_backend_url check failed: {e}")

print("\n" + "=" * 60)
print("All checks completed!")
print("=" * 60)
print("\nYou can now run the CLI with Gemini like this:")
print("python -m cli.main analyze --llm-provider google --ticker AAPL --depth 0")
