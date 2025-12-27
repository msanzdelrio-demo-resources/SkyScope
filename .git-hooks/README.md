# Git Hooks for SkyScope

This directory contains Git hooks to enhance security and code quality.

## Available Hooks

### pre-commit
Prevents committing sensitive information such as:
- Hardcoded API keys
- Secret keys and passwords
- `.env` files
- API keys in frontend code (JavaScript/HTML)

## Installation

### Automatic Installation (Recommended)

Run this command from the project root:

```bash
# For Unix/Linux/macOS
./scripts/install-hooks.sh

# Or manually
cp .git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Manual Installation

1. Copy the hook to your `.git/hooks` directory:
   ```bash
   cp .git-hooks/pre-commit .git/hooks/pre-commit
   ```

2. Make it executable:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

3. Verify installation:
   ```bash
   ls -la .git/hooks/pre-commit
   ```

## Testing the Hook

Try to commit a file with a hardcoded secret:

```bash
# This should be blocked
echo 'API_KEY="abc123secretkey456"' >> test.py
git add test.py
git commit -m "test"
# Should fail with security warning
```

## Bypassing the Hook

**⚠️ WARNING:** Only bypass if you're absolutely sure there are no secrets:

```bash
git commit --no-verify
```

## Hook Behavior

### What it Checks

1. **Hardcoded Secrets in Any File:**
   - API keys (OPENWEATHER_APPID, api_key)
   - Secret keys (SECRET_KEY, secret)
   - Passwords (password, passwd)
   - Tokens

2. **.env File Commits:**
   - Blocks any attempt to commit `.env` file
   - Suggests using `.env.example` instead

3. **Frontend Secret Exposure:**
   - Scans JavaScript and HTML files for API keys
   - Prevents client-side secret exposure

4. **Security TODOs:**
   - Warns about unresolved security-related tasks

### Exit Codes

- `0`: All checks passed, commit allowed
- `1`: Security issue found, commit blocked

## Troubleshooting

### Hook Not Running

Check if the hook is executable:
```bash
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x
```

If not, make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### False Positives

If the hook incorrectly flags something:

1. Review the match to ensure it's not a real secret
2. Consider refactoring the code to use environment variables
3. If it's a test value, use obvious fake data like "test-api-key"
4. As a last resort, bypass with `--no-verify` (document why in commit message)

## Updating Hooks

When hooks are updated in the repository:

```bash
# Re-install the latest version
cp .git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Additional Security

### Recommended Tools

Install these for additional security:

```bash
# Python security scanner
pip install bandit safety

# Pre-commit framework (optional)
pip install pre-commit
pre-commit install
```

### Manual Security Checks

Before major commits:

```bash
# Check for vulnerable dependencies
safety check

# Scan code for security issues
bandit -r app/

# Run comprehensive security check
python security_check.py
```

## Contributing

When adding new hooks:

1. Add the hook to `.git-hooks/`
2. Update this README
3. Test thoroughly
4. Document any dependencies
5. Consider cross-platform compatibility

## Support

For issues with Git hooks:
- Check the [Security Review](../SECURITY_REVIEW.md)
- Review [README Security Section](../README.md#security)
- Open an issue on GitHub
