# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def gmser_check(id) :
    alr_exist = []
    con = sqlite3.connect(r'파일의 경로 or 파일 이름', isolation_level = None)
    cur = con.cursor()
    cur.execute("SELECT id FROM UserInfo WHERE id = ?", (id,))
    rows = cur.fetchall()
    for i in rows :
        alr_exist.append(i[0])
    if id not in alr_exist :
        return 0
    elif id in alr_exist :
        return 1
    con.close()

print('PyCharm')