{% if cookiecutter.brave_browser_support == "Y" -%}
"""Tests for Brave browser integration."""

import pytest
from unittest.mock import Mock, patch

from {{ cookiecutter.package_name }}.brave_integration import (
    BraveSession,
    check_brave_rewards_api,
    get_brave_user_agent,
)


def test_get_brave_user_agent():
    """Test getting Brave user agent string."""
    user_agent = get_brave_user_agent()
    assert "Chrome" in user_agent
    assert "Safari" in user_agent
    assert "Mozilla" in user_agent


def test_brave_session_init():
    """Test BraveSession initialization."""
    session = BraveSession(brave_path="/fake/path", headless=True)
    assert session.brave_path == "/fake/path"
    assert session.headless is True
    assert session.driver is None


@patch('{{ cookiecutter.package_name }}.brave_integration.requests')
def test_check_brave_rewards_api_positive(mock_requests):
    """Test checking for Brave Rewards support - positive case."""
    mock_response = Mock()
    mock_response.text = '<html><meta name="brave-rewards" content="enabled"></html>'
    mock_requests.get.return_value = mock_response
    
    result = check_brave_rewards_api("https://example.com")
    assert result is True
    mock_requests.get.assert_called_once_with("https://example.com", timeout=10)


@patch('{{ cookiecutter.package_name }}.brave_integration.requests')
def test_check_brave_rewards_api_negative(mock_requests):
    """Test checking for Brave Rewards support - negative case."""
    mock_response = Mock()
    mock_response.text = '<html><title>Regular Website</title></html>'
    mock_requests.get.return_value = mock_response
    
    result = check_brave_rewards_api("https://example.com")
    assert result is False


@patch('{{ cookiecutter.package_name }}.brave_integration.requests')
def test_check_brave_rewards_api_exception(mock_requests):
    """Test checking for Brave Rewards support with network exception."""
    mock_requests.get.side_effect = mock_requests.RequestException("Network error")
    
    result = check_brave_rewards_api("https://example.com")
    assert result is False


@pytest.mark.skipif(True, reason="Integration test - requires Brave browser installation")
def test_brave_session_context_manager():
    """Test BraveSession as context manager - integration test."""
    # This test would require Brave browser to be installed
    # Skipped by default to avoid CI failures
    with BraveSession(headless=True) as driver:
        assert driver is not None
        driver.get("https://brave.com")
        assert "Brave" in driver.title
{%- endif %}