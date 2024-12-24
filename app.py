from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

users = []

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    number = request.form['number']
    photo = request.files['photo']

    if photo and photo.filename.endswith('.png'):
        photo_filename = f"{number}.png"
        photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
        photo.save(photo_path)
        users.append({
            'name': name,
            'number': number,
            'photo': f'/{photo_path}'  # Doğru URL yolu sağlanıyor
        })
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/search_user', methods=['GET'])
def search_user():
    number = request.args.get('number')
    for user in users:
        if user['number'] == number:
            return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/delete/<int:user_index>', methods=['POST'])
def delete_user(user_index):
    if 0 <= user_index < len(users):
        users.pop(user_index)
        return redirect(url_for('index'))
    return jsonify({'error': 'Invalid user index'}), 400

if __name__ == '__main__':
    app.run(debug=True)
