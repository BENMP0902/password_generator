import sys
from generator.password_generator import generate_password

def main():

    if len(sys.argv) < 2:
        print("Uso : python main.py <longitud>")
        return
    
    try:
        length = int(sys.argv[1])
    except ValueError:
        print("Error: la longitud deber ser un número")
        return
    
    if length < 4:
        print("Error: la longitud minima es 4")
        return
    
    password = generate_password(length)

    print("Contraseña generada:", password)

if __name__ == "__main__":
    main()

