import queue

st = queue.LifoQueue()

st.put("tigre")
st.put("Hola")
st.put(22)
st.put("Datos")

while not st.empty():
    value = st.get()
    print(value)

