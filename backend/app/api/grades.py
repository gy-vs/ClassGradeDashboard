from flask import Blueprint, jsonify, request, send_file
from app.models.grade import store
import os
import tempfile

bp = Blueprint('grades', __name__, url_prefix='/api')

@bp.route('/grades', methods=['GET'])
def get_grades():
    data = store.get_all()
    return jsonify({'data': data})

@bp.route('/grades', methods=['POST'])
def add_grade():
    data = request.json
    name = data.get('name')
    subject = data.get('subject')
    score = data.get('score')
    
    if not all([name, subject, score]):
        return jsonify({'error': '缺少必要参数'}), 400
    
    try:
        score = float(score)
        if score < 0 or score > 100:
            return jsonify({'error': '分数必须在0-100之间'}), 400
    except ValueError:
        return jsonify({'error': '分数必须是数字'}), 400
    
    store.add(name, subject, score)
    return jsonify({'message': '添加成功'})

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    stats = store.get_statistics()
    if stats is None:
        return jsonify({'message': '暂无数据'})
    return jsonify(stats)

@bp.route('/rankings', methods=['GET'])
def get_rankings():
    rankings = store.get_rankings()
    return jsonify({'data': rankings})

@bp.route('/distribution', methods=['GET'])
def get_distribution():
    distribution = store.get_distribution()
    if distribution is None:
        return jsonify({'message': '暂无数据'})
    return jsonify(distribution)

@bp.route('/import', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': '未上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': '文件格式错误，请上传Excel文件'}), 400
    
    temp_path = tempfile.mktemp(suffix='.xlsx')
    file.save(temp_path)
    
    try:
        store.import_excel(temp_path)
        os.unlink(temp_path)
        return jsonify({'message': '导入成功'})
    except Exception as e:
        os.unlink(temp_path)
        return jsonify({'error': f'导入失败: {str(e)}'}), 500

@bp.route('/template', methods=['GET'])
def download_template():
    template = store.get_template()
    temp_path = tempfile.mktemp(suffix='.xlsx')
    template.to_excel(temp_path, index=False)
    return send_file(temp_path, download_name='成绩导入模板.xlsx', as_attachment=True)
