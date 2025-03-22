import subprocess
import os
import polib
from deep_translator import GoogleTranslator
from babel.messages import Catalog
from babel.messages.pofile import write_po

# test app template start 
test_template="""
import gettext
import os
import argparse

# Lokalizatsiya fayllari joylashuvi
LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locales')

# Tilni o'rnatish funksiyasi
def set_locale(language_code):
    try:
        # gettext-ni tanlangan tilga sozlash
        lang = gettext.translation('messages', localedir=LOCALES_DIR, languages=[language_code])
        lang.install()  # gettextni o'rnatish
        _ = lang.gettext  # gettext (gettextni qisqacha belgilash)
        return _  # Bu "gettext" funksiyasini qaytaradi
    except FileNotFoundError:
        print(f"{language_code} tilidagi tarjima fayli topilmadi.")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
    return None

# Konsool interfeysi uchun argumentlar
def main():
    parser = argparse.ArgumentParser(description="CLI i18n Dasturi")
    parser.add_argument('--lang', type=str, help='Tarjima tilini kiriting (masalan: uz, ru, en)', required=True)
    parser.add_argument('--run', action='store_true', help='Tarjima matnini ko\'rsatish')

    args = parser.parse_args()

    # Tilni o'rnatish
    _ = set_locale(args.lang)

    # Tarjima matnini chiqarish
    if args.run:
        if _:
            print(_("Salom Dasturimga hush kelibsiz.!"))
            print(_("Sizga qanday yordam bera olaman"))
            print(_("Mening yaratuvchim: Otaboyev Sardorbek Davronbek o`g`li"))
        else:
            print("Tilni o'rnatishda xatolik yuz berdi!")

if __name__ == '__main__':
    main()

# ishlatish bo`yicha yo`riq noma
# python app.py --lang uz --run

"""

def test_template_cheks(file_path):
    # Fayl mavjudligini tekshirib ko'rish
    if not os.path.exists(file_path):
        # Agar fayl mavjud bo'lmasa, yangi fayl yaratish
        with open(file_path, 'w') as file:
            file.write(babel_config)
        print(f"Teplate yaratildi: {file_path}")
    else:
        print(f"Teplate  mavjud: {file_path}")
        # Faylni o'qish va ma'lumot mavjudligini tekshirish
        with open(file_path, 'r') as file:
            content = file.read()
            # Agar faylda hech qanday ma'lumot bo'lmasa, uni yangilash
            if not content.strip():
                print(f"{file_path} Faylda ma'lumot yo'q, yangilanmoqda...")
                with open(file_path, 'w') as file:
                    file.write(babel_config)
                print(f"Teplate yangilandi: {file_path}")
            else:
                print(f"Teplateda ma'lumot mavjud: {file_path}")

test_template_cheks(file_path='app.py')

# test app template end

# beble settings start 
babel_config="""[python:*.py]
extensions = ["gettext"] 
"""

def babel_config_check(file_path):
    # Fayl mavjudligini tekshirib ko'rish
    if not os.path.exists(file_path):
        # Agar fayl mavjud bo'lmasa, yangi fayl yaratish
        with open(file_path, 'w') as file:
            file.write(babel_config)
        print(f"Fayl yaratildi: {file_path}")
    else:
        print(f"Fayl mavjud: {file_path}")
        # Faylni o'qish va ma'lumot mavjudligini tekshirish
        with open(file_path, 'r') as file:
            content = file.read()
            # Agar faylda hech qanday ma'lumot bo'lmasa, uni yangilash
            if not content.strip():
                print("babel.cfg Faylda ma'lumot yo'q, yangilanmoqda...")
                with open(file_path, 'w') as file:
                    file.write(babel_config)
                print(f"Fayl yangilandi: {file_path}")
            else:
                print("Faylda ma'lumot mavjud: babel.cfg")

