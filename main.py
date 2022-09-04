from flashcard import Flashcard, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def menu():
    menu_list = [
        "Add flashcards",
        "Practice flashcards",
        "Exit"
    ]
    return menu_list


def sub_menu():
    menu_list = [
        "Add a new flashcard",
        "Exit"
    ]
    return menu_list


def add_flashcard(session):
    q = ""
    while not q:
        print("Question:")
        q = input().strip()
    a = ""
    while not a:
        print("Answer:")
        a = input().strip()
    new_data = Flashcard(question=q, answer=a)
    session.add(new_data)
    session.commit()


def practice(session):
    rows = session.query(Flashcard).all()
    for row in rows:
        print(f"Question: {row.question}")
        print('Please press "y" to see the answer or press "n" to skip:')
        pressed = input()
        if pressed == "n":
            continue
        elif pressed == "y":
            print(f"Answer: {row.answer}")
            print()
        else:
            print(f"{pressed} is not an option")


def create_db(engine):
    Base.metadata.create_all(engine)


def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    engine = create_engine("sqlite:///flashcard.db")
    create_db(engine)
    while True:
        for i, item in enumerate(menu(), start=1):
            print(f"{i}. {item}")

        choice = input()
        if choice == "1":
            while True:
                for i, item in enumerate(sub_menu(), start=1):
                    print(f"{i}. {item}")
                sub_choice = input()
                if sub_choice == "1":
                    add_flashcard(create_session(engine))
                elif sub_choice == "2":
                    break
                else:
                    print(f"{sub_choice} is not an option")
        elif choice == "2":
            practice(create_session(engine))
        elif choice == "3":
            print("Bye!")
            break
        else:
            print(f"{choice} is not an option")
