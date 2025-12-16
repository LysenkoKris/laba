import redis

client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def check_connection() -> None:
    try:
        client.ping()
        print("Успешное подключение к Redis")
    except redis.ConnectionError:
        print("Ошибка подключения к Redis")


def strings_example() -> None:
    print("\n Строки")
    client.set("user:name", "Иван")
    name = client.get("user:name")
    print("Имя:", name)

    client.setex("session:123", 3600, "active")
    print("TTL для session:123:", client.ttl("session:123"))


def numbers_example() -> None:
    print("\n Числа")
    client.set("counter", 0)
    client.incr("counter")
    client.incrby("counter", 5)
    client.decr("counter")
    print("counter =", client.get("counter"))


def lists_example() -> None:
    print("\n Списки")
    client.delete("tasks")
    client.lpush("tasks", "task1", "task2")
    client.rpush("tasks", "task3", "task4")
    tasks = client.lrange("tasks", 0, -1)
    print("Все задачи:", tasks)
    first = client.lpop("tasks")
    last = client.rpop("tasks")
    print("Первый:", first, "Последний:", last)
    print("Длина списка:", client.llen("tasks"))


def sets_example() -> None:
    print("\n Множества")
    client.delete("tags", "languages")
    client.sadd("tags", "python", "redis", "database")
    client.sadd("languages", "python", "java", "javascript")
    print("tags:", client.smembers("tags"))
    print("Пересечение:", client.sinter("tags", "languages"))
    print("Объединение:", client.sunion("tags", "languages"))
    print("Разность:", client.sdiff("tags", "languages"))


def hashes_example() -> None:
    print("\n Хэши")
    client.hset(
        "user:1000",
        mapping={"name": "Иван", "age": "30", "city": "Москва"},
    )
    print("Имя:", client.hget("user:1000", "name"))
    print("Все поля:", client.hgetall("user:1000"))
    print("Существует email?:", client.hexists("user:1000", "email"))


def sorted_sets_example() -> None:
    print("\n Отсортированные множества")
    client.delete("leaderboard")
    client.zadd("leaderboard", {"player1": 100, "player2": 200, "player3": 150})
    print(
        "По рангу:",
        client.zrange("leaderboard", 0, -1, withscores=True),
    )
    print(
        "По счёту 100..200:",
        client.zrangebyscore("leaderboard", 100, 200, withscores=True),
    )
    print("Ранг player1:", client.zrank("leaderboard", "player1"))


if __name__ == "__main__":
    check_connection()
    strings_example()
    numbers_example()
    lists_example()
    sets_example()
    hashes_example()
    sorted_sets_example()
