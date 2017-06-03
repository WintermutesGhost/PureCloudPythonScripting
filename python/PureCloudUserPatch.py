def addManagerName(user):
    try:
        managerId = user.manager.id
        managerName = getNameFromId(managerId)
    except AttributeError:
        return
    setattr(user,"managerName",managerName)
