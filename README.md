# PCController ⚡ Peak Performance Edition

Ультрабыстрый движок автоматизации, компьютерного зрения и аппаратного восприятия Windows для ИИ-ассистентов (Claude, Antigravity, Cursor, Cline и локальных LLM).

---

## 🚀 Архитектурные преимущества и замеры скорости

| Подсистема | Технология | Время отклика | Описание |
| :--- | :--- | :--- | :--- |
| **Мышь (Перемещение)** | Win32 `SetCursorPos` | **0.02 мс** | Мгновенное позиционирование без искусственных задержек |
| **Мышь (Клик)** | Win32 `mouse_event` | **0.05 мс** | Прямой клик в ядро Windows |
| **Клавиатура** | Batch `SendInput` (Unicode) | **~5–8 мс** на фразу | Ввод всей строки за один вызов ядра, полная поддержка русского языка |
| **Скриншот экрана** | MSS + OpenCV C++ JPEG | **~35–40 мс** | Нулевое копирование памяти, размер 1080p ~120 КБ |
| **Vision для мультимодальных ИИ** | In-Memory JPEG Stream | **~35 мс** | Возврат нативного `Image` в MCP без записи на диск |
| **Компьютерное зрение** | OpenCV `matchTemplate` | **~90 мс** | Поиск иконки/кнопки на экране и клик по координатам |
| **Управление окнами** | Win32 `ShowWindow` + Alt-Trick | **~1–2 мс** | Обход защиты от перехвата фокуса Windows |
| **Умное ожидание** | `wait_for_window` | Реактивно (50 мс) | Исключает слепые `time.sleep()`, ускоряя сценарии до 10 раз |

---

## 🛠️ Набор инструментов MCP-сервера (25 Tools)

### 1. Системный статус
- `get_system_info`: Срез состояния ПК (разрешение, координаты мыши, активное окно, число окон).
- `get_screen_size`: Разрешение основного монитора.

### 2. Зрение и Скриншоты
- `take_screenshot`: Сверхбыстрый скриншот в файл (JPEG/PNG, настройка качества и масштаба).
- `capture_screen_vision`: Нативный мультимодальный блок `Image` прямо в контекст ИИ.
- `find_image_on_screen`: Поиск шаблона (кнопки, иконки) на экране через OpenCV.
- `click_image`: Поиск шаблона и моментальный клик по нему в одно действие.

### 3. Мышь
- `get_mouse_position`: Координаты курсора в реальном времени.
- `mouse_move`: Перемещение курсора.
- `mouse_click`: Клик любой кнопкой (left/right/middle, двойной клик).
- `mouse_drag`: Перетаскивание объектов.
- `mouse_scroll`: Прокрутка колесиком мыши.

### 4. Клавиатура и Буфер обмена
- `keyboard_type`: Мгновенный ввод Unicode-текста любой длины.
- `keyboard_press`: Нажатие одиночной клавиши (`enter`, `esc`, `tab`, `win` и др.).
- `keyboard_hotkey`: Горячие клавиши (`ctrl+c`, `alt+tab` и др.) с гарантированным сбросом модификаторов.
- `clipboard_get` / `clipboard_set`: Чтение и запись в буфер обмена.

### 5. Окна и Процессы
- `list_windows`: Список всех видимых окон с их координатами.
- `get_active_window`: Данные активного окна в фокусе.
- `focus_window`: Активация и развертывание окна (`maximize=True/False`).
- `minimize_window`: Сворачивание окна.
- `close_window`: Корректное закрытие окна (`WM_CLOSE`).
- `wait_for_window`: Умное ожидание появления окна по ключевому слову.
- `launch_app`: Запуск любой программы Windows с опциональным ожиданием ее окна.

### 6. Аппаратное восприятие
- `capture_webcam`: Снимок с веб-камеры с прогревом матрицы.
- `record_mic`: Запись звука с микрофона с расчетом пиковой амплитуды и детекцией голоса.

---

## 🧪 Запуск единого теста и бенчмарка

```powershell
.venv\Scripts\python.exe benchmark.py
```

---

## 🔌 Подключение к ИИ-клиентам

### Вариант 1: stdio (Claude Desktop, Cursor, Cline, Antigravity)
```powershell
.venv\Scripts\python.exe server.py
```

Конфигурация в `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "pc-controller": {
      "command": "C:\\Users\\nz809\\PycharmProjects\\PCController\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\nz809\\PycharmProjects\\PCController\\server.py"
      ]
    }
  }
}
```

### Вариант 2: HTTP SSE (порт 8000)
```powershell
.venv\Scripts\python.exe server.py --transport sse --port 8000
```
