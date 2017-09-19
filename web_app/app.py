from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

with open('../df.pkl','rb') as f:
    df = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html',df=df)
    
@app.route('/resort')
def show_trails():
    resort = request.args.get('resort')
    return render_template('index.html',df=df)
    
@app.route('/get_trails')
def get_trails():
    resort = request.args.get('resort')
    print(resort)
    if resort:
        sub_df = df[df['resort'] == resort]
        id_name = zip(list(sub_df.index,list(sub_df['trail_name'])))
        data = [{"id": x[0], "name": x[1]} for x in id_name]
        print(data)
    return jsonify(data)
    
if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)