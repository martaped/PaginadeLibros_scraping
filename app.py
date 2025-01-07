from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def read_csv(file_path):
    books = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append({
                'title': row['title'],
                'price': row['price'],
                'availability': row['availability'],
                'image': row.get('image', 'default.jpg')
            })
    return books

@app.route("/")
def home():
    books = read_csv('books_with_images.csv')  # Cambia por tu archivo CSV
    return render_template('index.html', books=books)

@app.route("/process_order", methods=["POST"])

def process_order():
    # Leer todos los libros disponibles
    all_books = read_csv('books_with_images.csv')

    # Obtener los libros seleccionados desde el formulario
    selected_titles = request.form.getlist("selected_books")

    # Filtrar los libros seleccionados con sus precios
    selected_books = [
        {"title": book["title"], "price": float(book["price"].replace("£", ""))}
        for book in all_books
        if book["title"] in selected_titles
    ]
    if not selected_books:
        return "No ha libros seleccionados. Regrese y seleccione los libros."
        # Calcular el total
    total_price = sum(book["price"] for book in selected_books)

    # Renderizar el resumen del pedido
    return render_template(
        "order_summary.html",
        selected_books=selected_books,
        total_price=total_price
    )

if __name__ == "__main__":
    app.run(debug=True)
