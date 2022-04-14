def add_project(collection,project,url,platform):
    proj_details = {
        "platform":platform,
        "project": project,
        "url" : url,
        "status":0
    }
    try:
        collection.insert_many([proj_details])
    except:
        return False
    return True

