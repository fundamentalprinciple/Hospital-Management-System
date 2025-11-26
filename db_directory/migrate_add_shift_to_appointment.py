"""
Migration script to add 'shift' column to Appointment table.
"""
from application.database import db
from sqlalchemy import Column, String

def upgrade():
    with db.engine.connect() as conn:
        conn.execute('ALTER TABLE appointment ADD COLUMN shift VARCHAR(16) NOT NULL DEFAULT "morning";')

def downgrade():
    with db.engine.connect() as conn:
        conn.execute('ALTER TABLE appointment DROP COLUMN shift;')
