from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.order import Order
from ..schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse
from ..dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Crea una nueva orden (requiere autenticación)"""
    db_order = Order(**order_data.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=OrderListResponse)
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: str | None = Query(None, pattern="^(pending|completed|cancelled)$"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Lista órdenes con paginación y filtros (requiere autenticación)"""
    query = db.query(Order).filter(Order.is_active == True)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    total = query.count()
    orders = query.offset(skip).limit(limit).all()
    
    return {"total": total, "orders": orders}

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Obtiene una orden por ID (requiere autenticación)"""
    order = db.query(Order).filter(Order.id == order_id, Order.is_active == True).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Actualiza una orden (requiere autenticación)"""
    order = db.query(Order).filter(Order.id == order_id, Order.is_active == True).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Actualizar solo campos proporcionados
    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Elimina (soft delete) una orden (requiere autenticación)"""
    order = db.query(Order).filter(Order.id == order_id, Order.is_active == True).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    order.is_active = False
    db.commit()
    return None