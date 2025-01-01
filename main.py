import asyncio
import edge_tts
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.markdown import Markdown
from rich.style import Style
from rich.table import Table
from rich.box import SQUARE
from rich.columns import Columns
from typing import Dict

console = Console()

# Информация о программе
PROGRAM_NAME = "🎙 VoiceForge Pro"
PROGRAM_VERSION = "1.0.0"
PROGRAM_DESCRIPTION = """[bold cyan]VoiceForge Pro[/] - профессиональный генератор речи

[bold yellow]О программе:[/]
Современный инструмент для создания естественной речи на основе нейросетей Microsoft Edge TTS.
Идеально подходит для создания аудиокниг, подкастов, обучающих материалов и многого другого.

[bold green]🌟 Ключевые особенности:[/]
• Высококачественный синтез речи
• Два профессиональных голоса
• Готовые пресеты для разных задач
• Точная настройка параметров
• Умная обработка текста

[bold magenta]📋 Доступные пресеты:[/]

[bold]1. 🎙 Профессиональный диктор[/]
   ├─ Для: презентаций, рекламы, анонсов
   ├─ Особенности: чёткая речь, авторитетное звучание
   └─ Настройки: средний темп, оптимальная громкость

[bold]2. 📚 Аудиокнига[/]
   ├─ Для: художественной литературы
   ├─ Особенности: приятный тембр, естественные паузы
   └─ Настройки: комфортный темп, сбалансированный звук

[bold]3. 🎓 Обучающий материал[/]
   ├─ Для: уроков, лекций, инструкций
   ├─ Особенности: чёткое произношение
   └─ Настройки: медленный темп, повышенная чёткость

[bold]4. 📰 Новостной диктор[/]
   ├─ Для: новостей, обзоров, отчётов
   ├─ Особенности: профессиональное звучание
   └─ Настройки: оптимальная скорость и чёткость

[bold]5. 🗣 Разговорный стиль[/]
   ├─ Для: диалогов, блогов, подкастов
   ├─ Особенности: живая речь, естественные интонации
   └─ Настройки: динамичный темп, живое звучание

[bold]6. 📖 Художественное чтение[/]
   ├─ Для: поэзии, художественных текстов
   ├─ Особенности: выразительное чтение
   └─ Настройки: размеренный темп, эмоциональность

[bold yellow]💡 Как использовать:[/]
1. Подготовьте текст в файле text.txt
2. Выберите подходящий голос
3. Выберите пресет для вашей задачи
4. Дождитесь завершения генерации

[bold red]⚠️ Важно:[/] Убедитесь, что файл text.txt находится в той же папке, что и программа.
"""

# Базовые настройки пресетов
BASE_PRESETS = {
    "🎙 Профессиональный диктор": {
        "rate": "-3%",      # Слегка замедленный темп для четкости
        "volume": "+2%",    # Умеренная громкость для избежания искажений
        "pitch": "-1Hz",    # Минимальное понижение тона для естественности
    },
    "📚 Аудиокнига": {
        "rate": "-5%",      # Комфортный темп для восприятия
        "volume": "+0%",    # Стандартная громкость
        "pitch": "+0Hz",    # Естественный тон
    },
    "🎓 Обучающий материал": {
        "rate": "-10%",     # Медленный темп для лучшего понимания
        "volume": "+3%",    # Слегка повышенная громкость для четкости
        "pitch": "-2Hz",    # Легкое понижение для авторитетности
    },
    "📰 Новостной диктор": {
        "rate": "+0%",      # Стандартный темп
        "volume": "+4%",    # Оптимальная громкость для новостей
        "pitch": "-2Hz",    # Профессиональное звучание
    },
    "🗣 Разговорный стиль": {
        "rate": "+2%",      # Естественный темп речи
        "volume": "+1%",    # Легкое усиление для четкости
        "pitch": "+0Hz",    # Естественный тон
    },
    "📖 Художественное чтение": {
        "rate": "-7%",      # Размеренный темп для выразительности
        "volume": "+2%",    # Оптимальная громкость
        "pitch": "-1Hz",    # Легкое понижение для глубины
    }
}

# Голоса для разных полов
VOICES = {
    "Мужской": "ru-RU-DmitryNeural",
    "Женский": "ru-RU-SvetlanaNeural"
}

