from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

app = Flask(__name__)

def generate_meme_image(image_file, top_text, bottom_text):
    print(f"DEBUG: Rozpoczynam generowanie mema dla pliku: {image_file.filename}") # Debug
    try:
        img = Image.open(image_file).convert("RGB")
        print("DEBUG: Obrazek otwarty pomyślnie.") # Debug
    except Exception as e:
        print(f"ERROR: Błąd podczas otwierania obrazka: {e}") # Debug
        raise # Ponowne zgłoszenie błędu, aby zobaczyć go w konsoli Flask

    draw = ImageDraw.Draw(img)

    try:
        font_path = "static/fonts/impact.ttf"
        print(f"DEBUG: Próbuję załadować czcionkę z: {font_path}") # Debug
        font_size = int(img.height / 10)
        font = ImageFont.truetype(font_path, font_size)
        print("DEBUG: Czcionka załadowana pomyślnie.") # Debug
    except IOError as e:
        print(f"WARNING: Nie znaleziono czcionki Impact: {e}. Używam domyślnej.") # Debug
        font = ImageFont.load_default()
    except Exception as e:
        print(f"ERROR: Inny błąd podczas ładowania czcionki: {e}") # Debug
        font = ImageFont.load_default()


    def draw_text(text, y):
        # Ta część jest w porządku
        w, h = draw.textbbox((0,0), text, font=font)[2:] # Zmiana na textbbox dla Pillow 9+
        x = (img.width - w) / 2
        outline_range = 2
        for dx in range(-outline_range, outline_range + 1):
            for dy in range(-outline_range, outline_range + 1):
                draw.text((x + dx, y + dy), text, font=font, fill="black")
        draw.text((x, y), text, font=font, fill="white")

    if top_text:
        draw_text(top_text.upper(), y=10)
    if bottom_text:
        # Pamiętaj, że draw.textsize jest przestarzałe w nowszych wersjach Pillow
        # Warto użyć draw.textbbox dla precyzyjniejszego obliczenia rozmiaru tekstu
        # Dla obecnego kodu, jeśli font_size jest prawidłowe, powinno działać.
        # Sprawdź, czy ImageFont.load_default() ma sensowny rozmiar dla wysokości obrazu.
        bottom_text_y = img.height - font_size - 20
        if bottom_text_y < 10: # Proste sprawdzenie, aby tekst nie wychodził poza obrazek
            print("WARNING: Tekst dolny może być zbyt duży lub obrazek zbyt mały.")
        draw_text(bottom_text.upper(), y=bottom_text_y)

    filename = f"meme_{uuid.uuid4().hex[:8]}.jpg"
    output_path = os.path.join("static/images", filename)
    print(f"DEBUG: Próbuję zapisać obrazek do: {output_path}") # Debug
    try:
        img.save(output_path, "JPEG")
        print("DEBUG: Obrazek zapisany pomyślnie.") # Debug
    except Exception as e:
        print(f"ERROR: Błąd podczas zapisywania obrazka: {e}") # Debug
        raise # Ponowne zgłoszenie błędu, aby zobaczyć go w konsoli Flask

    return filename

@app.route('/generate_meme', methods=['POST'])
def generate_meme():
    try:
        if 'image' not in request.files:
            print("ERROR: Brak pliku 'image' w żądaniu.") # Debug
            return jsonify({'error': 'Brak pliku obrazu'}), 400

        image_file = request.files['image']
        top_text = request.form.get('top_text', '')
        bottom_text = request.form.get('bottom_text', '')

        print(f"DEBUG: Otrzymano żądanie: plik={image_file.filename}, tekst_górny='{top_text}', tekst_dolny='{bottom_text}'") # Debug

        filename = generate_meme_image(image_file, top_text, bottom_text)
        print(f"DEBUG: Mem wygenerowany: {filename}") # Debug
        return jsonify({'filename': filename})
    except Exception as e:
        print(f"GLOBAL ERROR: Wystąpił błąd w ścieżce /generate_meme: {e}") # Debug
        # Zwróć szczegółowy błąd do klienta (tylko w trybie debugowania!)
        return jsonify({'error': f'Wystąpił błąd serwera: {str(e)}'}), 500

@app.route("/")
def home():
    return render_template("layout.html")

if __name__ == "__main__":
    # Upewnij się, że foldery istnieją podczas uruchamiania aplikacji, jeśli nie chcesz ich tworzyć ręcznie
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/fonts', exist_ok=True)
    app.run(debug=True)
