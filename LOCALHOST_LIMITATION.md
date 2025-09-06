# 🌐 Exposing localhost for ChatGPT with ngrok

## ⚠️ Important: Localhost Limitation

ChatGPT **cannot access `localhost`** directly because:
- ChatGPT runs on OpenAI's servers, not your local machine
- Web services cannot access private networks for security reasons
- `localhost` is only accessible from your own computer

## 🔧 Solutions for ChatGPT Integration

### Option 1: Azure Deployment (Production - Recommended)
```bash
# Use the provided Azure deployment script
./start_azure.sh

# Then use in ChatGPT:
# https://your-app.azurewebsites.net/fetch?url=TARGET_URL&api_key=YOUR_API_KEY_HERE
```

### Option 2: ngrok Tunnel (Development/Testing)

#### Install ngrok
```bash
# On macOS with Homebrew
brew install ngrok

# On Ubuntu/Debian
sudo snap install ngrok

# Or download from https://ngrok.com/download
```

#### Setup and Use
```bash
# 1. Start your proxy locally
uvicorn main:app --host 127.0.0.1 --port 8003 --reload

# 2. In another terminal, expose it with ngrok
ngrok http 8003

# 3. ngrok will show you a public URL like:
# https://abc123.ngrok.io

# 4. Use this URL in ChatGPT:
# https://abc123.ngrok.io/fetch?url=TARGET_URL&api_key=YOUR_API_KEY_HERE
```

#### Example ChatGPT Prompt with ngrok:
```
Analyze this GitHub repository data:
https://abc123.ngrok.io/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE
```

### Option 3: Cloud VPS (Alternative)
- Deploy on DigitalOcean, Linode, AWS EC2, etc.
- Get a public IP/domain
- Use standard deployment procedures

## 🎯 Recommendation

**For ChatGPT integration, use Azure deployment:**
1. ✅ Professional and stable
2. ✅ HTTPS by default
3. ✅ Built-in security features
4. ✅ Easy scaling
5. ✅ Cost-effective

**ngrok is good for:**
- 🧪 Quick testing
- 🔬 Development
- 🎯 Proof of concept

## 🚀 Quick Test with ngrok

If you want to test immediately:

```bash
# Terminal 1: Start proxy
conda activate proxy
uvicorn main:app --host 127.0.0.1 --port 8003 --reload

# Terminal 2: Expose with ngrok (if installed)
ngrok http 8003

# Use the ngrok URL in ChatGPT instead of localhost
```

## 🔒 Security Notes for ngrok

- ⚠️ Your local service becomes publicly accessible
- ⚠️ Use only for development/testing
- ⚠️ Always keep API_KEY active when using ngrok
- ⚠️ Stop ngrok when not needed

## 📋 Updated README Section

The README should clarify this limitation and provide solutions.