def get_preset_settings(preset_name: str, voice: str) -> Dict:
    """Получение настроек пресета с учетом выбранного голоса"""
    settings = BASE_PRESETS[preset_name].copy()
    settings["voice"] = voice
    return settings

async def show_help():
    """Показать справку о программе"""
    # Очищаем экран перед выводом справки
    console.clear()
    
    # Основная информация
    console.print(Panel.fit(
        f"[bold cyan]{PROGRAM_NAME}[/] - профессиональный генератор речи",
        border_style="cyan",
        padding=(1, 2)
    ))

    console.print()  # Отступ

    # О программе и ключевые особенности в одной строке
    left_panel = Panel.fit(
        "[bold yellow]О программе[/]\n\n" +
        "Современный инструмент для создания естественной речи на основе\n" +
        "нейросетей Microsoft Edge TTS. Идеально подходит для создания\n" +
        "аудиокниг, подкастов, обучающих материалов и многого другого.",
        border_style="yellow",
        width=50,
        padding=(1, 2)
    )

    right_panel = Panel.fit(
        "• Высококачественный синтез речи\n" +
        "• Два профессиональных голоса\n" +
        "• Готовые пресеты для разных задач\n" +
        "• Точная настройка параметров\n" +
        "• Умная обработка текста",
        title="[bold green]🌟 Ключевые особенности[/]",
        border_style="green",
        width=50,
        padding=(1, 2)
    )

    # Выводим панели в одну строку
    console.print(Columns([left_panel, right_panel]))
    
    console.print()  # Отступ

    # Создаем таблицу пресетов
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="magenta",
        title="[bold magenta]📋 Доступные пресеты[/]",
        padding=(0, 1),
        expand=True,
        show_lines=True,
        box=SQUARE,
        row_styles=["none", "dim"]
    )
    
    table.add_column("Пресет", style="cyan", no_wrap=True, justify="left")
    table.add_column("Применение", style="green", justify="left")
    table.add_column("Особенности", style="yellow", justify="left")
    table.add_column("Настройки", style="blue", justify="left")

    # Добавляем данные в таблицу с улучшенным форматированием
    table.add_row(
        "🎙 Профессиональный\n   диктор",
        "Презентации, реклама,\nанонсы",
        "Чёткая речь,\nавторитетное звучание",
        "Средний темп,\nоптимальная громкость"
    )
    table.add_row(
        "📚 Аудиокнига",
        "Художественная\nлитература",
        "Приятный тембр,\nестественные паузы",
        "Комфортный темп,\nсбалансированный звук"
    )
    table.add_row(
        "🎓 Обучающий\n   материал",
        "Уроки, лекции,\nинструкции",
        "Чёткое\nпроизношение",
        "Медленный темп,\nповышенная чёткость"
    )
    table.add_row(
        "📰 Новостной\n   диктор",
        "Новости, обзоры,\nотчёты",
        "Профессиональное\nзвучание",
        "Оптимальная скорость\nи чёткость"
    )
    table.add_row(
        "🗣 Разговорный\n   стиль",
        "Диалоги, блоги,\nподкасты",
        "Живая речь,\nестественные интонации",
        "Динамичный темп,\nживое звучание"
    )
    table.add_row(
        "📖 Художественное\n   чтение",
        "Поэзия,\nхудожественные тексты",
        "Выразительное\nчтение",
        "Размеренный темп,\nэмоциональность"
    )

    console.print(table)
    
    console.print()  # Отступ

    # Инструкция и важное примечание в одной строке
    left_panel = Panel.fit(
        "1. Подготовьте текст в файле text.txt\n" +
        "2. Убедитесь, что файл text.txt находится\n" +
        "в той же папке, что и программа.\n" +
        "3. Выберите подходящий голос\n" +
        "4. Выберите пресет для вашей задачи\n" +
        "5. Дождитесь завершения генерации",
        title="[bold yellow]💡 Как использовать[/]",
        border_style="yellow",
        width=50,
        padding=(1, 2),
        box=SQUARE
    )
    
    # Выводим панель с инструкциями
    console.print(left_panel)
    
    console.print()  # Отступ

    # Ожидание ввода
    await questionary.text(
        "Нажмите Enter для продолжения...",
        style=questionary.Style([
            ('question', 'fg:teal'),
            ('pointer', 'fg:teal bold')
        ])
    ).ask_async()

