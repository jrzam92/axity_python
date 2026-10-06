import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.acceso_datos_orm.database import Base
from src.acceso_datos_orm.models import User, Order, OrderItem
from src.acceso_datos_orm.crud import create_user, get_user_by_email

# URL especial de SQLite para crear la base de datos en RAM (se borra al terminar)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    # Setup
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine) # Crea las tablas
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session # Entrega la sesión a la prueba
    
    # Teardown
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_crud_user_and_order(db_session):
    # 1. Probar crear usuario
    user = create_user(db_session, name="Polux", email="polux@test.com")
    assert user.id is not None
    assert user.name == "Polux"
    
    # 2. Comprobar lectura
    fetched_user = get_user_by_email(db_session, "polux@test.com")
    assert fetched_user is not None
    
    # 3. Probar relación con Orders y OrderItems
    new_order = Order(user_id=user.id)
    new_item = OrderItem(product_name="Teclado Mecánico", quantity=1, price=95.50)
    new_order.items.append(new_item)
    
    db_session.add(new_order)
    db_session.commit()
    
    # Verificamos que la relación funcione en cascada
    assert len(user.orders) == 1
    assert user.orders[0].items[0].product_name == "Teclado Mecánico"