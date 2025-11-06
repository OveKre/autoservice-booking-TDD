from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.booking import Booking, BookingStatus
from src.utils.datetime_provider import DatetimeProvider


class BookingService:
    """Service for managing bookings with business logic."""

    @staticmethod
    def validate_booking_time(booking_datetime: datetime) -> bool:
        """
        Validate booking time according to business rules:
        - Must be at least 24 hours in the future
        - Must be within working hours (Monday-Friday, 8:00-17:00)
        
        Args:
            booking_datetime: The requested booking datetime
            
        Returns:
            True if valid, False otherwise
        """
        now = DatetimeProvider.now()
        
        # Check if booking is at least 24 hours in the future
        min_booking_time = now + timedelta(hours=24)
        if booking_datetime <= min_booking_time:
            return False
        
        # Check if booking is on a weekend (Monday=0, Sunday=6)
        if booking_datetime.weekday() >= 5:  # Saturday=5, Sunday=6
            return False
        
        # Check if booking is within working hours (8:00-17:00)
        if booking_datetime.hour < 8 or booking_datetime.hour >= 17:
            return False
        
        return True

    @staticmethod
    def create_booking(
        session: Session,
        customer_email: str,
        service_type: str,
        booking_datetime: datetime,
    ) -> Booking:
        """
        Create a new booking if validation passes.
        
        Args:
            session: Database session
            customer_email: Customer email address
            service_type: Type of service requested
            booking_datetime: Requested booking datetime
            
        Returns:
            Created Booking object
            
        Raises:
            ValueError: If booking time is invalid
        """
        if not BookingService.validate_booking_time(booking_datetime):
            raise ValueError("Invalid booking time")
        
        booking = Booking(
            customer_email=customer_email,
            service_type=service_type,
            booking_datetime=booking_datetime,
            status=BookingStatus.PENDING,
        )
        session.add(booking)
        session.commit()
        return booking

    @staticmethod
    def cancel_booking(session: Session, booking_id: int) -> bool:
        """
        Cancel a booking if conditions are met:
        - Booking must be in CONFIRMED status
        - Cancellation must be at least 2 hours before booking time
        
        Args:
            session: Database session
            booking_id: ID of booking to cancel
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        
        if not booking:
            return False
        
        # Check if booking is in CONFIRMED status
        if booking.status != BookingStatus.CONFIRMED:
            return False
        
        # Check if cancellation is at least 2 hours before booking time
        now = DatetimeProvider.now()
        min_cancellation_time = booking.booking_datetime - timedelta(hours=2)
        
        if now >= min_cancellation_time:
            return False
        
        booking.status = BookingStatus.CANCELLED
        session.commit()
        return True

    @staticmethod
    def confirm_booking(session: Session, booking_id: int) -> bool:
        """
        Confirm a pending booking.
        
        Args:
            session: Database session
            booking_id: ID of booking to confirm
            
        Returns:
            True if confirmed successfully, False otherwise
        """
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        
        if not booking:
            return False
        
        if booking.status != BookingStatus.PENDING:
            return False
        
        booking.status = BookingStatus.CONFIRMED
        session.commit()
        return True

