# Custom Switchboard (Test Version)

**⚠️ Warning: This is a test version. Do not use in production environments.**

A **customized test version** of Epic Games' Switchboard that addresses key issues and provides enhanced features.

## 🎯 Key Differences (vs. Original Switchboard)

### 1. **Automatic Administrator Privilege Request** ⭐ Core Improvement
- **Issue**: "Failed to obtain/convert traceback!" error during GPU clock control
- **Solution**: Complete resolution through Windows manifest automatic privilege request

### 2. **Enhanced Error Handling** ⭐ Core Improvement
- **Issue**: Untraceable errors in original version
- **Solution**: Specific error information and debugging guides

### 3. **Improved Build Process**
- Executable generation with automatic privilege request

## 🚨 Test Version Notice

### ⚠️ Important Notice
- **Use this version for testing purposes only**
- **Do not use in production environments**
- **Does not replace original Switchboard**
- **Not officially supported by Epic Games**

## 🛠️ Installation and Setup

### Prerequisites
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.11 or higher
- **Unreal Engine**: 5.0 or higher
- **Administrator privileges**: Automatically requested

### Installation
```bash
git clone <repository-url>
cd Switchboard
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Build (with automatic administrator privilege request)
```bash
python -m PyInstaller Switchboard.spec
```

## 🎮 Testing

This is a **test version** of Switchboard with enhanced features. We have conducted comprehensive testing including:

- Administrator privilege auto-request functionality
- GPU clock control improvements
- Enhanced error handling and logging
- Build process optimizations

**Test Video**: [Switchboard Test Demo](https://youtu.be/l__FfgYSjxw?si=PQjXHdZVdkgyggT3)

For testing purposes, you can build the executable using:
```bash
python -m PyInstaller Switchboard.spec
```

The built executable will automatically request administrator privileges when needed.

## 📝 Changelog

### v1.0.0 (Test)
- **Automatic Administrator Privilege Request**: Automatic privilege request through Windows manifest
- **Enhanced Error Handling**: Resolution of "Failed to obtain/convert traceback!" error
- **Improved Build Process**: Executable generation with automatic privilege request
- **Test Environment Setup**: Test configuration and guides

---

**⚠️ Important**: This Custom Switchboard is a **test version**. It does not replace Epic Games' official Switchboard and should not be used in production environments. Use only for testing purposes.

## 🔧 Key Changes 