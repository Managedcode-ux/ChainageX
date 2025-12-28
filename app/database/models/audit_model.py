from sqlalchemy import Column,Integer,String,DateTime,Text
from datetime import datetime, timezone
from app.database.dbConfig import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer,primary_key=True)
    table_name = Column(String,nullable=False)
    record_id = Column(Integer,nullable=False)
    action = Column(String,nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_at = Column(DateTime,default=lambda: datetime.now(timezone.utc))