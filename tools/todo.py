from datetime import datetime
from typing import List
import argparse
import json
from pathlib import Path

class TodoItem:
    def __init__(self, id: int, title: str, done:bool, created_at:str = None):
        self.id = id
        self.title = title
        self.done = done
        if created_at is None:
            self.created_at = datetime.now().isoformat()
        else:
            self.created_at = created_at

    def to_dict(self) -> dict:
        return \
            {"id": self.id,
             "title": self.title,
             "done": self.done,
             "created_at": self.created_at
            }
    
    @classmethod
    def from_dict(cls, data:dict) -> "TodoItem":
        return cls(data["id"], data["title"], data["done"], data["created_at"])
    

class TodoList:
    def __init__(self, filepath:str):
        self.items = []
        self.filepath = filepath
        self.load()

    def add(self, title:str) -> None:
        if len(self.items) == 0:
            id = 1
        else:
            id = max(item.id for item in self.items) + 1
        
        item = TodoItem(id, title, False)
        self.items.append(item)

        self.save()

    def complete(self, item_id: int) -> None:
        for item in self.items:
            if item.id == item_id:
                item.done = True
                self.save()
                return
            
        print(f"Item ID: {item_id} could not be found")
    
    def delete(self, item_id: int) -> None:
        for item in self.items:
            if item.id == item_id:
                self.items.remove(item)
                self.save()
                return
            
        print(f"Item ID: {item_id} could not be found")

    def list_items(self) -> list:
        return self.items
    
    def save(self):
        ls = []
        for item in self.items:
            ls.append(item.to_dict())
            
        with open(self.filepath, "w") as f:
            json.dump(ls, f)

    def load(self):
        if Path(self.filepath).exists():
            with open(self.filepath, "r") as f:
                records = json.load(f)

            for record in records:
                self.items.append(TodoItem.from_dict(record))

def main():
    parser = argparse.ArgumentParser(description="Todo List")
    subparsers = parser.add_subparsers(dest="command")
    
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title", help="Todo title")

    list_parser = subparsers.add_parser("list", help="List all todos")

    done_parser = subparsers.add_parser("done", help="Complete a todo")
    done_parser.add_argument("id", type=int, help="Todo ID")
    
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="Delete ID")

    args = parser.parse_args()
    
    todo = TodoList("data/todos.json")

    if args.command == "add":
        todo.add(args.title)
    elif args.command == "list":
        items = todo.list_items()
        for item in items:
            print(item.to_dict())

    elif args.command == "done":
        todo.complete(args.id)
    elif args.command == "delete":
        todo.delete(args.id)


if __name__ == "__main__":
    main()