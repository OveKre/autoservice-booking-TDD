"""Tests for spare part availability checking."""
import pytest
from src.models.spare_part import SparePart
from src.services.spare_part_service import SparePartService, SparePartAvailability


class TestSparePartAvailability:
    """Test suite for spare part availability rules."""

    def test_should_return_available_when_in_stock_and_priced(self):
        """Test that spare part is available when quantity > 0 and price is set."""
        # Arrange
        spare_part = SparePart(
            name="Oil Filter",
            part_number="OF-001",
            quantity=5,
            price=15.99,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.AVAILABLE

    def test_should_return_out_of_stock_when_quantity_zero(self):
        """Test that spare part is out of stock when quantity is 0."""
        # Arrange
        spare_part = SparePart(
            name="Oil Filter",
            part_number="OF-001",
            quantity=0,
            price=15.99,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.OUT_OF_STOCK

    def test_should_return_price_undefined_when_price_null(self):
        """Test that spare part has undefined price when price is NULL."""
        # Arrange
        spare_part = SparePart(
            name="Oil Filter",
            part_number="OF-001",
            quantity=5,
            price=None,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.PRICE_UNDEFINED

    def test_should_return_out_of_stock_when_negative_quantity(self):
        """Test that spare part is out of stock when quantity is negative."""
        # Arrange
        spare_part = SparePart(
            name="Oil Filter",
            part_number="OF-001",
            quantity=-1,
            price=15.99,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.OUT_OF_STOCK

    def test_should_return_price_undefined_when_quantity_one_and_price_null(self):
        """Test that spare part with quantity 1 but no price is price undefined."""
        # Arrange
        spare_part = SparePart(
            name="Brake Pad",
            part_number="BP-001",
            quantity=1,
            price=None,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.PRICE_UNDEFINED

    def test_should_return_available_when_quantity_one_and_priced(self):
        """Test that spare part with quantity 1 and price is available."""
        # Arrange
        spare_part = SparePart(
            name="Brake Pad",
            part_number="BP-001",
            quantity=1,
            price=25.50,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.AVAILABLE

    def test_should_return_available_when_large_quantity_and_priced(self):
        """Test that spare part with large quantity and price is available."""
        # Arrange
        spare_part = SparePart(
            name="Spark Plug",
            part_number="SP-001",
            quantity=100,
            price=5.99,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.AVAILABLE

    def test_should_return_out_of_stock_when_quantity_zero_and_price_null(self):
        """Test that spare part with quantity 0 and no price is out of stock."""
        # Arrange
        spare_part = SparePart(
            name="Battery",
            part_number="BAT-001",
            quantity=0,
            price=None,
        )
        
        # Act
        result = SparePartService.check_availability(spare_part)
        
        # Assert
        assert result == SparePartAvailability.OUT_OF_STOCK

