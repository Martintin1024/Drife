from Utilities.helpers import supabase

def register_user(email, user_name, password):
    if not email.strip() or not user_name.strip() or not password.strip():
        return False, "Campos vacíos"

    try:
        # Creamos el usuario y guardamos el user_name en los metadatos internos
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "user_name": user_name 
                }
            }
        })
        return True, "¡Usuario creado! Por favor, revisa tu correo para verificar la cuenta."
        
    except Exception as e:
        print(f"auth register error: {e}")
        return False, "Error al registrar. Puede que el correo ya exista o la contraseña sea débil."

def login_user(email, password):
    try:
        # El usuario intenta iniciar sesión usando la conexión compartida
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            user_id = response.user.id
            user_name = response.user.user_metadata.get("user_name", "")
            
            # Como ya inició sesión, creamos/actualizamos su perfil en la tabla pública
            try:
                supabase.table("users").upsert({
                    "user_id": user_id,
                    "email": email,
                    "user_name": user_name
                }).execute()
            except Exception as e:
                print(f"Error guardando el perfil en la tabla users: {e}")

            return user_id
            
        return None

    except Exception as e:
        print(f"auth login error: {e}")
        return None