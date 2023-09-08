from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
#from model import db
from model1 import summary

# Flaskアプリの初期化
app = Flask(__name__)
# 接続するデータベースのURIを設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"


db = SQLAlchemy()

class Todo(db.Model):#db.Modelでモデルを作成
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String,nullable=False)
    assign = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    memo = db.Column(db.Text, nullable=False)
# FlaskアプリにSQLAlchemyを拡張する
db.init_app(app)#アプリとデータベースを適合
#model.pyで定義した設計図はスキーマを作成するための設計図
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    # データベース上の全てのデータを取得
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)


@app.route("/create",methods=['GET','POST'])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        #モデルのインスタンス
        todo = Todo(
            assign = request.form.get('assign'),
            phrase = request.form.get('phrase'),
            title = summary(request.form.get('title')),#要約文
            #request.form.get('title'),
            memo = request.form.get('memo')
           
        )
        #title = summary(request.form.get('title')),#要約文
        #return render_template("create2.html",title)
        # データベースに登録
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("create"))

# @app.route("/create2",methods=['GET','POST'])
# def create2():
#     if request.method == "GET":
#         return render_template("create2.html")
#     if request.method == "POST":
#         #モデルのインスタンス
#         todo = Todo(
#             assign = request.form.get('assign'),
#             #title = create.summary(request.form.get('title')),#要約文
#             title =request.form.get('title'),
#             memo = request.form.get('memo')
           
#         )
#         #return render_template("create2.html",title)
#         # データベースに登録
#         db.session.add(todo)
#         db.session.commit()
#         return redirect(url_for("index"))
    


@app.route("/detail/<id>")
# idを引数に渡す
def detail(id):
    if request.method == 'GET':
        # idに基づいたレコードを抽出
        detail_todo = Todo.query.get_or_404(id)
        return render_template("detail.html",todo = detail_todo)

@app.route("/delete/<id>")
def delete(id):
    if request.method == 'GET':
        delete_todo = Todo.query.get_or_404(id)
        db.session.delete(delete_todo)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/update/<id>", methods=["GET","POST"])
def update(id):
    if request.method == "GET":
        update_todo = Todo.query.get_or_404(id)
        return render_template("update.html", todo = update_todo)
    else:
        # 更新するレコードを選択
        update_todo = Todo.query.get_or_404(id)
        # 送信した値に元データを更新
        update_todo.assign = request.form.get("assign")
        update_todo.title = request.form.get("title")
        update_todo.memo = request.form.get("memo")
        # データベースに反映
        db.session.commit()
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)





