from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


if Base.metadata.create_all(engine):
    print("database created")


from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def print_tasks(rows):
    for ind, row in enumerate(rows):
        print("{0}. {1}. {2}".format(str(ind + 1), row.task, row.deadline.strftime("%-d %b")))
    print()

inp = 10
while inp != 0:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    print(">", end=" ")
    inp = int(input())
    if inp == 0:
        print("Bye")
        break
    elif inp == 1:
        print("Today: " + str(datetime.today().strftime("%d %b")) + ":")
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if rows:
            print_tasks(rows)
        else:
            print("Nothing to do!")
            print()

    elif inp == 2:
        today = datetime.today()
        week = today + timedelta(days=7)
        for day in range(7):
            update = today + timedelta(day)
            print(str(update.date().strftime("%A %-d %b")) + ":")
            rows = session.query(Table).filter(Table.deadline == update.date()).all()
            if rows:
                print_tasks(rows)
            else:
                print("Nothing to do!")
                print()
    elif inp == 4:
        print("Missed tasks:")
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        if rows:
            print_tasks(rows)
        else:
            print("Nothing is missed!")
            print()
    elif inp == 3:
        print("All tasks:")
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            print_tasks(rows)
        else:
            print("Nothing to do!")
            print()

    elif inp == 5:
        print("Enter task")
        print('>', end=" ")
        text = input()
        date = input()
        deadline = datetime.strptime(date, "%Y-%m-%d")
        task = Table(task=text, deadline=deadline)
        session.add(task)
        session.commit()
        print("The task has been added!")
        print()

    elif inp == 6:
        print("Choose the number of the task you want to delete:")
        print('>', end=" ")
        today = datetime.today()
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            print_tasks(rows)
        taskn = int(input()) - 1
        session.delete(rows[taskn])
        session.commit()
        print("The task has been added!")
        print()
    else:
        break


