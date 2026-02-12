from flask import Flask, request, render_template, send_file, redirect, url_for
import csv
import os
from werkzeug.utils import secure_filename
import xlsxwriter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# 确保上传目录存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件部分
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # 检查文件是否为空
    if file.filename == '':
        return redirect(request.url)
    # 检查文件是否为CSV
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 转换CSV为XLSX
        xlsx_filename = filename.rsplit('.', 1)[0] + '.xlsx'
        xlsx_filepath = os.path.join(app.config['UPLOAD_FOLDER'], xlsx_filename)
        
        try:
            # 使用纯Python处理CSV和生成XLSX
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                rows = list(csv_reader)
            
            # 创建XLSX文件
            workbook = xlsxwriter.Workbook(xlsx_filepath)
            worksheet = workbook.add_worksheet()
            
            # 写入数据
            for row_num, row in enumerate(rows):
                for col_num, value in enumerate(row):
                    worksheet.write(row_num, col_num, value)
            
            workbook.close()
            
            # 清除临时CSV文件
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # 提供下载链接
            return redirect(url_for('download_file', filename=xlsx_filename))
        except Exception as e:
            # 清除临时文件
            if os.path.exists(filepath):
                os.remove(filepath)
            if os.path.exists(xlsx_filepath):
                os.remove(xlsx_filepath)
            return f"转换失败: {str(e)}"
    else:
        return "只允许上传CSV文件"

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        # 发送文件后删除
        response = send_file(filepath, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return response
    else:
        return "文件不存在"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
