"""Tests for booking cancellation."""
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest
from src.models.booking import Booking, BookingStatus
from src.services.booking_service import BookingService


class TestBookingCancellation:
    """Test suite for booking cancellation rules."""

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_allow_cancellation_3_hours_before(self, mock_now, test_db):
        """Test that cancellation is allowed 3 hours before booking."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 13, 0),  # 3 hours later
            status=BookingStatus.CONFIRMED,
            created_at=datetime(2025, 11, 14, 10, 0),  # Created yesterday
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is True
        test_db.refresh(booking)
        assert booking.status == BookingStatus.CANCELLED

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_cancellation_1_hour_before(self, mock_now, test_db):
        """Test that cancellation is not allowed 1 hour before booking."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 11, 0),  # 1 hour later
            status=BookingStatus.CONFIRMED,
            created_at=datetime(2025, 11, 14, 10, 0),  # Created yesterday
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is False
        test_db.refresh(booking)
        assert booking.status == BookingStatus.CONFIRMED

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_cancellation_of_cancelled_booking(self, mock_now, test_db):
        """Test that already cancelled booking cannot be cancelled again."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 13, 0),
            status=BookingStatus.CANCELLED,
            created_at=datetime(2025, 11, 14, 10, 0),
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_cancellation_of_completed_booking(self, mock_now, test_db):
        """Test that completed booking cannot be cancelled."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 13, 0),
            status=BookingStatus.COMPLETED,
            created_at=datetime(2025, 11, 14, 10, 0),
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_cancellation_of_pending_booking(self, mock_now, test_db):
        """Test that pending booking cannot be cancelled."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 13, 0),
            status=BookingStatus.PENDING,
            created_at=datetime(2025, 11, 14, 10, 0),
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is False

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_cancellation_exactly_2_hours_before(self, mock_now, test_db):
        """Test that cancellation is not allowed exactly 2 hours before booking (must be MORE than 2 hours)."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 12, 0),  # Exactly 2 hours later
            status=BookingStatus.CONFIRMED,
            created_at=datetime(2025, 11, 14, 10, 0),
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is False
        test_db.refresh(booking)
        assert booking.status == BookingStatus.CONFIRMED

    @patch('src.utils.datetime_provider.DatetimeProvider.now')
    def test_should_not_allow_cancellation_less_than_2_hours_before(self, mock_now, test_db):
        """Test that cancellation is not allowed less than 2 hours before booking."""
        # Arrange
        now = datetime(2025, 11, 15, 10, 0)
        mock_now.return_value = now

        booking = Booking(
            customer_email="test@example.com",
            service_type="Oil Change",
            booking_datetime=datetime(2025, 11, 15, 11, 59),  # Less than 2 hours
            status=BookingStatus.CONFIRMED,
            created_at=datetime(2025, 11, 14, 10, 0),
        )
        test_db.add(booking)
        test_db.commit()

        # Act
        result = BookingService.cancel_booking(test_db, booking.id)

        # Assert
        assert result is False

    def test_should_return_false_for_nonexistent_booking(self, test_db):
        """Test that cancelling non-existent booking returns False."""
        # Act
        result = BookingService.cancel_booking(test_db, 999)
        
        # Assert
        assert result is False

