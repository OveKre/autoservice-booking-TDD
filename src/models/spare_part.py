from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint, Index
from src.models.base import Base


class SparePart(Base):
    """Spare part model for autoservice inventory."""
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    part_number = Column(String(100), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
        Index('idx_part_number', 'part_number'),
    )

    def __repr__(self):
        return f"<SparePart(id={self.id}, name={self.name}, part_number={self.part_number}, quantity={self.quantity}, price={self.price})>"

