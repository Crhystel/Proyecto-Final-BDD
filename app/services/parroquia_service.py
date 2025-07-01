from app.database import get_db_connection

def obtener_parroquias():
    db=get_db_connection()
    cursor=db.parroquias.find(
        {},
        {"_id":1,"nombre":1}
    )
    return list(cursor)