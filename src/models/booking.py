from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, CheckConstraint, Index
from src.models.base import Base


class BookingStatus(str, Enum):
    """Booking status enumeration."""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class Booking(Base):
    """Booking model for autoservice appointments."""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    customer_email = Column(String(255), nullable=False)
    service_type = Column(String(255), nullable=False)
    booking_datetime = Column(DateTime, nullable=False)
    status = Column(SQLEnum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('booking_datetime > created_at', name='check_booking_future'),
        Index('idx_booking_datetime', 'booking_datetime'),
        Index('idx_customer_email', 'customer_email'),
    )

    def __repr__(self):
        return f"<Booking(id={self.id}, customer_email={self.customer_email}, booking_datetime={self.booking_datetime}, status={self.status})>"