babel_config_check(file_path='babel.cfg')
# beble settings end
# BabelCommand - buyruqlarni bajarish uchun
class BabelCommand:
    def __init__(self, command: str, description: str):
        self.command = command
        self.description = description
    
    def execute(self):
        try:
            # Buyruqni bajarish
            print(f"Buyruq bajarilmoqda: {self.command}")
            subprocess.run(self.command, shell=True, check=True)
            print(f"Buyruq muvaffaqiyatli bajarildi: {self.description}")
        except subprocess.CalledProcessError as e:
            print(f"Xatolik yuz berdi: {e}")
        except Exception as e:
            print(f"Xatolik: {e}")

# BabelApp - Babel buyruqlari va algoritmlarini bajarish
class BabelApp:
    def __init__(self):
        self.commands = [
            BabelCommand("pybabel extract -F babel.cfg -o locales/messages.pot .", "Dasturdagi matnlarni .pot fayliga chiqaradi."),
            BabelCommand("pybabel update -i locales/messages.pot -d locales", "Tarjimalarni yangilaydi."),
            BabelCommand("pybabel compile -d locales", ".po fayllarini .mo formatiga kompyilyatsiya qiladi.")
        ]
    
    def run_init_command(self, lang_code):
        # Foydalanuvchi kiritgan til qisqartmasi uchun pybabel init buyruqni yaratamiz
        command = f"pybabel init -i locales/messages.pot -d locales -l {lang_code}"
        description = f"Yangi til ({lang_code}) uchun tarjima faylini yaratadi."
        init_command = BabelCommand(command, description)
        init_command.execute()

    def po_to_mo(self, lang_code):
        # Foydalanuvchi kiritgan til qisqartmasi uchun pybabel init buyruqni yaratamiz
        cammand=f'msgfmt locales/{lang_code}/LC_MESSAGES/messages.po -o locales/{lang_code}/LC_MESSAGES/messages.mo'
        description='po fayilini mo fayiliga o`zgartirish.(yangi usuli)'
        init_command = BabelCommand(cammand, description)
        init_command.execute()

    def show_commands(self):
        print("Buyruqlar ro'yxati:")
        for idx, cmd in enumerate(self.commands, 1):
            print(f"{idx}. {cmd.description}")
    
    def run_algorithm(self):
        # Buyruqlarni ketma-ket bajarish
        print("Algoritm boshlanmoqda...")
        for cmd in self.commands:
            cmd.execute()
        
        print("Algoritm tugadi.")

    def run_specific_command(self, command_id):
        try:
            selected_command = self.commands[command_id - 1]
            selected_command.execute()
        except IndexError:
            print("Noto'g'ri buyruq ID.")
        
# Tarjima uchun asosiy bo'lim (i18n)
catalog = Catalog()
locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

if not os.path.exists(locales_dir):
    os.makedirs(locales_dir)
    print("locales papkasi yaratildi.!")

def beble_i18n_any():
    try:
        catalog_data = []
        while True:
            print("Dasturni to`xtatish va ma`lumotlarni saqlash uchun: os buyrug`ini kiriting.!")
            data = str(input(f"Kalit so`zni kiriting: "))
            if not data:
                continue
            if data == 'os':
                print(" ")
                break
            catalog_data.append(data)
        for text in catalog_data:
            catalog.add(text, '')
    except Exception:
        print("Xato aniqlandi.!")
    except(KeyboardInterrupt):
        print("\n")
        print("Dastur to`xtatildi.!")

def po_generate():
    try:
        info = 'locales/messages.pot'
        with open(os.path.join(locales_dir, 'messages.pot'), 'wb') as pot_file:
            write_po(pot_file, catalog)
            print(f"Template yaratildi: {info}")
            print(end="\n")
            
    except(KeyboardInterrupt):
        print("\n")
        print("Dasturni to`xtatdingiz.!")
    except Exception as error:
        print(f"xato aniqlandi: {error}")

def babel_any_funk():
    try:
        beble_i18n_any()
        po_generate()
    except(KeyboardInterrupt):
        print("Dasturni to`xtatildi.!")
    except Exception:
        print("Xato aniqlandi")
