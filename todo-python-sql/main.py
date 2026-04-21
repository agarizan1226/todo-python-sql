import sqlite3


DB_NAME = "tasks.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def add_task(title):
    with connect() as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    print("Aufgabe wurde hinzugefuegt.")


def list_tasks():
    with connect() as conn:
        tasks = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()

    if not tasks:
        print("Die Aufgabenliste ist leer.")
        return

    for task_id, title, done in tasks:
        status = "erledigt" if done else "offen"
        print(f"{task_id}. {title} [{status}]")


def complete_task(task_id):
    with connect() as conn:
        cursor = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))

    if cursor.rowcount == 0:
        print("Aufgabe wurde nicht gefunden.")
    else:
        print("Aufgabe wurde als erledigt markiert.")


def delete_task(task_id):
    with connect() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    if cursor.rowcount == 0:
        print("Aufgabe wurde nicht gefunden.")
    else:
        print("Aufgabe wurde geloescht.")


def show_menu():
    print("\nTo-Do List")
    print("1. Aufgaben anzeigen")
    print("2. Aufgabe hinzufuegen")
    print("3. Aufgabe erledigen")
    print("4. Aufgabe loeschen")
    print("0. Beenden")


def main():
    create_table()

    while True:
        show_menu()
        choice = input("Aktion auswaehlen: ").strip()

        if choice == "1":
            list_tasks()
        elif choice == "2":
            title = input("Aufgabe eingeben: ").strip()
            if title:
                add_task(title)
            else:
                print("Die Aufgabe darf nicht leer sein.")
        elif choice == "3":
            task_id = input("Aufgaben-ID eingeben: ").strip()
            if task_id.isdigit():
                complete_task(int(task_id))
            else:
                print("Bitte eine Zahl eingeben.")
        elif choice == "4":
            task_id = input("Aufgaben-ID eingeben: ").strip()
            if task_id.isdigit():
                delete_task(int(task_id))
            else:
                print("Bitte eine Zahl eingeben.")
        elif choice == "0":
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungueltige Auswahl.")


if __name__ == "__main__":
    main()
