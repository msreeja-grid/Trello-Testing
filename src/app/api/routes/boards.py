from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import uuid4

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.board import Board
from app.models.invitation import Invitation
from app.models.section import Section
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.board import BoardCreate, BoardOut, BoardDetail, InvitationCreate

router = APIRouter(prefix="/boards", tags=["boards"])


def board_accessible(board: Board, current_user: User, db: Session):
    if board.owner_id == current_user.id:
        return True
    return db.query(Invitation).filter(
        Invitation.board_id == board.id,
        Invitation.invited_user_id == current_user.id
    ).first() is not None


@router.post("/", response_model=BoardOut)
def create_board(board: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_board = Board(**board.model_dump(), owner_id=current_user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


@router.get("/", response_model=list[BoardOut])
def get_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    boards = db.query(Board).filter(
        or_(
            Board.owner_id == current_user.id,
            Board.id.in_(
                db.query(Invitation.board_id).filter(Invitation.invited_user_id == current_user.id)
            )
        )
    ).all()
    return boards


@router.get("/{board_id}", response_model=BoardDetail)
def get_board(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if not board_accessible(board, current_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    sections = db.query(Section).filter(Section.board_id == board.id).all()
    tickets = db.query(Ticket).join(Section).filter(Section.board_id == board.id).all()
    invited_users = [invite.invited_user for invite in board.invitations]
    users = [board.owner] + invited_users
    invitations = [invite.token for invite in board.invitations]

    return {
        "id": board.id,
        "name": board.name,
        "description": board.description,
        "owner_id": board.owner_id,
        "sections": sections,
        "tickets": tickets,
        "users": users,
        "invitations": invitations,
    }


@router.post("/{board_id}/invite")
def invite_board_member(
    board_id: int,
    invitation: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only board owner can invite users")

    invited_user = db.query(User).filter(User.email == invitation.email).first()
    if not invited_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if invited_user.id == board.owner_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner is already part of the board")

    existing_invitation = db.query(Invitation).filter(
        Invitation.board_id == board.id,
        Invitation.invited_user_id == invited_user.id
    ).first()
    if existing_invitation:
        return {"token": existing_invitation.token}

    token = uuid4().hex
    invitation_record = Invitation(
        board_id=board.id,
        invited_user_id=invited_user.id,
        token=token,
    )
    db.add(invitation_record)
    db.commit()
    db.refresh(invitation_record)

    return {"token": invitation_record.token}
