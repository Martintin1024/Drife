from Utilities.helpers import supabase

def create_option_db(roulette_id, option_name):
    if not option_name or not str(option_name).strip():
        return False, "El nombre no puede estar vacío"

    try:
        data_to_insert = {
            "roulette_id": roulette_id,
            "option_name": str(option_name).strip()
        }
        
        supabase.table("options").insert(data_to_insert).execute()
        return True, "Opción creada"

    except Exception as e:
        return False, f"Error en la nube: {e}"

def get_options_db(roulette_id):
    try:
        response = supabase.table("options").select("option_id, option_name").eq("roulette_id", roulette_id).execute()
        options_data = response.data
        
        results = [(o["option_id"], o["option_name"]) for o in options_data]
        return results

    except Exception:
        return []

def update_option_db(roulette_id, option_id, new_name):
    if not new_name or not str(new_name).strip():
        return False, "Nombre vacío"

    try:
        data_to_update = {"option_name": str(new_name).strip()}
        supabase.table("options").update(data_to_update).eq("option_id", option_id).eq("roulette_id", roulette_id).execute()
        
        return True, "Actualizado correctamente"
        
    except Exception as e:
        return False, f"Error en la nube: {e}"

def delete_option_db(roulette_id, option_id):
    try:
        supabase.table("options").delete().eq("option_id", option_id).eq("roulette_id", roulette_id).execute()
        return True, "Eliminado correctamente"
        
    except Exception as e:
        return False, f"Error en la nube: {e}"

def get_roulette_items_text(roulette_id):
    data = get_options_db(roulette_id)
    return [item[1] for item in data]