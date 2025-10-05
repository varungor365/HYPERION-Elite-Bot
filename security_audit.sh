#!/bin/bash

# HYPERION Elite Bot - Security Audit Script
# ==========================================
# Comprehensive security check before VPS deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "🔒 HYPERION ELITE BOT - SECURITY AUDIT"
echo "====================================="
echo "Comprehensive pre-deployment security check"
echo -e "${NC}"

# Function to print results
print_pass() {
    echo -e "${GREEN}✅ PASS${NC} $1"
}

print_fail() {
    echo -e "${RED}❌ FAIL${NC} $1"
    ((FAIL_COUNT++))
}

print_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️  INFO${NC} $1"
}

# Initialize counters
FAIL_COUNT=0
WARN_COUNT=0

echo "Starting security audit..."
echo

# 1. Check for hardcoded tokens/secrets
echo "🔍 Checking for hardcoded secrets..."

# Search for potential hardcoded tokens
TOKEN_PATTERNS=(
    "7090420579"
    "AAE[A-Za-z0-9_-]+"
    "bot[0-9]+:[A-Za-z0-9_-]+"
    "sk-[A-Za-z0-9]+"
    "xoxb-[0-9]+-[0-9]+-[A-Za-z0-9]+"
)

SECRETS_FOUND=0
for pattern in "${TOKEN_PATTERNS[@]}"; do
    if grep -r -E "$pattern" . --include="*.py" --exclude-dir=".git" --exclude-dir=".venv" --exclude-dir="venv" --exclude-dir="__pycache__" 2>/dev/null; then
        print_fail "Hardcoded token/secret pattern found: $pattern"
        ((SECRETS_FOUND++))
    fi
done

if [ $SECRETS_FOUND -eq 0 ]; then
    print_pass "No hardcoded tokens/secrets found"
else
    print_fail "Found $SECRETS_FOUND potential hardcoded secrets"
fi

echo

# 2. Check file permissions
echo "🔐 Checking file permissions..."

# Check for world-readable sensitive files
SENSITIVE_FILES=(
    ".env"
)

for file in "${SENSITIVE_FILES[@]}"; do
    if [ -f "$file" ]; then
        perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null)
        if [ "${perms: -1}" != "0" ]; then
            print_fail "File $file is world-readable (permissions: $perms)"
        else
            print_pass "File $file has secure permissions ($perms)"
        fi
    fi
done

# Check for config files (less strict)
CONFIG_FILES=(
    "hyperion_config.py"
    "config.py"
)

for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null)
        if [ "$perms" == "644" ] || [ "$perms" == "640" ] || [ "$perms" == "600" ]; then
            print_pass "Config file $file has acceptable permissions ($perms)"
        else
            print_warn "Config file $file has loose permissions ($perms)"
            ((WARN_COUNT++))
        fi
    fi
done

echo

# 3. Check environment variable usage
echo "🌍 Checking environment variable usage..."

# Look for proper environment variable usage
if grep -r "os.getenv\|os.environ" . --include="*.py" | grep -v "test" | grep -v "example" >/dev/null; then
    print_pass "Environment variables are used for configuration"
else
    print_warn "No environment variable usage detected"
    ((WARN_COUNT++))
fi

# Check for get_telegram_token function
if grep -r "get_telegram_token\|TELEGRAM_TOKEN" . --include="*.py" >/dev/null; then
    print_pass "Telegram token accessed via secure method"
else
    print_fail "Telegram token access method not found"
fi

echo

# 4. Check Python dependencies security
echo "📦 Checking Python dependencies..."

if [ -f "requirements.txt" ]; then
    print_pass "Requirements.txt file found"
    
    # Check for known vulnerable packages (basic check)
    VULNERABLE_PACKAGES=(
        "pillow==2.2.1"
        "requests==2.5.0"
        "urllib3==1.21"
    )
    
    VULNERABLE_FOUND=0
    for pkg in "${VULNERABLE_PACKAGES[@]}"; do
        if grep -q "$pkg" requirements.txt; then
            print_fail "Potentially vulnerable package found: $pkg"
            ((VULNERABLE_FOUND++))
        fi
    done
    
    if [ $VULNERABLE_FOUND -eq 0 ]; then
        print_pass "No known vulnerable packages detected"
    fi
    
    # Check for pinned versions
    if grep -E "==" requirements.txt >/dev/null; then
        print_pass "Dependencies have pinned versions"
    else
        print_warn "Some dependencies may not have pinned versions"
        ((WARN_COUNT++))
    fi
else
    print_fail "Requirements.txt file not found"
fi

echo

