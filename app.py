from flask import Flask, render_template, request, redirect, url_for, session
from database import create_connection, create_table, insert_score, get_high_scores

app = Flask(__name__)
app.secret_key = '12345'
create_connection()
create_table()

@app.route('/')
def anasayfa():
    en_yuksek_puanlar = get_high_scores()
    return render_template('index.html', en_yuksek_puanlar=en_yuksek_puanlar)

@app.route('/quiz', methods=['GET', 'POST'])
def sınav():
    en_yuksek_puanlar = get_high_scores()
    if request.method == 'POST':
        cevaplar = []
        for i in range(1, 7):
            cevaplar.append(request.form.get(f'question{i}'))
        score = hesapla_puan(cevaplar)
        session['score'] = score
        insert_score(score)
        return redirect(url_for('sonuc'))
    return render_template('quiz.html', en_yuksek_puanlar=en_yuksek_puanlar)

@app.route('/result')
def sonuc():
    score = session.get('score')
    if score is None:
        return redirect(url_for('anasayfa'))
    en_yuksek_puanlar = get_high_scores()
    return render_template('result.html', score=score, en_yuksek_puanlar=en_yuksek_puanlar)

def hesapla_puan(cevaplar):
    dogru_cevaplar = ['c', 'a', 'b', 'b', 'b', 'c']
    score = sum([1 for i in range(len(cevaplar)) if cevaplar[i] == dogru_cevaplar[i]])
    return score

if __name__ == '__main__':
    app.run(debug=True)