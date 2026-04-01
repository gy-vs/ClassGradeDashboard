import pandas as pd
import os

DATA_FILE = 'data/grades.xlsx'
SUBJECTS = ['语文', '数学', '英语', '物理', '化学']

class GradeStore:
    def __init__(self):
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(DATA_FILE):
            self._create_empty_file()
    
    def _create_empty_file(self):
        df = pd.DataFrame(columns=['姓名'] + SUBJECTS)
        init_data = [
            {'姓名': '王明辉', '语文': 92, '数学': 95, '英语': 88, '物理': 91, '化学': 89},
            {'姓名': '李晓燕', '语文': 88, '数学': 90, '英语': 95, '物理': 85, '化学': 87},
            {'姓名': '张伟强', '语文': 76, '数学': 82, '英语': 78, '物理': 80, '化学': 75},
            {'姓名': '刘芳', '语文': 95, '数学': 88, '英语': 92, '物理': 87, '化学': 91},
            {'姓名': '陈志远', '语文': 68, '数学': 75, '英语': 70, '物理': 72, '化学': 69},
            {'姓名': '赵雨萱', '语文': 85, '数学': 79, '英语': 90, '物理': 83, '化学': 86},
            {'姓名': '孙浩然', '语文': 72, '数学': 68, '英语': 65, '物理': 70, '化学': 73},
            {'姓名': '周思琪', '语文': 90, '数学': 93, '英语': 87, '物理': 94, '化学': 92},
            {'姓名': '吴俊杰', '语文': 58, '数学': 62, '英语': 55, '物理': 60, '化学': 59},
            {'姓名': '郑丽娜', '语文': 82, '数学': 85, '英语': 80, '物理': 78, '化学': 84}
        ]
        df = pd.concat([df, pd.DataFrame(init_data)], ignore_index=True)
        df.to_excel(DATA_FILE, index=False)
    
    def get_all(self):
        df = pd.read_excel(DATA_FILE)
        return df.to_dict('records')
    
    def add(self, name, subject, score):
        df = pd.read_excel(DATA_FILE)
        if len(df) == 0 or name not in df['姓名'].values:
            new_row = {'姓名': name}
            for s in SUBJECTS:
                new_row[s] = None
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.loc[df['姓名'] == name, subject] = score
        df.to_excel(DATA_FILE, index=False)
        return True
    
    def import_excel(self, file_path):
        df_import = pd.read_excel(file_path)
        df_existing = pd.read_excel(DATA_FILE)
        
        for _, row in df_import.iterrows():
            name = row['姓名']
            if name not in df_existing['姓名'].values:
                df_existing = pd.concat([df_existing, pd.DataFrame([row])], ignore_index=True)
            else:
                for s in SUBJECTS:
                    if s in row and pd.notna(row[s]):
                        df_existing.loc[df_existing['姓名'] == name, s] = row[s]
        
        df_existing.to_excel(DATA_FILE, index=False)
        return True
    
    def get_template(self):
        template = pd.DataFrame(columns=['姓名'] + SUBJECTS)
        sample_data = [
            {'姓名': '张三', '语文': 85, '数学': 92, '英语': 78, '物理': 88, '化学': 90},
            {'姓名': '李四', '语文': 76, '数学': 85, '英语': 92, '物理': 79, '化学': 82}
        ]
        template = pd.concat([template, pd.DataFrame(sample_data)], ignore_index=True)
        return template
    
    def get_statistics(self):
        df = pd.read_excel(DATA_FILE)
        if len(df) == 0:
            return None
        
        stats = {}
        for subject in SUBJECTS:
            scores = df[subject].dropna()
            if len(scores) == 0:
                continue
            stats[subject] = {
                '平均分': round(scores.mean(), 1),
                '最高分': int(scores.max()),
                '最低分': int(scores.min()),
                '及格率': round((scores >= 60).sum() / len(scores) * 100, 1),
                '优秀率': round((scores >= 90).sum() / len(scores) * 100, 1)
            }
        
        overall_scores = df[SUBJECTS].stack()
        total_students = len(df)
        overall_avg = round(overall_scores.mean(), 1)
        overall_pass = round((overall_scores >= 60).sum() / len(overall_scores) * 100, 1)
        overall_excellent = round((overall_scores >= 90).sum() / len(overall_scores) * 100, 1)
        
        return {
            'subjects': stats,
            'overview': {
                'total_students': total_students,
                'average': overall_avg,
                'pass_rate': overall_pass,
                'excellent_rate': overall_excellent
            }
        }
    
    def get_rankings(self):
        df = pd.read_excel(DATA_FILE)
        if len(df) == 0:
            return []
        
        df['总分'] = df[SUBJECTS].sum(axis=1)
        df = df.sort_values('总分', ascending=False).reset_index(drop=True)
        return df.to_dict('records')
    
    def get_distribution(self):
        df = pd.read_excel(DATA_FILE)
        if len(df) == 0:
            return None
        
        bins = [0, 60, 70, 80, 90, 101]
        labels = ['0-59', '60-69', '70-79', '80-89', '90-100']
        
        distribution = {}
        for subject in SUBJECTS:
            scores = df[subject].dropna()
            hist = pd.cut(scores, bins=bins, labels=labels, right=False).value_counts()
            distribution[subject] = hist.to_dict()
        
        return distribution

store = GradeStore()
