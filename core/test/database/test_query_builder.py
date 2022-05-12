# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.database.query_builder import UpdateBuilder


class UpdateBuilderTestCase(TestCase):
    def test_build(self):
        email = "test@localhost"
        index = 100
        name = "tester"
        extra = 40
        table_name = "users"
        expected_set = f"UPDATE {table_name} SET email=$1,index=$2,phone2=NULL"
        expected_where = " WHERE name LIKE $3 OR category IS NULL AND extra >= $4;"
        expected_query = expected_set + expected_where

        builder = UpdateBuilder(email=email, index=index, phone2=None)
        w = builder.where()
        w.a.like(name=name)
        w.o.eq(category=None)
        w.a.ge(extra=extra)
        query, args = builder.build(table_name)

        self.assertEqual(expected_query, query)
        self.assertEqual(4, len(args))
        self.assertEqual(email, args[0])
        self.assertEqual(index, args[1])
        self.assertEqual(name, args[2])
        self.assertEqual(extra, args[3])


if __name__ == "__main__":
    main()
