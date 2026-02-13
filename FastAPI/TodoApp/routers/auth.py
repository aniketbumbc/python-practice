from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter()


@router.get("/auth/")
async def auth():
    return {"user": "user authenticated"}