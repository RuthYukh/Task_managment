

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Pending")

# Create tables within the application context
# with app.app_context():
#     db.create_all()


VALID_STATUSES = ["Pending", "In Progress", "Completed"]


# Routes
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'status': task.status} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json

    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    status = data.get('status', 'Pending')
    if status not in VALID_STATUSES:
        return jsonify({'error': 'Invalid status'}), 400
    
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    status = data.get('status')
    if status and status not in VALID_STATUSES:
        return jsonify({'error': f'Invalid status. valis statuses are: {", ".join(VALID_STATUSES)}'}), 400
    
    task.status = status if status else task.status
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
