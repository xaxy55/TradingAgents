# Using TradingAgents with Ollama

This guide explains how to use TradingAgents with Ollama, allowing you to run the trading analysis framework entirely on your local machine with open-source LLMs.

## What is Ollama?

[Ollama](https://ollama.ai) is a tool that allows you to run large language models locally on your computer. This provides several benefits:

- **Privacy**: All LLM processing happens on your machine
- **No API Costs**: Free to use, no per-token charges
- **Offline Capable**: Works without internet (except for market data)
- **Open Source Models**: Full transparency and control

## Installation

### Step 1: Install Ollama

1. Visit [https://ollama.ai](https://ollama.ai)
2. Download and install for your platform (macOS, Linux, or Windows)
3. The Ollama server will start automatically

### Step 2: Pull Required Models

TradingAgents works best with the following models:

```bash
# Recommended for deep thinking (trading decisions, analysis)
ollama pull llama3.1

# Optional: For embedding generation (memory/context)
ollama pull nomic-embed-text

# Alternative models you can try:
ollama pull qwen3       # Good alternative for deep thinking
ollama pull llama3.2    # Lighter weight option for quick thinking
```

### Step 3: Verify Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# You should see a JSON response with your installed models
```

### Step 4: Set Up Environment Variables

You still need Alpha Vantage API for market data:

```bash
export ALPHA_VANTAGE_API_KEY=your_api_key_here
```

Get a free Alpha Vantage API key at: https://www.alphavantage.co/support/#api-key

## Usage

### Using the Example Script

The simplest way to test BTC with Ollama:

```bash
python example_crypto_ollama.py
```

This script will:
- Check if Ollama is running
- Verify required models are available
- Analyze Bitcoin (BTC) using local LLMs
- Display the trading analysis and decision

### Using the Python API

```python
import copy
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure for Ollama
config = copy.deepcopy(DEFAULT_CONFIG)
config["llm_provider"] = "ollama"
config["backend_url"] = "http://localhost:11434/v1"
config["deep_think_llm"] = "llama3.1"
config["quick_think_llm"] = "llama3.1"

# For cryptocurrency analysis
config["crypto_settings"]["default_market"] = "USD"

# Initialize and run
ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("BTC", "2024-05-10")
print(decision)
```

### Using the CLI

```bash
python -m cli.main
```

When prompted:
1. Select **Ollama** as your LLM provider
2. Choose your preferred models (e.g., llama3.1)
3. Enter **BTC** as the ticker symbol
4. Enter the analysis date

## Performance Considerations

### Speed

- **Local LLMs are slower** than cloud APIs (OpenAI, Gemini)
- Analysis may take 10-30 minutes depending on your hardware
- Use shallow research depth (1 debate round) for faster results

### Hardware Requirements

**Recommended:**
- **RAM**: 16GB+ (8GB minimum for llama3.1)
- **CPU**: Modern multi-core processor
- **GPU**: Optional but significantly speeds up inference
- **Storage**: 10GB+ for models

**Model Sizes:**
- llama3.1: ~4.7GB
- qwen3: ~4.5GB
- nomic-embed-text: ~274MB

### Configuration for Faster Local Execution

```python
config = copy.deepcopy(DEFAULT_CONFIG)
config["llm_provider"] = "ollama"
config["backend_url"] = "http://localhost:11434/v1"
config["deep_think_llm"] = "llama3.1"
config["quick_think_llm"] = "llama3.1"

# Use shallow research for faster execution
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1
```

## Supported Cryptocurrencies

All cryptocurrencies supported by TradingAgents work with Ollama:

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- And 30+ other major cryptocurrencies

## Testing

Run the test suite to verify everything is working:

```bash
python test_btc_ollama.py
```

This will test:
- Ollama configuration
- BTC symbol detection
- TradingAgentsGraph initialization with Ollama
- Full BTC analysis (if Ollama is running)

## Troubleshooting

### "Cannot connect to Ollama at http://localhost:11434"

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it (on most systems it starts automatically)
# On macOS/Linux, it may be in your Applications or /usr/local/bin
ollama serve
```

### "Model not found" Error

**Solution:**
```bash
# Pull the model you're trying to use
ollama pull llama3.1

# List available models
ollama list
```

### "Out of memory" Error

**Solutions:**
1. Use a smaller model: `ollama pull llama3.2`
2. Close other applications to free up RAM
3. Reduce research depth in config:
   ```python
   config["max_debate_rounds"] = 1
   config["max_risk_discuss_rounds"] = 1
   ```

### Slow Performance

**Solutions:**
1. Use GPU acceleration if available (Ollama uses GPU automatically)
2. Use smaller/faster models like llama3.2
3. Reduce debate rounds as shown above
4. Ensure no other heavy applications are running

## Comparing LLM Providers

| Provider | Cost | Speed | Privacy | Setup |
|----------|------|-------|---------|-------|
| **Ollama** | Free | Slower | Complete | Moderate |
| **OpenAI** | Pay-per-use | Fast | Cloud | Easy |
| **Google Gemini** | Free tier available | Fast | Cloud | Easy |
| **Anthropic Claude** | Pay-per-use | Fast | Cloud | Easy |

## Advanced Configuration

### Using Different Models for Different Tasks

```python
config["llm_provider"] = "ollama"
config["backend_url"] = "http://localhost:11434/v1"
config["deep_think_llm"] = "llama3.1"    # Larger model for complex decisions
config["quick_think_llm"] = "llama3.2"    # Smaller model for quick tasks
```

### Using Ollama with GPU

Ollama automatically uses GPU if available. To verify:

```bash
# Check Ollama GPU usage (macOS/Linux)
ollama ps

# You should see GPU utilization if supported
```

## More Information

- **Ollama Documentation**: https://github.com/ollama/ollama
- **TradingAgents Crypto Guide**: See [CRYPTOCURRENCY.md](CRYPTOCURRENCY.md)
- **Model Library**: https://ollama.ai/library

## Support

For issues specific to:
- **Ollama**: Visit https://github.com/ollama/ollama/issues
- **TradingAgents**: Open an issue on the TradingAgents GitHub repository

## Summary

✓ **Free to use** - No API costs
✓ **Private** - All processing on your machine  
✓ **Works with BTC** - And all other supported cryptocurrencies
✓ **Easy setup** - Just install Ollama and pull models
✓ **Open source** - Full transparency and control

Get started now:
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.1
export ALPHA_VANTAGE_API_KEY=your_key_here
python example_crypto_ollama.py
```
