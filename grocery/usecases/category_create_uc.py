from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories.category_repo import CategoryRepository


class CategoryCreateUseCase(BaseUseCase):
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self) -> ...:
        ...
