from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

subjects = ['语文', '数学', '英语', '物理', '化学']

students_data = [
    {'姓名': '张伟', '语文': 85, '数学': 92, '英语': 78, '物理': 88, '化学': 90},
    {'姓名': '李娜', '语文': 92, '数学': 88, '英语': 85, '物理': 90, '化学': 87},
    {'姓名': '王强', '语文': 78, '数学': 95, '英语': 72, '物理': 82, '化学': 80},
    {'姓名': '刘洋', '语文': 88, '数学': 76, '英语': 90, '物理': 78, '化学': 85},
    {'姓名': '陈明', '语文': 95, '数学': 90, '英语': 88, '物理': 92, '化学': 93},
    {'姓名': '赵静', '语文': 72, '数学': 68, '英语': 75, '物理': 65, '化学': 70},
    {'姓名': '孙磊', '语文': 80, '数学': 85, '英语': 82, '物理': 87, '化学': 84},
    {'姓名': '周婷', '语文': 88, '数学': 92, '英语': 90, '物理': 85, '化学': 89},
    {'姓名': '吴涛', '语文': 65, '数学': 70, '英语': 68, '物理': 72, '化学': 66},
    {'姓名': '郑丽', '语文': 90, '数学': 85, '英语': 92, '物理': 88, '化学': 91}
]


def calculate_statistics():
    if not students_data:
        return None
    
    df = pd.DataFrame(students_data)
    stats = {}
    
    for subject in subjects:
        scores = df[subject]
        avg = round(scores.mean(), 2)
        max_score = int(scores.max())
        min_score = int(scores.min())
        pass_rate = round((scores >= 60).sum() / len(scores) * 100, 2)
        excellent_rate = round((scores >= 90).sum() / len(scores) * 100, 2)
        
        stats[subject] = {
            'average': avg,
            'max': max_score,
            'min': min_score,
            'pass_rate': pass_rate,
            'excellent_rate': excellent_rate
        }
    
    return stats


def calculate_distribution():
    if not students_data:
        return None
    
    df = pd.DataFrame(students_data)
    distribution = {'0-59': 0, '60-69': 0, '70-79': 0, '80-89': 0, '90-100': 0}
    
    for subject in subjects:
        scores = df[subject]
        for score in scores:
            if score < 60:
                distribution['0-59'] += 1
            elif score < 70:
                distribution['60-69'] += 1
            elif score < 80:
                distribution['70-79'] += 1
            elif score < 90:
                distribution['80-89'] += 1
            else:
                distribution['90-100'] += 1
    
    return distribution


def get_overview():
    if not students_data:
        return {
            'total_students': 0,
            'overall_average': 0,
            'overall_pass_rate': 0,
            'overall_excellent_rate': 0
        }
    
    df = pd.DataFrame(students_data)
    total_students = len(df)
    
    all_scores = []
    for subject in subjects:
        all_scores.extend(df[subject].tolist())
    
    overall_average = round(sum(all_scores) / len(all_scores), 2)
    
    pass_count = 0
    excellent_count = 0
    for score in all_scores:
        if score >= 60:
            pass_count += 1
        if score >= 90:
            excellent_count += 1
    
    overall_pass_rate = round(pass_count / len(all_scores) * 100, 2)
    overall_excellent_rate = round(excellent_count / len(all_scores) * 100, 2)
    
    return {
        'total_students': total_students,
        'overall_average': overall_average,
        'overall_pass_rate': overall_pass_rate,
        'overall_excellent_rate': overall_excellent_rate
    }


@app.route('/api/students', methods=['GET'])
def get_students():
    df = pd.DataFrame(students_data)
    if not df.empty:
        df['总分'] = df[subjects].sum(axis=1)
        df = df.sort_values('总分', ascending=False)
        df['排名'] = range(1, len(df) + 1)
        return jsonify(df.to_dict('records'))
    return jsonify([])


@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    required_fields = ['姓名'] + subjects
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少字段: {field}'}), 400
    
    for subject in subjects:
        try:
            data[subject] = float(data[subject])
            if data[subject] < 0 or data[subject] > 100:
                return jsonify({'error': f'{subject} 分数必须在0-100之间'}), 400
        except ValueError:
            return jsonify({'error': f'{subject} 必须是数字'}), 400
    
    students_data.append(data)
    return jsonify({'message': '添加成功', 'student': data}), 201


@app.route('/api/students/<int:index>', methods=['DELETE'])
def delete_student(index):
    if 0 <= index < len(students_data):
        students_data.pop(index)
        return jsonify({'message': '删除成功'})
    return jsonify({'error': '学生不存在'}), 404


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    stats = calculate_statistics()
    overview = get_overview()
    distribution = calculate_distribution()
    
    return jsonify({
        'overview': overview,
        'subject_stats': stats,
        'distribution': distribution
    })


@app.route('/api/import', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    try:
        df = pd.read_excel(file)
        required_columns = ['姓名'] + subjects
        
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'error': f'Excel缺少列: {col}'}), 400
        
        df = df[required_columns].copy()
        
        for subject in subjects:
            df[subject] = pd.to_numeric(df[subject], errors='coerce')
            if df[subject].isnull().any():
                return jsonify({'error': f'{subject} 列包含非数字值'}), 400
            if ((df[subject] < 0) | (df[subject] > 100)).any():
                return jsonify({'error': f'{subject} 列包含0-100范围外的值'}), 400
        
        for _, row in df.iterrows():
            student = {col: row[col] for col in required_columns}
            students_data.append(student)
        
        return jsonify({'message': f'成功导入 {len(df)} 条数据'})
    
    except Exception as e:
        return jsonify({'error': f'导入失败: {str(e)}'}), 400


@app.route('/api/template', methods=['GET'])
def download_template():
    data = {
        '姓名': ['张三', '李四', '王五'],
        '语文': [85, 92, 78],
        '数学': [90, 88, 95],
        '英语': [82, 76, 89],
        '物理': [78, 85, 91],
        '化学': [88, 90, 82]
    }
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='成绩模板')
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='成绩导入模板.xlsx'
    )


@app.route('/api/clear', methods=['POST'])
def clear_data():
    students_data.clear()
    return jsonify({'message': '数据已清空'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
