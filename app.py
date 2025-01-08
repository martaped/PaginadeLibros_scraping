from flask import Flask, render_template, request
import csv
from flask_frozen import Freezer


app = Flask(__name__)

freezer = Freezer(app)

# Leer datos desde un archivo CSV
def read_csv(file_path):
    books = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append({
                'title': row['title'],
                'price': row['price'],
                'availability': row['availability'],
                'image': row.get('image', 'libro.jpg')
            })
    return books

@app.route("/")
def home():
    books = read_csv('books_with_images.csv')
    return render_template('index.html', books=books)

@app.route("/process_order", methods=["POST"])
def process_order():
    all_books = read_csv('books_with_images.csv')
    selected_titles = request.form.getlist("selected_books")
    selected_books = [
        {"title": book["title"], "price": float(book["price"].replace("£", ""))}
        for book in all_books
        if book["title"] in selected_titles
    ]
    if not selected_books:
        return "No ha libros seleccionados. Regrese y seleccione los libros."
    total_price = sum(book["price"] for book in selected_books)
    return render_template("order_summary.html", selected_books=selected_books, total_price=total_price)

if __name__ == "__main__":
    import sys

    # Verifica si se debe ejecutar el servidor o congelar la aplicación
    if len(sys.argv) > 1 and sys.argv[1] == "freeze":
        freezer.freeze()  # Genera los archivos estáticos
        print("Sitio estático generado en la carpeta 'build'.")
    else:
        app.run(debug=True)  # Inicia el servidor Flask
