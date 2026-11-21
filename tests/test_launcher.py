import os, ast, zipfile
base='/mnt/data/ReallyVisualsLauncher'
os.makedirs(os.path.join(base,'tests'),exist_ok=True)
test_code = '''import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / "ReallyVisualsLauncher.py"


def test_launcher_source_has_valid_python_syntax():
    source = SOURCE_FILE.read_text(encoding="utf-8")
    ast.parse(source, filename=str(SOURCE_FILE))


def test_all_requested_minecraft_versions_are_configured():
    tree = ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))
    versions = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "VERSIONS"
                   for target in node.targets):
                versions = ast.literal_eval(node.value)
                break

    assert versions is not None, "VERSIONS list was not found"
    assert set(versions) == {
        "1.12.2", "1.16.5", "1.20.1", "1.20.4",
        "1.21.1", "1.21.4", "1.21.11"
    }


def test_launcher_has_expected_application_name():
    tree = ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))
    app_name = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "APP_NAME"
                   for target in node.targets):
                app_name = ast.literal_eval(node.value)
                break

    assert app_name == "ReallyVisuals"
'''
with open(os.path.join(base,'tests','test_launcher.py'),'w',encoding='utf-8') as f: f.write(test_code)
# README append clarification
rp=os.path.join(base,'README.txt')
with open(rp,encoding='utf-8') as f: readme=f.read()
readme += '''
ПРОВЕРКА PYTEST:
В проект добавлена папка tests с тремя простыми проверками:
- синтаксис Python-файла;
- наличие всех 7 выбранных версий;
- название приложения.
Это устраняет ошибку pytest "no tests ran" (exit code 5), если workflow запускает pytest.
'''
with open(rp,'w',encoding='utf-8') as f: f.write(readme)
# verify tests using local python (pytest may be installed)
import subprocess, sys
r=subprocess.run([sys.executable,'-m','pytest','-q',os.path.join(base,'tests')],capture_output=True,text=True)
print("pytest exit:",r.returncode, r.stdout, r.stderr[-1000:])
