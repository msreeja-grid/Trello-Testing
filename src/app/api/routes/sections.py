from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.board import Board
from app.models.section import Section
from app.models.invitation import Invitation
from app.models.user import User
from app.schemas.section import SectionCreate, SectionOut, SectionUpdate

router = APIRouter(prefix="/sections", tags=["sections"])


def board_accessible(board: Board, current_user: User, db: Session):
    if not board:
        return False
    if board.owner_id == current_user.id:
        return True
    return db.query(Invitation).filter(
        Invitation.board_id == board.id,
        Invitation.invited_user_id == current_user.id
    ).first() is not None


@router.post("/", response_model=SectionOut)
def create_section(
    section_data: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board = db.query(Board).filter(Board.id == section_data.board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only board owner can create sections")

    new_section = Section(**section_data.model_dump())
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    return new_section


@router.get("/{section_id}", response_model=SectionOut)
def get_section(section_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")

    board = db.query(Board).filter(Board.id == section.board_id).first()
    if not board_accessible(board, current_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return section


@router.patch("/{section_id}", response_model=SectionOut)
def update_section(
    section_id: int,
    section_data: SectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")

    board = db.query(Board).filter(Board.id == section.board_id).first()
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only board owner can update sections")

    if section_data.name is not None:
        section.name = section_data.name
    if section_data.description is not None:
        section.description = section_data.description

    db.commit()
    db.refresh(section)
    return section


@router.delete("/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")

    board = db.query(Board).filter(Board.id == section.board_id).first()
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only board owner can delete sections")

    db.delete(section)
    db.commit()
    return {"detail": "Section deleted"}
