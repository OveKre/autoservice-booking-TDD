"""Initial schema - Create bookings and spare_parts tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-11-03 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema - CREATE TABLES"""
    
    # Create bookings table
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_email', sa.String(255), nullable=False),
        sa.Column('service_type', sa.String(255), nullable=False),
        sa.Column('booking_datetime', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('booking_datetime > created_at', name='check_booking_future')
    )
    
    # Create index for faster queries
    op.create_index('idx_booking_datetime', 'bookings', ['booking_datetime'], unique=False)
    op.create_index('idx_customer_email', 'bookings', ['customer_email'], unique=False)
    
    # Create spare_parts table
    op.create_table(
        'spare_parts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('part_number', sa.String(100), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('part_number', name='uq_part_number')
    )
    
    # Create index for faster queries
    op.create_index('idx_part_number', 'spare_parts', ['part_number'], unique=False)


def downgrade() -> None:
    """Downgrade database schema - DROP TABLES"""
    
    # Drop spare_parts table
    op.drop_index('idx_part_number', table_name='spare_parts')
    op.drop_table('spare_parts')
    
    # Drop bookings table
    op.drop_index('idx_customer_email', table_name='bookings')
    op.drop_index('idx_booking_datetime', table_name='bookings')
    op.drop_table('bookings')

