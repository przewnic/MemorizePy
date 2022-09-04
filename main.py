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
    if not rows:
        print("There is no flashcard to practice!")
        return

    for row in rows:
        print(f"Question: {row.question}")
        print(
            'press "y" to see the answer:',
            'press "n" to skip:',
            'press "u" to update:',
            sep="\n"
        )
        pressed = input()
        if pressed == "n":
            continue
        elif pressed == "y":
            print(f"Answer: {row.answer}")
            update_leitner(row, session)
        elif pressed == "u":
            update_flashcard(row, session)
        else:
            print(f"{pressed} is not an option")
    session.commit()


def update_leitner(row, session):
    print(
        'press "y" if your answer is correct:',
        'press "n" if your answer is wrong:',
        sep="\n"
    )
    pressed = input()
    if pressed == "y":
        if row.box_number == 3:
            delete_flashcard(row, session)
        else:
            row.box_number = row.box_number + 1 if row.box_number < 3 else 3
    elif pressed == "n":
        row.box_number = row.box_number - 1 if row.box_number > 1 else 1
    else:
        print(f"{pressed} is not an option")


def update_flashcard(row, session):
    """ User advances to update menu from practice """
    print(
        'press "d" to delete the flashcard:',
        'press "e" to edit the flashcard:',
        sep="\n"
    )
    pressed = input()
    print()
    if pressed == "d":
        delete_flashcard(row, session)
    elif pressed == "e":
        edit_flashcard(row)
    else:
        print(f"{pressed} is not an option")


def edit_flashcard(row):
    print(f"current question: {row.question}")
    print("please write a new question:")
    new_q = input()
    print(f"current answer: {row.answer}")
    print("please write a new answer:")
    new_a = input()
    row.question = new_q
    row.answer = new_a


def delete_flashcard(row, session):
    session.delete(row)


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
