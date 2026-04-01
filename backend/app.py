from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import io
import os
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = 'grades_data.json'
SUBJECTS = ['语文', '数学', '英语', '物理', '化学']

SAMPLE_DATA = [
    {'姓名': '张三', '语文': 85, '数学': 92, '英语': 78, '物理': 88, '化学': 90},
    {'姓名': '李四', '语文': 92, '数学': 88, '英语': 95, '物理': 90, '化学': 94},
    {'姓名': '王五', '语文': 78, '数学': 95, '英语': 80, '物理': 85, '化学': 82},
    {'姓名': '赵六', '语文': 88, '数学': 76, '英语': 92, '物理': 79, '化学': 85},
    {'姓名': '孙七', '语文': 95, '数学': 91, '英语': 89, '物理': 93, '化学': 91},
    {'姓名': '周八', '语文': 72, '数学': 68, '英语': 75, '物理': 70, '化学': 65},
    {'姓名': '吴九', '语文': 80, '数学': 85, '英语': 82, '物理': 81, '化学': 79},
    {'姓名': '郑十', '语文': 65, '数学': 58, '英语': 70, '物理': 62, '化学': 68},
    {'姓名': '陈一', '语文': 89, '数学': 94, '英语': 87, '物理': 91, '化学': 92},
    {'姓名': '刘二', '语文': 76, '数学': 82, '英语': 79, '物理': 84, '化学': 80}
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                return SAMPLE_DATA
            return data
    return SAMPLE_DATA

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/api/grades', methods=['GET'])
def get_grades():
    data = load_data()
    return jsonify(data)

@app.route('/api/grades', methods=['POST'])
def add_grade():
    data = load_data()
    new_entry = request.json
    
    for entry in data:
        if entry['姓名'] == new_entry['姓名']:
            entry.update(new_entry)
            save_data(data)
            return jsonify({'message': '成绩更新成功', 'data': entry})
    
    data.append(new_entry)
    save_data(data)
    return jsonify({'message': '成绩添加成功', 'data': new_entry})

@app.route('/api/grades/<name>', methods=['DELETE'])
def delete_grade(name):
    data = load_data()
    data = [entry for entry in data if entry['姓名'] != name]
    save_data(data)
    return jsonify({'message': '删除成功'})

@app.route('/api/import', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    try:
        df = pd.read_excel(file)
        required_columns = ['姓名', '语文', '数学', '英语', '物理', '化学']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'error': f'模板缺少列: {col}'}), 400
        
        data = load_data()
        imported_count = 0
        
        for _, row in df.iterrows():
            new_entry = {col: int(row[col]) if col != '姓名' else str(row[col]) for col in required_columns}
            
            exists = False
            for i, entry in enumerate(data):
                if entry['姓名'] == new_entry['姓名']:
                    data[i] = new_entry
                    exists = True
                    break
            
            if not exists:
                data.append(new_entry)
            imported_count += 1
        
        save_data(data)
        return jsonify({'message': f'成功导入 {imported_count} 条数据', 'count': imported_count})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/template', methods=['GET'])
def download_template():
    data = {
        '姓名': ['张三', '李四', '王五'],
        '语文': [85, 92, 78],
        '数学': [90, 88, 95],
        '英语': [82, 95, 80],
        '物理': [88, 90, 85],
        '化学': [86, 94, 82]
    }
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)
    return send_file(
        output,
        download_name='成绩导入模板.xlsx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/api/statistics/subjects', methods=['GET'])
def get_subject_statistics():
    data = load_data()
    if not data:
        return jsonify({})
    
    df = pd.DataFrame(data)
    result = {}
    
    for subject in SUBJECTS:
        scores = df[subject].astype(int)
        result[subject] = {
            '平均分': round(scores.mean(), 1),
            '最高分': int(scores.max()),
            '最低分': int(scores.min()),
            '及格率': round((scores >= 60).sum() / len(scores) * 100, 1),
            '优秀率': round((scores >= 90).sum() / len(scores) * 100, 1)
        }
    
    return jsonify(result)

@app.route('/api/statistics/overview', methods=['GET'])
def get_overview():
    data = load_data()
    if not data:
        return jsonify({
            '总人数': 0,
            '总平均分': 0,
            '总及格率': 0,
            '总优秀率': 0
        })
    
    df = pd.DataFrame(data)
    all_scores = []
    pass_count = 0
    excellent_count = 0
    total_count = len(df) * len(SUBJECTS)
    
    for subject in SUBJECTS:
        scores = df[subject].astype(int)
        all_scores.extend(scores.tolist())
        pass_count += (scores >= 60).sum()
        excellent_count += (scores >= 90).sum()
    
    return jsonify({
        '总人数': len(df),
        '总平均分': round(np.mean(all_scores), 1),
        '总及格率': round(pass_count / total_count * 100, 1),
        '总优秀率': round(excellent_count / total_count * 100, 1)
    })

@app.route('/api/statistics/ranking', methods=['GET'])
def get_ranking():
    data = load_data()
    if not data:
        return jsonify([])
    
    df = pd.DataFrame(data)
    
    df['总分'] = df[SUBJECTS].astype(int).sum(axis=1)
    df = df.sort_values('总分', ascending=False).reset_index(drop=True)
    
    result = df.to_dict('records')
    for i, item in enumerate(result):
        item['排名'] = i + 1
        item['平均分'] = round(item['总分'] / len(SUBJECTS), 1)
    
    return jsonify(result)

@app.route('/api/statistics/distribution', methods=['GET'])
def get_distribution():
    data = load_data()
    if not data:
        return jsonify({})
    
    df = pd.DataFrame(data)
    result = {}
    
    bins = [0, 60, 70, 80, 90, 101]
    labels = ['0-59', '60-69', '70-79', '80-89', '90-100']
    
    for subject in SUBJECTS:
        scores = df[subject].astype(int)
        hist = pd.cut(scores, bins=bins, labels=labels, right=False).value_counts().sort_index()
        result[subject] = hist.to_dict()
    
    overall_dist = {}
    all_scores = []
    for subject in SUBJECTS:
        all_scores.extend(df[subject].astype(int).tolist())
    
    overall_hist = pd.cut(pd.Series(all_scores), bins=bins, labels=labels, right=False).value_counts().sort_index()
    result['整体'] = overall_hist.to_dict()
    
    return jsonify(result)

@app.route('/api/clear', methods=['POST'])
def clear_data():
    save_data([])
    return jsonify({'message': '数据已清空'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
