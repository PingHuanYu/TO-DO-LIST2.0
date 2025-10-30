from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# 初始化 Flask app 和資料庫
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # 使用 SQLite 資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 關閉不必要的訊息
db = SQLAlchemy(app)
ma = Marshmallow(app)

# 任務資料表模型
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title):
        self.title = title

# 任務資料的序列化模型
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

# 創建資料庫（如果資料庫還不存在）
with app.app_context():
    db.create_all()

# 取得所有任務的 API (Read)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()  # 查詢所有任務
    task_schema = TaskSchema(many=True)  # 序列化多個任務
    return jsonify(task_schema.dump(tasks))  # 回傳任務清單的 JSON 格式

# 根據 ID 取得單一任務的 API (Read)
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)  # 查詢單一任務，如果沒有則回傳 404
    task_schema = TaskSchema()  # 序列化單一任務
    return jsonify(task_schema.dump(task))  # 回傳任務的 JSON 格式

# 新增任務的 API (Create)
@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']  # 從請求中取得任務標題
    new_task = Task(title=title)  # 建立新的任務物件
    db.session.add(new_task)  # 把新的任務加入資料庫
    db.session.commit()  # 提交變更

    task_schema = TaskSchema()  # 序列化新任務
    return jsonify(task_schema.dump(new_task)), 201  # 回傳新增的任務資料，並設置 HTTP 狀態碼為 201

# 更新任務的 API (Update)
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)  # 查詢要更新的任務

    title = request.json.get('title', task.title)  # 取得新的標題（若沒有則使用舊的標題）
    completed = request.json.get('completed', task.completed)  # 取得新的完成狀態（若沒有則使用舊的狀態）

    task.title = title
    task.completed = completed

    db.session.commit()  # 提交更新的資料

    task_schema = TaskSchema()  # 序列化更新後的任務
    return jsonify(task_schema.dump(task))  # 回傳更新後的任務資料

# 刪除任務的 API (Delete)
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)  # 查詢要刪除的任務
    db.session.delete(task)  # 刪除任務
    db.session.commit()  # 提交變更
    return '', 204  # 返回無內容的回應，並設置 HTTP 狀態碼為 204

if __name__ == '__main__':
    app.run(debug=True)