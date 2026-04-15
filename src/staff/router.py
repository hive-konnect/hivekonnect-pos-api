from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.auth.dependencies import CurrentOwner
from src.core.database import get_db

from . import schemas, service


router = APIRouter(tags=["Staff"])


@router.post("/shops/{shop_id}/staff", response_model=schemas.StaffCreateResponse)
def create_staff(
    shop_id: UUID,
    payload: schemas.StaffCreate,
    current_user: CurrentOwner,
    db: Session = Depends(get_db),
):
    if not service.owner_controls_shop(db, owner_id=current_user.id, shop_id=shop_id):
        raise HTTPException(status_code=404, detail="Shop not found")

    staff, pin = service.create_staff_member(
        db,
        shop_id=shop_id,
        display_name=payload.display_name,
        phone=payload.phone,
        role=payload.role,
    )
    return {"staff": staff, "pin": pin}


@router.get("/shops/{shop_id}/staff", response_model=list[schemas.StaffResponse])
def get_shop_staff(
    shop_id: UUID,
    current_user: CurrentOwner,
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    is_active: bool | None = Query(default=None),
):
    if not service.owner_controls_shop(db, owner_id=current_user.id, shop_id=shop_id):
        raise HTTPException(status_code=404, detail="Shop not found")

    return service.list_shop_staff(db, shop_id=shop_id, limit=limit, offset=offset, is_active=is_active)


@router.patch("/staff/{staff_id}/reset-pin", response_model=schemas.StaffPinResetResponse)
def reset_pin(staff_id: UUID, current_user: CurrentOwner, db: Session = Depends(get_db)):
    staff = service.get_staff_member(db, staff_id=staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    if not service.owner_controls_shop(db, owner_id=current_user.id, shop_id=staff.shop_id):
        raise HTTPException(status_code=403, detail="Not allowed")

    _, pin = service.reset_staff_pin(db, staff=staff)
    return {"staff_id": staff.id, "pin": pin}


@router.patch("/staff/{staff_id}/disable", response_model=schemas.StaffResponse)
def disable_staff(staff_id: UUID, current_user: CurrentOwner, db: Session = Depends(get_db)):
    staff = service.get_staff_member(db, staff_id=staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    if not service.owner_controls_shop(db, owner_id=current_user.id, shop_id=staff.shop_id):
        raise HTTPException(status_code=403, detail="Not allowed")

    return service.disable_staff_member(db, staff=staff)
