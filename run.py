from godisbilen.app import create_app

app = create_app(create_db=True)

if __name__ == "__main__":
    app.run(debug=True)
    