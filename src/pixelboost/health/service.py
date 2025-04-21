from ..models import User, Stat, Health
from .models import StatUpdate


async def update(user: User, health: Health):
    setattr(user, 'health', health)
    await user.save()
    return user

async def update_one(user: User, stat: str, stat_update: StatUpdate):
    current_stat = getattr(user.health, stat).model_dump()
    update_data = stat_update.model_dump(exclude_unset=True)
    current_stat.update(update_data)

    setattr(user.health, stat, current_stat)
    await user.save()
    return user
