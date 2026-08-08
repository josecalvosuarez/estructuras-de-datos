import queue

q = queue.Queue()

q.put("Hola Tigre")
q.put(22)
q.put("Jueves")
q.put("Datos")

while not q.empty():
    value = q.get()
    print(value)


