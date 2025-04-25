import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import pytz
from datetime import datetime

Base = declarative_base()

# Zona horaria de Colombia
colombia_tz = pytz.timezone('America/Bogota')

class Suppliers(Base):
    __tablename__ = "suppliers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    preferred_payment_method: Mapped[str] = mapped_column(sa.String(50))
    created_at: Mapped[sa.TIMESTAMP] = mapped_column(sa.TIMESTAMP, default=datetime.now(colombia_tz))