async def text_to_speech():
    # Показываем приветствие
    console.print(Panel.fit(
        f"[bold blue]{PROGRAM_NAME} v{PROGRAM_VERSION}[/]\n" +
        "[cyan]Нейронный генератор речи с продвинутыми настройками[/]",
        border_style="blue"
    ))
    
    # Показываем меню
    action = await questionary.select(
        "Выберите действие:",
        choices=[
            "🎙 Начать генерацию",
            "❔ Справка",
            "❌ Выход"
        ],
        style=questionary.Style([
            ('answer', 'fg:teal'),
            ('selected', 'fg:teal bg:gray'),
            ('pointer', 'fg:teal bold'),
            ('highlighted', 'fg:teal')
        ])
    ).ask_async()
    
    if action == "❌ Выход":
        return
    elif action == "❔ Справка":
        await show_help()
        await text_to_speech()
        return
    
    # Выбор пола диктора
    gender = await questionary.select(
        "Выберите голос диктора:",
        choices=list(VOICES.keys()),
        style=questionary.Style([
            ('answer', 'fg:blue'),
            ('selected', 'fg:blue bg:gray'),
            ('pointer', 'fg:blue bold'),
            ('highlighted', 'fg:blue')
        ])
    ).ask_async()
    
    # Выбор пресета
    preset_name = await questionary.select(
        "Выберите стиль речи:",
        choices=list(BASE_PRESETS.keys()),
        style=questionary.Style([
            ('answer', 'fg:teal'),
            ('selected', 'fg:teal bg:gray'),
            ('pointer', 'fg:teal bold'),
            ('highlighted', 'fg:teal')
        ])
    ).ask_async()
    
    # Получаем настройки с учетом выбранного голоса
    settings = get_preset_settings(preset_name, VOICES[gender])
    
    # Чтение текста из файла
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            
        # Предварительная обработка текста для улучшения качества
        text = text.replace('...', '… ').replace('..', '…')
        text = text.replace('!?', '?!').replace('?.', '?')
        text = text.strip()
        
        if not text:
            raise ValueError("Файл text.txt пуст!")
            
    except FileNotFoundError:
        console.print("[red]Ошибка: Файл text.txt не найден![/]")
        return
    except Exception as e:
        console.print(f"[red]Ошибка при чтении файла: {str(e)}[/]")
        return
    
    # Создание объекта для синтеза речи с выбранными настройками
    tts = edge_tts.Communicate(
        text=text,
        **settings
    )
    
    # Показываем прогресс генерации
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as progress:
        # Создаем задачу для прогресс-бара
        task = progress.add_task("[cyan]Генерация речи...", total=100)
        
        try:
            # Сохранение аудио файла
            output_file = "output_speech.mp3"
            
            # Запускаем генерацию и обновление прогресса параллельно
            async def update_progress():
                current = 0
                while current < 95:
                    await asyncio.sleep(0.1)
                    current += 1
                    progress.update(task, completed=current)
            
            # Запускаем генерацию и обновление прогресса параллельно
            await asyncio.gather(
                tts.save(output_file),
                update_progress()
            )
            
            # Завершаем прогресс
            progress.update(task, completed=100)
            
        except Exception as e:
            console.print(f"[red]Ошибка при генерации аудио: {str(e)}[/]")
            return
    
    # Выводим информацию о примененных настройках
    console.print(Panel.fit(
        f"[bold green]✨ Аудио файл успешно создан: {output_file}[/]\n\n"
        f"[cyan]Примененные настройки:[/]\n"
        f"- Голос: {gender}\n"
        f"- Стиль: {preset_name}\n"
        f"- Скорость речи: {settings['rate']}\n"
        f"- Уровень громкости: {settings['volume']}\n"
        f"- Тональность: {settings['pitch']}",
        title="🎉 Генерация завершена 🎉",
        border_style="green"
    ))

if __name__ == '__main__':
    try:
        asyncio.run(text_to_speech())
    except KeyboardInterrupt:
        console.print("\n[red]❌ Генерация прервана пользователем[/]")
    except Exception as e:
        console.print(f"\n[red]❌ Ошибка: {str(e)}[/]") 