from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.board import Board
from app.models.section import Section
from app.models.ticket import Ticket
from app.models.invitation import Invitation
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["tickets"])


def board_accessible(board: Board, current_user: User, db: Session):
    if not board:
        return False
    if board.owner_id == current_user.id:
        return True
    return db.query(Invitation).filter(
        Invitation.board_id == board.id,
        Invitation.invited_user_id == current_user.id
    ).first() is not None


def ticket_editable(ticket: Ticket, current_user: User, board: Board):
    if board.owner_id == current_user.id:
        return True
    return ticket.created_by == current_user.id


@router.post("/", response_model=TicketOut)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    section = db.query(Section).filter(Section.id == ticket_data.section_id).first()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")

    board = db.query(Board).filter(Board.id == section.board_id).first()
    if not board_accessible(board, current_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    new_ticket = Ticket(
        name=ticket_data.name,
        description=ticket_data.description,
        section_id=ticket_data.section_id,
        assigned_to=ticket_data.assigned_to,
        created_by=current_user.id,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    section = db.query(Section).filter(Section.id == ticket.section_id).first()
    board = db.query(Board).filter(Board.id == section.board_id).first()
    if not board_accessible(board, current_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return ticket


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    section = db.query(Section).filter(Section.id == ticket.section_id).first()
    board = db.query(Board).filter(Board.id == section.board_id).first()
    if not ticket_editable(ticket, current_user, board):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only ticket owner or board owner can update this ticket")

    if ticket_data.section_id is not None:
        new_section = db.query(Section).filter(Section.id == ticket_data.section_id).first()
        if not new_section or new_section.board_id != board.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Section must belong to the same board")
        ticket.section_id = ticket_data.section_id

    if ticket_data.name is not None:
        ticket.name = ticket_data.name
    if ticket_data.description is not None:
        ticket.description = ticket_data.description
    if ticket_data.assigned_to is not None:
        ticket.assigned_to = ticket_data.assigned_to

    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    section = db.query(Section).filter(Section.id == ticket.section_id).first()
    board = db.query(Board).filter(Board.id == section.board_id).first()
    if not ticket_editable(ticket, current_user, board):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only ticket owner or board owner can delete this ticket")

    db.delete(ticket)
    db.commit()
    return {"detail": "Ticket deleted"}
