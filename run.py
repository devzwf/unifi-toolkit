#!/usr/bin/env python3
"""
UI Toolkit - Application Entry Point

This script starts the UI Toolkit web application.
It checks for required environment variables and starts the FastAPI server.
"""
import os
import sys
from pathlib import Path

# Check if .env file exists
env_file = Path(__file__).parent / ".env"
if not env_file.exists():
    print("=" * 70)
    print("ERROR: .env file not found!")
    print("=" * 70)
    print()
    print("Please create a .env file in the project root directory.")
    print("You can copy .env.example as a starting point:")
    print()
    print("  cp .env.example .env")
    print()
    print("Then edit .env and set the required values:")
    print("  - ENCRYPTION_KEY (required)")
    print("  - UniFi controller settings (optional, can configure via web UI)")
    print()
    print("=" * 70)
    sys.exit(1)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(env_file)
except ImportError:
    print("WARNING: python-dotenv not installed, .env file will not be loaded")
    print("Install it with: pip install python-dotenv")

# Check for required environment variables
encryption_key = os.getenv("ENCRYPTION_KEY")
if not encryption_key:
    print("=" * 70)
    print("ERROR: ENCRYPTION_KEY not set in .env file!")
    print("=" * 70)
    print()
    print("The ENCRYPTION_KEY is required to encrypt sensitive data.")
    print("Generate a new key with:")
    print()
    print("  python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")
    print()
    print("Then add it to your .env file:")
    print()
    print("  ENCRYPTION_KEY=your_generated_key_here")
    print()
    print("=" * 70)
    sys.exit(1)

# Start the application
if __name__ == "__main__":
    import uvicorn
    from shared.config import get_settings
    from app import __version__ as app_version
    from tools.wifi_stalker import __version__ as stalker_version
    from tools.threat_watch import __version__ as threat_watch_version
    from tools.network_pulse import __version__ as pulse_version

    settings = get_settings()

    print("=" * 70)
    print("Starting UI Toolkit...")
    print("=" * 70)
    print()
    print(f"Version: {app_version}")
    print(f"Log Level: {settings.log_level}")
    print(f"Database: {settings.database_url}")
    print()

    # Display deployment mode
    deployment_type = settings.deployment_type.upper()
    if deployment_type == "PRODUCTION":
        print(f"Deployment: PRODUCTION (authentication enabled)")
        if settings.domain:
            print(f"Domain: {settings.domain}")
    else:
        print(f"Deployment: LOCAL (authentication disabled)")
    print()

    print("Available tools:")
    print(f"  - Wi-Fi Stalker v{stalker_version}")
    print(f"  - Threat Watch v{threat_watch_version}")
    print(f"  - Network Pulse v{pulse_version}")
    print()

    if deployment_type == "PRODUCTION":
        print("Access via your configured domain with HTTPS")
    else:
        print("Access the dashboard at: http://localhost:8000")
        print("Wi-Fi Stalker at: http://localhost:8000/stalker/")
        print("Threat Watch at: http://localhost:8000/threats/")
        print("Network Pulse at: http://localhost:8000/pulse/")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()

    # Configure logging level
    log_level = settings.log_level.lower()

    # Start uvicorn server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to True for development
        log_level=log_level,
        access_log=True
    )
