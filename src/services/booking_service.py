from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.booking import Booking, BookingStatus
from src.utils.datetime_provider import DatetimeProvider


class BookingService:
    """Service for managing bookings with business logic."""

    # Working hours constants
    WORKING_HOUR_START = 8
    WORKING_HOUR_END = 17
    MIN_ADVANCE_HOURS = 24

    @staticmethod
    def _is_within_working_hours(booking_datetime: datetime) -> bool:
        """Check if time is within working hours (8:00-17:00)."""
        return (
            BookingService.WORKING_HOUR_START <= booking_datetime.hour 
            < BookingService.WORKING_HOUR_END
        )

    @staticmethod
    def _is_weekday(booking_datetime: datetime) -> bool:
        """Check if date is a weekday (Monday-Friday)."""
        return booking_datetime.weekday() < 5  # Monday=0, Friday=4

    @staticmethod
    def _is_sufficient_advance_notice(booking_datetime: datetime) -> bool:
        """Check if booking is at least 24 hours in the future."""
        now = DatetimeProvider.now()
        min_booking_time = now + timedelta(hours=BookingService.MIN_ADVANCE_HOURS)
        return booking_datetime > min_booking_time

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
        return (
            BookingService._is_sufficient_advance_notice(booking_datetime)
            and BookingService._is_weekday(booking_datetime)
            and BookingService._is_within_working_hours(booking_datetime)
        )

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
        # TODO: Implement cancellation logic
        raise NotImplementedError("Booking cancellation not yet implemented")

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

