def add_project(collection,project,url,platform,desc):
    proj_details = {
        "platform":platform,
        "project": project,
        "url" : url,
        "description":desc,
        "status":0
    }
    try:
        collection.insert_many([proj_details])
    except:
        return False
    return True

