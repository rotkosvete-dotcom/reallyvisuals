REALLYVISUALS LAUNCHER — GitHub build for Windows 11

ТЕБЕ НЕ НУЖНО УСТАНАВЛИВАТЬ PYTHON ИЛИ ДРУГИЕ ПРОГРАММЫ НА ПК.

Как получить готовый EXE через сайт GitHub:
1. Открой github.com и войди в аккаунт (или создай аккаунт).
2. Нажми New repository, назови его ReallyVisualsLauncher.
3. Выбери Public или Private и нажми Create repository.
4. Нажми "uploading an existing file" и загрузи ВСЕ файлы и папки из этого архива.
   Важно: папка .github тоже нужна. Если сайт не показывает её, создай папки .github/workflows и добавь туда build.yml.
5. Нажми Commit changes.
6. Открой вкладку Actions, выбери "Build ReallyVisuals Launcher" и нажми Run workflow.
7. Когда сборка закончится зелёной галочкой, открой запуск сборки и скачай artifact
   ReallyVisualsLauncher-Windows. Внутри будет ReallyVisualsLauncher.exe.

Для создания GitHub Release:
- В репозитории открой Releases -> Create a new release.
- Создай тег v1.0.0 и опубликуй. Workflow автоматически прикрепит EXE к релизу.

Поддерживаемые версии в меню:
1.12.2, 1.16.5, 1.20.1, 1.20.4, 1.21.1, 1.21.4, 1.21.11.
Fabric ставится для выбранных поддерживаемых версий; 1.12.2 — Vanilla.

Важно про мод:
Загруженный reallyvisuals-1.0.0.jar — Fabric-мод только для Minecraft 1.16.5.
Для остальных версий требуются отдельные совместимые версии ReallyVisuals.
Профили в текущей версии — локальные офлайн-ники, Microsoft OAuth не реализован.
Для первой загрузки игры нужен интернет.
Minecraft использует стандартную папку %APPDATA%\.minecraft.

Безопасность:
GitHub Actions собирает EXE на серверах GitHub. Скачивай файл только из своего репозитория.
Windows SmartScreen может показать предупреждение для нового неподписанного EXE.
