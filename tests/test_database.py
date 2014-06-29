import os
import unittest
import random

from seasondog import database
from seasondog import info


class PlainDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_text(self):
        self.assertEqual("a\x00\x00", database.text("a", 3))

    def test_text_raise(self):
        self.assertRaises(RuntimeError, database.text, "abc", 1)

    def test_db_value(self):
        self.assertEqual(
            database.text("/:1:-subs @subs()", database.STRLEN),
            database.db_value("/", 1, "-subs @subs()"))

    def test_check(self):
        self.assertIsNone(database.check(
            "{}:{},{}:{}".format(info.NAME, info.VERSION, database.NAME, database.VERSION)))

        args_all = [info.NAME, info.VERSION, database.NAME, database.VERSION]
        for x in range(2):
            args = args_all.copy()
            args[x+2] = 99
            self.assertRaises(RuntimeError, database.check, "{}:{},{}:{}".format(*args))

    def test_get(self):
        db = database.db_struct("", {"/": {database.EPISODE: 1, database.PLAYER_ARGS: "args"}}, {})
        self.assertEqual(database.get(db, "/"), {database.EPISODE: 1, database.PLAYER_ARGS: "args"})
        self.assertIsNone(database.get(db, "/blah"))

    def test_set(self):
        db = database.db_struct("", {"/": {database.EPISODE: 1, database.PLAYER_ARGS: "args"}}, {})
        database.set(db, "/", {database.EPISODE: 2, database.PLAYER_ARGS: "args"})
        self.assertEqual(database.get(db, "/"), {database.EPISODE: 2, database.PLAYER_ARGS: "args"})

    def test_unset(self):
        db = database.db_struct("", {"/": {database.EPISODE: 1, database.PLAYER_ARGS: "args"}}, {})
        database.unset(db, "/")
        self.assertIsNone(database.get(db, "/"))

    def test_update(self):
        db = database.db_struct("", {"/": {database.EPISODE: 1, database.PLAYER_ARGS: "args"}}, {})
        database.update(db, "/", lambda x, a: {database.EPISODE: a, database.PLAYER_ARGS: "args"}, 2)
        self.assertEqual(database.get(db, "/"), {database.EPISODE: 2, database.PLAYER_ARGS: "args"})

    def test_init(self):
        path = "/tmp/sdog_testdb"
        database.init(database.db_struct(path, {}, {}))
        with open(path, 'r') as f:
            contents = f.read()
        self.assertEqual(
            database.text(
                "{}:{},{}:{}".format(info.NAME, info.VERSION, database.NAME, database.VERSION),
                database.STRLEN)+"\n",
            contents)

    def test_load(self):
        db = database.load("./test_db")
        self.assertEqual(db[database.DB][os.path.abspath(".")][database.EPISODE], 1)
        self.assertEqual(db[database.DB][os.path.abspath(".")][database.PLAYER_ARGS], "-sub @subs()")

    def test_save(self):
        db = database.load("./test_db")
        database.set(
            db,
            "/",
            {database.EPISODE: 2,
                database.PLAYER_ARGS: "args", })

        db[database.PATH] = "/tmp/sdog_testdb"
        database.save(db)

        db = database.load("/tmp/sdog_testdb")
        self.assertEqual(db[database.DB][os.path.abspath("/")][database.EPISODE], 2)
        self.assertEqual(db[database.DB][os.path.abspath("/")][database.PLAYER_ARGS], "args")

    def test_commit(self):
        db = database.load("./test_db")
        database.set(
            db,
            "/",
            {database.EPISODE: 2,
                database.PLAYER_ARGS: "args", })

        database.set(
            db,
            "/home/sp",
            {database.EPISODE: 200,
                database.PLAYER_ARGS: "-audiofile @files()", })

        db[database.PATH] = "/tmp/sdog_testdb"
        database.commit(db)

        db = database.load("/tmp/sdog_testdb")
        self.assertEqual(db[database.DB][os.path.abspath("/")][database.EPISODE], 2)
        self.assertEqual(db[database.DB][os.path.abspath("/")][database.PLAYER_ARGS], "args")

        self.assertEqual(db[database.DB][os.path.abspath("/home/sp")][database.EPISODE], 200)
        self.assertEqual(db[database.DB][os.path.abspath("/home/sp")][database.PLAYER_ARGS], "-audiofile @files()")

    def test_cleanup(self):
        folder = "/I_damn_shure_this_folder_cant_exist_but_if_you_create_it_{}_in_your_face".format(
                random.randint(10000, 90000))
        db = database.load("./test_db")
        database.set(
            db,
            folder,
            {database.EPISODE: 2,
                database.PLAYER_ARGS: "args", })

        db[database.PATH] = "/tmp/sdog_testdb"
        database.save(db)

        db = database.load("/tmp/sdog_testdb")
        database.cleanup(db)

        db = database.load("/tmp/sdog_testdb")
        self.assertIsNone(db[database.DB].get(folder))

    def test_migrate(self):
        db = database.load("./test_db")
        database.set(
            db,
            "/x",
            {database.EPISODE: 2,
                database.PLAYER_ARGS: "args", })

        db[database.PATH] = "/tmp/sdog_testdb"
        database.save(db)
        db = database.load(db[database.PATH])

        database.migrate(db, os.path.abspath("/x"), os.path.expanduser("~"))
        db = database.load(db[database.PATH])

        self.assertIsNotNone(database.get(db, os.path.expanduser("~")))
        self.assertIsNone(database.get(db, os.path.abspath("/x")))

        self.assertRaises(RuntimeError, database.migrate, db, "/blah", "/wah")
