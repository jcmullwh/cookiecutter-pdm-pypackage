{% if cookiecutter.brave_browser_support == "Y" -%}
"""Brave browser integration utilities."""

from typing import Optional
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import requests
except ImportError:
    pass  # Dependencies not installed


class BraveSession:
    """A session manager for Brave browser automation."""
    
    def __init__(self, brave_path: Optional[str] = None, headless: bool = False):
        """Initialize a Brave browser session.
        
        Args:
            brave_path: Path to Brave browser executable. If None, will try to auto-detect.
            headless: Whether to run in headless mode.
        """
        self.brave_path = brave_path
        self.headless = headless
        self.driver = None
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
    
    def start(self):
        """Start the Brave browser session."""
        if 'webdriver' not in globals():
            raise ImportError("selenium not installed. Install with: pip install selenium webdriver-manager")
            
        options = Options()
        
        # Common Brave browser paths
        brave_paths = [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",  # macOS
            "/usr/bin/brave-browser",  # Linux
            "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",  # Windows
            "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",  # Windows 32-bit
        ]
        
        if self.brave_path:
            options.binary_location = self.brave_path
        else:
            # Try to find Brave browser automatically
            import os
            for path in brave_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    break
        
        if self.headless:
            options.add_argument("--headless")
        
        # Brave-specific options for better compatibility
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=options
            )
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            raise RuntimeError(f"Failed to start Brave browser: {e}") from e
    
    def stop(self):
        """Stop the Brave browser session."""
        if self.driver:
            self.driver.quit()
            self.driver = None


def check_brave_rewards_api(url: str) -> bool:
    """Check if a URL supports Brave Rewards via BAT.
    
    Args:
        url: The URL to check for Brave Rewards support.
        
    Returns:
        True if the URL appears to support Brave Rewards, False otherwise.
    """
    if 'requests' not in globals():
        raise ImportError("requests not installed. Install with: pip install requests")
    
    try:
        response = requests.get(url, timeout=10)
        # Check for common Brave Rewards indicators
        content = response.text.lower()
        brave_indicators = [
            'brave-rewards',
            'basic attention token',
            'bat-ads',
            'brave-publisher'
        ]
        return any(indicator in content for indicator in brave_indicators)
    except requests.RequestException:
        return False


def get_brave_user_agent() -> str:
    """Get a common Brave browser user agent string.
    
    Returns:
        A Brave browser user agent string.
    """
    return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36")
{%- endif %}