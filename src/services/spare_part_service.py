from sqlalchemy.orm import Session
from src.models.spare_part import SparePart


class SparePartAvailability:
    """Enumeration for spare part availability status."""
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    PRICE_UNDEFINED = "price_undefined"


class SparePartService:
    """Service for managing spare parts with business logic."""

    @staticmethod
    def check_availability(spare_part: SparePart) -> str:
        """
        Check spare part availability according to business rules:
        - Available: quantity > 0 AND price is defined (not NULL)
        - Out of stock: quantity <= 0
        - Price undefined: quantity > 0 BUT price is NULL
        
        Args:
            spare_part: The spare part to check
            
        Returns:
            Availability status string
        """
        # TODO: Implement availability check logic
        raise NotImplementedError("Spare part availability check not yet implemented")

    @staticmethod
    def get_spare_part_by_number(session: Session, part_number: str) -> SparePart:
        """
        Get a spare part by its part number.
        
        Args:
            session: Database session
            part_number: The part number to search for
            
        Returns:
            SparePart object or None if not found
        """
        return session.query(SparePart).filter(SparePart.part_number == part_number).first()

    @staticmethod
    def create_spare_part(
        session: Session,
        name: str,
        part_number: str,
        quantity: int = 0,
        price: float = None,
    ) -> SparePart:
        """
        Create a new spare part.
        
        Args:
            session: Database session
            name: Part name
            part_number: Unique part number
            quantity: Initial quantity in stock
            price: Part price
            
        Returns:
            Created SparePart object
            
        Raises:
            ValueError: If quantity is negative
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        spare_part = SparePart(
            name=name,
            part_number=part_number,
            quantity=quantity,
            price=price,
        )
        session.add(spare_part)
        session.commit()
        return spare_part

    @staticmethod
    def update_quantity(session: Session, spare_part_id: int, quantity: int) -> bool:
        """
        Update spare part quantity.
        
        Args:
            session: Database session
            spare_part_id: ID of spare part to update
            quantity: New quantity
            
        Returns:
            True if updated successfully, False otherwise
            
        Raises:
            ValueError: If quantity is negative
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        spare_part = session.query(SparePart).filter(SparePart.id == spare_part_id).first()
        
        if not spare_part:
            return False
        
        spare_part.quantity = quantity
        session.commit()
        return True

