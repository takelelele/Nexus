# Nexus

#### Nexus - A very simple but super effective storage of information about different organizations

---

## Requirements
* alembic 1.15.1
* django-environ 0.12.0
* fastapi 0.115.11
* psycopg2 2.9.10
* sqlalchemy 2.0.39
* uvicorn 0.34.0

---

## Installation
To start working with Nexus app, you need to clone the current repository
```
git clone https://github.com/takelelele/Nexus.git
```
Create a .env file in the /app directory and note the environment variables
```text
DB_USERNAME=***
DB_PASSWORD=***
DB_DATABASE=NexusDB
DB_HOST=db

POSTGRES_USER=***
POSTGRES_PASSWORD=***
POSTGRES_DB=NexusDB

PGUSER=***
PGPASSWORD=***
PGDATABASE=NexusDB
PGHOST=db
```
1. The first paragraph is environment variables for connecting the application to the database
2. In the second we define variables for the database
3. In the third we specify data for executing psql commands inside the application 

( Usually they are all the same )

Next you need to go to the Nexus folder and run the docker container
```
docker-compose up -d
```

Congratulations! The application is running and running at [0.0.0.0:8000](http://localhost:8000)

---

## API Documentation( SwaggerUI | Redoc )

You can view the documentation at [`localhost:8000/docs`](http://localhost:8000/docs) or [`localhost:8000/redoc`](http://localhost:8000/redoc)

---
## Methods

Get information about an organization by its id, use [`/org/by_id/{org_id}`](http://localhost:8000/org/by_id/{org_id}1)

+ **org_id**: *Integer* - Organization id

```python
@router.get("/by_id/{org_id}")
async def org_by_id(org_id: int, db: Session = Depends(get_db)):
    return await get_org_by_id(org_id, db)
```

You can get the data of the organization(s) that are located in the building using [`/org/by_building/{building_id}`](http://localhost:8000/org/by_building/1)( GET )

+ **building_id**: *Integer* - Id of the building in which the organization is located

```python
@router.get("/by_building/{building_id}")
async def org_by_building(building_id: int, db: Session = Depends(get_db)):
    return await get_orgs_by_build(building_id, db)
```

To get an organization by its activities, use [`/org/by_activity/{activity_id}`](http://localhost:8000/org/by_activity/1)( GET )

+ **activity_id**: *Integer* - Organization activity id

```python
@router.get("/by_activity/{activity_id}")
async def org_by_activity(activity_id: int, db: Session = Depends(get_db)):
    return await get_orgs_by_activity(activity_id, db)
```

This method will return not only an organization for a specific activity, but also organizations with nested activities
 [`/org/by_activity_in_tree/{root_activity_id}`](http://localhost:8000/org/by_activity_in_tree/1)( GET )

+ **root_activity_id**: *Integer* - Organization activity id

```python
@router.get("/by_activity_in_tree/{root_activity_id}")
async def org_by_activity_in_tree(root_activity_id: int, db: Session = Depends(get_db)):
    return await get_org_by_activities_tree(root_activity_id, db)
```

This method will help you find an organization by its name (or part of the name) [`/org/by_name/{org_name}`](http://localhost:8000/org/by_name/"Белый")( GET )

+ **org_name**: *String* - Organization name

```python
@router.get("/by_name/{org_name}")
async def org_by_name(org_name: str, db: Session = Depends(get_db)):
    return await get_org_by_name(org_name, db)
```

Allows you to add new activities [`/activity/add_activity`]("")( POST )

Query arguments:
+ **activity_name**: *String* - Activity name
+ **parent_id**: *Integer* - Parenting activity (Optional, default=None)

```python
@router.post("/add_activity")
async def new_activity(activity_name: str, parent_id: int = None, db: Session = Depends(get_db)):
    return await add_activity(activity_name, parent_id, db)
```