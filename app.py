from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load('rf_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            user_input = request.form['input_text']
            
            # Check if the input contains the word "kill"
            if "kill" in user_input.lower():
                prediction = "negative"
            
            else:
                # Transform the input text and make a prediction
                input_features = vectorizer.transform([user_input])
                prediction = model.predict(input_features)[0]
            
            return render_template('index.html', prediction=prediction)
        
        except KeyError:
            return render_template('index.html', error="Please enter some text to predict.")

if __name__ == '__main__':
    app.run(debug=True, port=5002)
