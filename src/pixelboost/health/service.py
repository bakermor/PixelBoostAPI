from ..models import User, Stat, Health


async def update(user: User, health: Health):
    setattr(user, 'health', health)
    await user.save()
    return user

async def update_one(user: User, stat: str, stat_update: Stat):
    setattr(user.health, stat, stat_update)
    await user.save()
    return user
