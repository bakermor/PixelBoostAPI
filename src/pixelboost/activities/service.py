from beanie import PydanticObjectId
from bson import DBRef

from .models import ActivityBase, ActivityUpdate
from ..exceptions import ACTIVITY_CONFLICT, ACTIVITY_NOT_FOUND, NOT_OWNER
from ..models import User, Activity


async def create(activity: ActivityBase, user: User) -> Activity:
    activity_data = activity.model_dump()
    activity_out = await Activity.insert_one(Activity(**activity_data))

    user.activities.append(activity_out.id)
    await user.save()

    return activity_out

async def get_all(user: User) -> list[Activity]:
    activities = []
    for activity_id in user.activities:
        activities += [await Activity.get(activity_id)]
    return activities

async def get(activity_id: PydanticObjectId, user: User) -> Activity:
    if activity_id not in user.activities:
        raise NOT_OWNER

    activity = await Activity.get(activity_id)
    if not activity:
        raise ACTIVITY_NOT_FOUND

    return activity

async def start(activity_id: PydanticObjectId, time: float, user: User):
    activity = await Activity.get(activity_id)
    if not activity:
        raise ACTIVITY_NOT_FOUND

    activity.start_time = time
    await activity.save()

    user.current_activity = activity
    await user.save()

async def stop(activity_id: PydanticObjectId, user: User):
    activity = await Activity.get(activity_id)
    if not activity:
        raise ACTIVITY_NOT_FOUND

    activity.start_time = None
    await activity.save()

    user.current_activity = None
    await user.save()

async def update(activity_id: PydanticObjectId, updated_activity: ActivityUpdate, user: User) -> Activity:
    if activity_id not in user.activities:
        raise NOT_OWNER

    activity = await Activity.get(activity_id)
    if not activity:
        raise ACTIVITY_NOT_FOUND

    # Update original modifiers without overwriting them
    update_data = updated_activity.model_dump(exclude_unset=True)
    original = activity.modifiers.model_dump()
    original.update(update_data["modifiers"])

    update_data["modifiers"] = original
    await Activity.find_one(Activity.id == activity_id).update({"$set": update_data})

    activity_out = await Activity.get(activity_id)
    return activity_out

async def delete(activity_id: PydanticObjectId, user: User):
    if activity_id not in user.activities:
        raise NOT_OWNER

    activity = await Activity.get(activity_id)
    if not activity:
        raise ACTIVITY_NOT_FOUND

    user.activities.remove(activity_id)
    await user.save()
    await activity.delete()
