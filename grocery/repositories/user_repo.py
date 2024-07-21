import sqlalchemy as sa
from pydantic import EmailStr

from grocery.repositories.base_repo import BaseRepository
from grocery.enums import UserRole
from grocery.dto import UserDto
from grocery.models import User


class UserRepository(BaseRepository):
    async def get_one_by_email(self, email: EmailStr) -> UserDto | None:
        stmt = (
            sa
            .select(User)
            .where(User.email == email)
        )
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        return UserDto.one_from_orm(user)

    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[UserDto]:
        stmt = (
            sa
            .select(User)
            .offset(offset=offset)
            .limit(limit=limit)
            .order_by(User.id.desc())
        )
        users = (await self.session.execute(stmt)).scalars().all()
        return UserDto.many_from_orm(users)
    
    async def get_count_records(self) -> int:
        stmt = (
            sa
            .select(sa.func.count())
            .select_from(User)
        )
        total = (await self.session.execute(stmt)).scalar_one()
        return total

    async def create(self, *, email: str, password: bytes, role: UserRole) -> UserDto:
        user = User(
            email=email,
            password=password,
            role=role
        )
        self.session.add(user)
        await self.session.flush()
        return UserDto.one_from_orm(user)
