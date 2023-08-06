from assimilator.alchemy.database import AlchemyRepository as BaseAlchemyRepository
from assimilator.core.database import SpecificationType

from velait.common.exceptions import AlreadyDeletedError


class VelaitRepository(BaseAlchemyRepository):
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query=None,
    ):
        return super(VelaitRepository, self).filter(
            *specifications,
            lazy=lazy,
            initial_query=initial_query,
        )

    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query=None,
    ):
        return super(VelaitRepository, self).get(
            *specifications,
            lazy=lazy,
            initial_query=initial_query,
        )

    def delete(
        self,
        obj=None,
        *specifications: SpecificationType
    ) -> None:
        if obj is not None:
            if obj.is_deleted:
                raise AlreadyDeletedError()

            obj.is_deleted = True
        else:
            self.update(*specifications, is_deleted=True)


__all__ = [
    'VelaitRepository',
]
