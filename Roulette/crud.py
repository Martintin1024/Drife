from Utilities.helpers import supabase

def create_roulette_db(user_id, name_roulette):
    """Crea una ruleta y devuelve (True, nuevo_id) o (False, error)"""
    try:
        data_to_insert = {
            "user_id": user_id,
            "name_roulette": name_roulette
        }
        
        response = supabase.table("roulettes").insert(data_to_insert).execute()
        new_id = response.data[0]["roulette_id"]
        
        return True, new_id

    except Exception as e:
        return False, f"Error en la nube: {e}"

def get_user_roulettes(user_id):
    """Devuelve una lista de tuplas [(id, nombre), (id, nombre)...]"""
    try:
        response = supabase.table("roulettes").select("roulette_id, name_roulette").eq("user_id", user_id).execute()
        roulettes_data = response.data
        
        results = [(r["roulette_id"], r["name_roulette"]) for r in roulettes_data]
        return results

    except Exception:
        return []

def delete_roulette_db(user_id, roulette_id):
    """Borra una ruleta específica"""
    try:
        supabase.table("roulettes").delete().eq("roulette_id", roulette_id).eq("user_id", user_id).execute()
        return True
    except Exception:
        return False

def update_roulette_db(user_id, roulette_id, new_name):
    """Actualiza el nombre de la ruleta"""
    try:
        data_to_update = {"name_roulette": new_name}
        supabase.table("roulettes").update(data_to_update).eq("roulette_id", roulette_id).eq("user_id", user_id).execute()
        
        return True, "Nombre actualizado correctamente"
        
    except Exception as e:
        return False, f"Error en la nube: {e}"