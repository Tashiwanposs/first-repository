import argparse
import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def add_task(text):
    tasks = load_tasks()
    next_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    tasks.append({"id": next_id, "text": text, "done": False})
    save_tasks(tasks)
    print(f"已添加任务 #{next_id}: {text}")


def list_tasks(show_all):
    tasks = load_tasks()
    if not tasks:
        print("当前没有任务。")
        return

    for task in tasks:
        if not show_all and task["done"]:
            continue
        mark = "x" if task["done"] else " "
        print(f"[{mark}] #{task['id']} {task['text']}")


def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"任务 #{task_id} 已完成。")
            return
    print(f"未找到任务 #{task_id}。")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"未找到任务 #{task_id}。")
        return
    save_tasks(new_tasks)
    print(f"任务 #{task_id} 已删除。")


def build_parser():
    parser = argparse.ArgumentParser(description="一个简单的待办清单命令行工具")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="添加任务")
    add_p.add_argument("text", help="任务内容")

    list_p = sub.add_parser("list", help="查看任务")
    list_p.add_argument("--all", action="store_true", help="显示包含已完成任务")

    done_p = sub.add_parser("done", help="标记任务为完成")
    done_p.add_argument("id", type=int, help="任务编号")

    del_p = sub.add_parser("del", help="删除任务")
    del_p.add_argument("id", type=int, help="任务编号")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.text)
    elif args.command == "list":
        list_tasks(args.all)
    elif args.command == "done":
        mark_done(args.id)
    elif args.command == "del":
        delete_task(args.id)


if __name__ == "__main__":
    main()
