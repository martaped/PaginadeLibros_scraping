import requests
from bs4 import BeautifulSoup
import csv

# URL base de la página
BASE_URL = "http://books.toscrape.com/"

def scrape_books(url):
    """
    Función para scrapear los libros de una página.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: No se pudo acceder a {url}")
        return []

    # Parsear el contenido HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Lista para guardar los datos
    books = []

    # Encontrar todos los libros en la página
    for book in soup.find_all('article', class_='product_pod'):
        # Extraer el título del libro
        title = book.h3.a['title']
        
        # Extraer el precio
        price = book.find('p', class_='price_color').text.strip()
        
        # Extraer disponibilidad
        availability = book.find('p', class_='instock availability').text.strip()
        
        # Extraer la URL de la imagen
        image_url = book.find('img')['src']
        # Completar la URL de la imagen si es relativa
        full_image_url = BASE_URL + image_url.replace('../', '')

        # Guardar los datos del libro
        books.append({
            'title': title,
            'price': price,
            'availability': availability,
            'image': full_image_url
        })
    
    return books

def scrape_all_pages():
    """
    Función para scrapear todos los libros en todas las páginas.
    """
    page = 1
    all_books = []

    while True:
        print(f"Scrapeando página {page}...")
        url = f"{BASE_URL}catalogue/page-{page}.html"
        books = scrape_books(url)
        
        if not books:
            break  # Salir del bucle si no hay libros (fin de las páginas)
        
        all_books.extend(books)
        page += 1

    return all_books

def save_to_csv(books, filename='books_with_images.csv'):
    """
    Guardar los datos en un archivo CSV.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'price', 'availability', 'image'])
        writer.writeheader()
        writer.writerows(books)

    print(f"Datos extraídos y guardados en {filename}")

if __name__ == "__main__":
    # Scrape todos los libros
    all_books = scrape_all_pages()

    # Guardar los datos en un archivo CSV
    save_to_csv(all_books)
