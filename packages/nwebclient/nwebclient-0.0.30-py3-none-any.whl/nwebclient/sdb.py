
import sqlite3
import io

def sdb_write(data, prompt, negativ_prompt, guidance_scale, name='data', dbfile='data.db'):
    nxfiles_sql = """CREATE TABLE IF NOT EXISTS nxfiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        prompt VARCHAR(255),negativ_prompt VARCHAR(255), guidance_scale FLOAT,
        data BLOB)
    """
    try:
        sqliteConnection = sqlite3.connect('data.db')
        cursor = sqliteConnection.cursor()
        cursor.execute(nxfiles_sql)
        sqlite_insert_blob_query = """ INSERT INTO nxfiles
                     (name, prompt, negativ_prompt, guidance_scale, data) VALUES (?, ?, ?, ?, ?)"""
        data_tuple = (name, prompt, negativ_prompt, guidance_scale, data)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Data Stored.")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def sdb_write_pil(img, prompt, negativ_prompt, guidance_scale, name='data', dbfile='data.db'):
    #img = Image.open("p67b2.jpg")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    #img.close()
    sdb_write(img_byte_arr.read(), prompt, negativ_prompt, guidance_scale, name)

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    #print("Stored blob data into: ", filename, "\n")

def sdb_extract(dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT id, name, data from nxfiles"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            id = row[0]
            data = row[2]
            filename = name+"_"+str(id)+".jpg"
            print("Write File: " + filename)
            writeTofile(data, filename)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
