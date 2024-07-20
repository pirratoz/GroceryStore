from re import match

from fastapi import HTTPException


class Slug:
    @staticmethod
    def validate(slug: str):
        if not match(r"^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$", slug):
            raise HTTPException(
                status_code=422,
                detail="this not slug"
            )
