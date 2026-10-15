from app import create_app

# Instancia a aplicação Flask chamando a factory
app = create_app()

if __name__ == '__main__':
    # Roda o servidor de desenvolvimento
    app.run()