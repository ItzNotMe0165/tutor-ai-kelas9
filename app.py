import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("AI_API_KEY"))

SYSTEM_PROMPT = """
Kamu adalah "CLORX", asisten belajar yang ramah, pintar, dan sabar untuk siswa kelas 9 SMP di Indonesia.
Jawab pertanyaan dengan bahasa yang mudah dipahami anak SMP.
Gunakan langkah-langkah yang jelas untuk soal hitungan.
Gunakan analogi sederhana dari kehidupan sehari-hari.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tanya', methods=['POST'])
def tanya_ai():
    data = request.get_json()
    pertanyaan = data.get('pertanyaan')
    
    if not pertanyaan:
        return jsonify({'error': 'Pertanyaan tidak boleh kosong'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": pertanyaan}
            ]
        )
        jawaban = response.choices[0].message.content
        return jsonify({'jawaban': jawaban})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Maaf, terjadi kesalahan pada server'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
