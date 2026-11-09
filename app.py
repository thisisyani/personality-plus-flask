from flask import Flask, render_template, request

app = Flask(__name__)

jawaban_kelemahan = []
jawaban_kelebihan = []

# --- PARENT CLASS (CETAKAN KALKULATOR) ---
class EvaluatorKuis:
    def __init__(self, daftar_jawaban):
        self.jawaban = daftar_jawaban
        self.skor = {"sanguinis": 0, "koleris": 0, "melankolis": 0, "plegmatis": 0}

    def hitung_total_skor(self):
        for jwb in self.jawaban:
            if jwb in self.skor:
                self.skor[jwb] += 1
        return self.skor

# --- PILAR INHERITANCE (CHILD CLASS) ---
class EvaluatorKombinasi(EvaluatorKuis):
    penjelasan_tipe = {
        "Sanguinis": {
            "deskripsi": "Kamu adalah pribadi yang hangat, ramah, dan mudah bergaul. Kamu cenderung optimis dan suka bersosialisasi dengan orang lain.",
            "kekuatan": "Optimis, ceria, komunikatif, penuh energi, dan pandai menghidupkan suasana.",
            "tantangan": "Mudah kehilangan fokus, cenderung impulsif, dan kadang kurang terorganisir."
        },
        "Koleris": {
            "deskripsi": "Kamu adalah pribadi yang tegas, berorientasi pada tujuan, dan memiliki jiwa kepemimpinan yang kuat. Kamu cenderung mandiri dan suka mengambil inisiatif.",
            "kekuatan": "Tegas, memiliki jiwa pemimpin yang kuat, berorientasi pada target, dan mandiri.",
            "tantangan": "Cenderung dominan, tidak sabaran, dan bisa terlihat kurang berempati."
        },
        "Melankolis": {
            "deskripsi": "Kamu adalah pribadi yang analitis, perfeksionis, dan sangat memperhatikan detail. Kamu cenderung introspektif dan memiliki standar tinggi terhadap diri sendiri maupun orang lain.",
            "kekuatan": "Analitis, mendalam, teratur, perfeksionis, dan sangat berbakat dalam hal detail.",
            "tantangan": "Mudah stres karena terlalu perfeksionis, cenderung pesimis, dan sensitif."
        },
        "Plegmatis": {
            "deskripsi": "Kamu adalah pribadi yang tenang, damai, dan setia. Kamu cenderung menghindari konflik dan lebih suka menjaga keharmonisan dalam hubungan dengan orang lain.",
            "kekuatan": "Tenang, cinta damai, setia, pendengar yang baik, dan mudah beradaptasi.",
            "tantangan": "Cenderung menghindari konflik, kurang bermotivasi, dan sulit mengambil keputusan."
        },
        "Sanguinis-Plegmatis": {
            "deskripsi": "Kamu merupakan pribadi yang hangat, mudah bergaul, dan mampu mencairkan suasana. Di saat yang sama, kamu juga cenderung tenang, mudah beradaptasi, dan berusaha menjaga keharmonisan hubungan dengan orang lain.",
            "kekuatan": "Sangat ramah dan menyenangkan, suka bersosialisasi tapi tetap kalem, serta pembawa damai di kelompok.",
            "tantangan": "Cenderung menunda pekerjaan dan kurang tegas dalam mengambil sikap."
        },
        "Sanguinis-Koleris": {
            "deskripsi": "Kamu adalah pribadi yang karismatik, penuh energi, dan percaya diri. Kamu mampu memimpin dan memotivasi orang lain, namun juga cenderung impulsif dan suka mengambil alih situasi.",
            "kekuatan": "Karismatik, penuh energi, percaya diri, mudah memimpin, dan mampu memengaruhi serta memotivasi orang lain.",
            "tantangan": "Cenderung impulsif, tidak sabar, suka mengambil alih situasi, dan terkadang berbicara tanpa mempertimbangkan dampaknya."
        },
        "Sanguinis-Melankolis": {
            "deskripsi": "Kamu adalah pribadi yang kreatif, ekspresif, dan hangat. Kamu mampu menyeimbangkan semangat dengan perhatian terhadap detail, namun juga mudah mengalami perubahan suasana hati.",
            "kekuatan": "Kreatif, ekspresif, hangat, serta mampu menyeimbangkan semangat dengan perhatian terhadap detail.",
            "tantangan": "Mudah mengalami perubahan suasana hati, sensitif terhadap kritik, dan kadang terlalu banyak berpikir."
        },
        "Koleris-Melankolis": {
            "deskripsi": "Kamu adalah pribadi yang analitis, terorganisir, dan berorientasi pada tujuan. Kamu mampu merencanakan dengan baik dan memiliki standar tinggi terhadap diri sendiri maupun orang lain.",
            "kekuatan": "Strategis, terorganisir, berorientasi target, dan memiliki standar kualitas yang tinggi.",
            "tantangan": "Perfeksionis, kritis terhadap diri sendiri maupun orang lain, dan sulit menerima kesalahan."
        },
        "Koleris-Plegmatis": {
            "deskripsi": "Kamu adalah pribadi yang tenang namun tegas, mampu mengambil keputusan dengan kepala dingin, dan dapat diandalkan dalam memimpin. Kamu cenderung stabil dan menjaga keharmonisan dalam hubungan.",
            "kekuatan": "Tenang namun tegas, mampu mengambil keputusan dengan kepala dingin, stabil, dan dapat diandalkan dalam memimpin.",
            "tantangan": "Cenderung keras kepala, sulit mengubah keputusan yang sudah dibuat, dan kadang kurang ekspresif dalam menyampaikan perasaan."
        },
        "Melankolis-Plegmatis": {
            "deskripsi": "Kamu adalah pribadi yang tenang, introspektif, dan penuh perhatian. Kamu cenderung analitis dan perfeksionis, namun juga mampu menjaga keharmonisan dalam hubungan dengan orang lain.",
            "kekuatan": "Sabar, setia, penuh perhatian, pendengar yang baik, dan dapat diandalkan.",
            "tantangan": "Menghindari konflik, sulit mengambil keputusan cepat, dan cenderung menyimpan perasaan sendiri."
        }
    }
        
    def dapatkan_temperamen_dominan(self):
        skor_terurut = sorted(self.skor.items(), key=lambda x: x[1], reverse=True)
        tipe_1, skor_1 = skor_terurut[0]
        tipe_2, skor_2 = skor_terurut[1]
        
        if (skor_1 - skor_2) <= 1 and skor_2 > 0:
            return f"{tipe_1.capitalize()}-{tipe_2.capitalize()}"
        else:
            return tipe_1.capitalize()

    # Ambil penjelasan berdasarkan hasil kuis
    def dapatkan_deskripsi(self, tipe_hasil):
        # Jika tipe kombinasi belum terdaftar di kamus -> template default aman
        if tipe_hasil in self.penjelasan_tipe:
            return self.penjelasan_tipe[tipe_hasil]
        else:
            # Ambil data dari komponen pertama jika kombinasinya belum terdaftar 
            tipe_tunggal = tipe_hasil.split('-')[0]
            return self.penjelasan_tipe.get( tipe_tunggal, {"deskripsi": "-", "kekuatan": "-","tantangan": "-"})                                               