# Tarjima bo'limi
class TranslatorApp:
    def __init__(self, target_language: str):
        self.target_language = target_language  # Tarjimaga o'zgartirmoqchi bo'lgan til
        self.translator = GoogleTranslator(source="auto", target=self.target_language)

    def translate_text(self, text: str) -> str:
        """Berilgan matnni tarjima qilish"""
        if not text:
            return "Ma'lumot parametrlari noto'g'ri"
        return self.translator.translate(text=text)

    def read_po_file(self, file_path: str):
        """.po faylini o'qish"""
        try:
            po_file = polib.pofile(file_path)
            return po_file
        except Exception as e:
            print(f"Xatolik: {e}")
            return None

    def translate_po_file(self, po_file):
        """Po faylini tarjima qilish"""
        for entry in po_file:
            if entry.msgid:  # msgid bo'lsa, tarjima qilamiz
                entry.msgstr = self.translate_text(entry.msgid)
        return po_file

    def save_po_file(self, po_file, output_file_path: str):
        """Tarjima qilingan .po faylini saqlash"""
        try:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  # Direktoriyalarni yaratamiz
            po_file.save(output_file_path)
            print(f"Fayl muvaffaqiyatli saqlandi: {output_file_path}")
        except Exception as e:
            print(f"Xatolik: {e}")

    def process_translation(self, input_po_file: str, output_po_file: str):
        """Po faylini tarjima qilish va saqlash jarayonini bajarish"""
        po_file = self.read_po_file(input_po_file)
        if po_file:
            translated_po_file = self.translate_po_file(po_file)
            self.save_po_file(translated_po_file, output_po_file)

def TranslatorApp_init():
    target_language = str(input("Tarjima tilini kiriting: ")) # Tarjimaga o'zgartirmoqchi bo'lgan til
    if not target_language:
        return "Hato aniqlandi.!"
    output_po_file = f'locales/{target_language}/LC_MESSAGES/messages.po' 
    translator_app = TranslatorApp(target_language)  # Dastur obyekti yaratamiz
    translator_app.process_translation('locales/messages.pot', output_po_file)

# Asosiy main funksiyasi
def main():
    # Babel buyruqlari
    app = BabelApp()
    
    while True:
        try:
            print("\nBabel Buyruqlari va Algoritmlar:")
            app.show_commands()
            
            print("\nMaxsus algoritmni ishga tushurish uchun 'a' ni bosing.")
            print("\nMaxsus qo`lda kiritish algaritimi 'any' ni bosing.")
            print("\nMaxsus algoritmni tarjimon uchun 'tra' ni bosing.")
            print("\nMaxsus algoritmni po file to mo file 'moto' ni bosing.")
            print("\nYoki, ma'lum bir buyruqni bajarish uchun ID ni tanlang (1-4).")
            print("\nYangi tilni yaratish uchun til qisqartmasini kiriting.(masalan: uz,ru,en)")
            print("\nDasturdan chiqish uchun 'exit' ni yozing.")
            
            choice = input("Tanlovni kiriting: ").strip()
            
            if choice == 'exit':
                print("Dasturdan chiqyapman...")
                break
            elif choice =='any':
                babel_any_funk()
            elif choice =='tra':
                TranslatorApp_init()
            elif choice =='moto':
                lang_code=str(input("Tilni kiriting masalan:(uz,ru,en): "))
                if not lang_code:
                    continue
                app.po_to_mo(lang_code=lang_code)
            elif choice == 'a':
                app.run_algorithm()
            elif choice.isdigit():
                app.run_specific_command(int(choice))
            elif len(choice) == 2 and choice.isalpha():  # 2 ta harfli til qisqartmasi
                app.run_init_command(choice)
            else:
                print("Noto'g'ri tanlov, iltimos, qayta urinib ko'ring.")
        except(KeyboardInterrupt) as devstop:
            print(end='\n')
            print("Dastur to`xtatildi.!")
            break

if __name__ == "__main__":
    main()