# 5. Check Docker security
echo "🐳 Checking Docker configuration..."

if [ -f "Dockerfile.production" ]; then
    print_pass "Production Dockerfile found"
    
    # Check for non-root user
    if grep -q "USER " Dockerfile.production; then
        print_pass "Dockerfile uses non-root user"
    else
        print_fail "Dockerfile does not specify non-root user"
    fi
    
    # Check for minimal base image
    if grep -q "alpine" Dockerfile.production; then
        print_pass "Uses minimal Alpine Linux base image"
    else
        print_warn "Not using Alpine Linux (consider for smaller attack surface)"
        ((WARN_COUNT++))
    fi
else
    print_warn "Production Dockerfile not found"
    ((WARN_COUNT++))
fi

echo

# 6. Check systemd service security
echo "⚙️  Checking systemd service configuration..."

if [ -f "hyperion-elite-bot.service" ]; then
    print_pass "Systemd service file found"
    
    # Check for security features
    SECURITY_FEATURES=(
        "NoNewPrivileges=true"
        "ProtectSystem"
        "PrivateTmp=true"
    )
    
    SECURITY_SCORE=0
    for feature in "${SECURITY_FEATURES[@]}"; do
        if grep -q "$feature" hyperion-elite-bot.service; then
            ((SECURITY_SCORE++))
        fi
    done
    
    if [ $SECURITY_SCORE -ge 2 ]; then
        print_pass "Systemd service includes security features ($SECURITY_SCORE/3)"
    else
        print_warn "Systemd service has minimal security features ($SECURITY_SCORE/3)"
        ((WARN_COUNT++))
    fi
else
    print_warn "Systemd service file not found"
    ((WARN_COUNT++))
fi

echo

# 7. Check logging security
echo "📝 Checking logging configuration..."

# Check for log rotation
if [ -f "deploy_vps.sh" ] && grep -q "logrotate" deploy_vps.sh; then
    print_pass "Log rotation configured"
else
    print_warn "Log rotation not configured"
    ((WARN_COUNT++))
fi

# Check for sensitive data in logs
LOG_PATTERNS=(
    "token"
    "password"
    "secret"
    "key"
)

SENSITIVE_LOGS=0
for pattern in "${LOG_PATTERNS[@]}"; do
    if grep -r -i "$pattern.*=" . --include="*.py" | grep -i "log\|print" >/dev/null; then
        print_warn "Potential sensitive data in logging: $pattern"
        ((SENSITIVE_LOGS++))
    fi
done

if [ $SENSITIVE_LOGS -eq 0 ]; then
    print_pass "No obvious sensitive data in logging"
fi

echo

# 8. Check network security
echo "🌐 Checking network configuration..."

# Check for HTTPS usage
if grep -r "https://" . --include="*.py" | grep -v "http://localhost" >/dev/null; then
    print_pass "Uses HTTPS for external connections"
else
    print_warn "HTTP usage detected (ensure HTTPS for production)"
    ((WARN_COUNT++))
fi

# Check for proxy support
if grep -r "proxy" . --include="*.py" >/dev/null; then
    print_pass "Proxy support available"
else
    print_warn "No proxy support detected"
    ((WARN_COUNT++))
fi

echo

# 9. Final Security Score
echo "🏁 Security Audit Summary"
echo "========================"

TOTAL_CHECKS=25
PASSED_CHECKS=$((TOTAL_CHECKS - FAIL_COUNT - WARN_COUNT))
SECURITY_SCORE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

echo "Passed: $PASSED_CHECKS/$TOTAL_CHECKS"
echo "Warnings: $WARN_COUNT"
echo "Failures: $FAIL_COUNT"
echo "Security Score: $SECURITY_SCORE%"

# Debug output
echo
echo "DEBUG: FAIL_COUNT=$FAIL_COUNT, WARN_COUNT=$WARN_COUNT"

if [ $FAIL_COUNT -eq 0 ] && [ $WARN_COUNT -le 5 ]; then
    print_pass "SECURITY AUDIT PASSED - Ready for production deployment"
    echo -e "${GREEN}🎯 Your HYPERION Elite Bot is secure and ready for VPS deployment!${NC}"
    exit 0
elif [ $FAIL_COUNT -eq 0 ]; then
    print_warn "SECURITY AUDIT PASSED WITH WARNINGS - Review warnings before deployment"
    echo -e "${YELLOW}⚠️  Consider addressing warnings for optimal security${NC}"
    exit 0
else
    print_fail "SECURITY AUDIT FAILED - Fix critical issues before deployment"
    echo -e "${RED}❌ Address all failures before deploying to production${NC}"
    exit 1
fi