# --- ALUR FLASK WEB ---
@app.route('/')
def home():
    return render_template('index.html')

# 1. Halaman Pertama (Kelemahan) 
@app.route('/kelebihan', methods=['POST'])
def kelebihan():
    nama = request.form.get('nama_user')
    
    global jawaban_kelemahan
    jawaban_kelemahan = [value for key, value in request.form.items() if key != 'nama_user']
    
    return render_template('kelebihan.html', nama_user=nama)

# 2. Halaman Kedua (Kelebihan) 
@app.route('/hitung', methods=['POST'])
def hitung():
    nama = request.form.get('nama_user')
   
    global jawaban_kelebihan
    jawaban_kelebihan = [value for key, value in request.form.items() if key != 'nama_user']
   
    total_semua_jawaban = jawaban_kelemahan + jawaban_kelebihan
    
    kalkulator = EvaluatorKombinasi(total_semua_jawaban)
    
    skor_akhir = kalkulator.hitung_total_skor()
    hasil_dominan = kalkulator.dapatkan_temperamen_dominan()
    
    deskripsi = kalkulator.dapatkan_deskripsi(hasil_dominan)
    print(deskripsi)
    return render_template('result.html', 
                           nama_user=nama, 
                           hasil=hasil_dominan, 
                           detail_skor=skor_akhir,
                           deskripsi=deskripsi['deskripsi'],
                           kekuatan=deskripsi['kekuatan'],    # Dikirim ke HTML
                           tantangan=deskripsi['tantangan'])  # Dikirim ke HTML


if __name__ == '__main__':
    app.run(debug=True)
