from .models import StatUpdate, HealthUpdate, EquationUpdate
from ..models import User


async def update(user: User, health_update: HealthUpdate):
    initial_health = getattr(user, 'health').model_dump()
    update_data = health_update.model_dump(exclude_unset=True)
    for stat in initial_health:
        initial_health[stat].update(update_data[stat])

    setattr(user, 'health', initial_health)
    await user.save()
    return user

async def update_one(user: User, stat: str, stat_update: StatUpdate):
    initial_stat = getattr(user.health, stat).model_dump()
    update_data = stat_update.model_dump(exclude_unset=True)
    initial_stat.update(update_data)

    setattr(user.health, stat, initial_stat)
    await user.save()
    return user

async def equation_update(user: User, updated_data: EquationUpdate):
    initial_health = getattr(user, 'health').model_dump()
    for stat, value in updated_data:
        initial_equation = initial_health[stat]['equation']
        initial_equation[0] = value
        initial_health[stat]['equation'] = initial_equation

    setattr(user, 'health', initial_health)
    await user.save()
    return user
