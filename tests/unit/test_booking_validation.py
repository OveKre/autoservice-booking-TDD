"""Tests for booking time validation."""
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest
from src.services.booking_service import BookingService


class TestBookingTimeValidation:
    """Test suite for booking time validation rules."""

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_allow_booking_tomorrow_at_10am(self, mock_now):
        """Test that booking tomorrow at 10:00 is allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 16, 10, 0)  # Thursday 10:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is True

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_booking_today(self, mock_now):
        """Test that booking today is not allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 15, 14, 0)  # Same day 14:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_booking_less_than_24_hours_ahead(self, mock_now):
        """Test that booking less than 24 hours ahead is not allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 16, 8, 0)  # Next day 8:00 (23 hours)
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_booking_on_saturday(self, mock_now):
        """Test that booking on Saturday is not allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 18, 10, 0)  # Saturday 10:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_booking_on_sunday(self, mock_now):
        """Test that booking on Sunday is not allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 19, 10, 0)  # Sunday 10:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_booking_before_8am(self, mock_now):
        """Test that booking before 8:00 is not allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 17, 7, 30)  # Friday 7:30
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_booking_after_5pm(self, mock_now):
        """Test that booking after 17:00 is not allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 17, 17, 0)  # Friday 17:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_allow_booking_at_8am(self, mock_now):
        """Test that booking at 8:00 is allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 17, 8, 0)  # Friday 8:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is True

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_allow_booking_at_4pm(self, mock_now):
        """Test that booking at 16:00 is allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 17, 16, 0)  # Friday 16:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is True

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_allow_booking_on_monday(self, mock_now):
        """Test that booking on Monday is allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 20, 10, 0)  # Monday 10:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is True

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_allow_booking_on_friday(self, mock_now):
        """Test that booking on Friday is allowed."""
        # Arrange
        mock_now.return_value = datetime(2025, 1, 15, 9, 0)  # Wednesday 9:00
        booking_time = datetime(2025, 1, 17, 10, 0)  # Friday 10:00
        
        # Act
        result = BookingService.validate_booking_time(booking_time)
        
        # Assert
        assert result is True

