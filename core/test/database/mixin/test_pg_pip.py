# -*- coding: utf-8 -*-

from unittest import main

from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgPipTestCase(PostgresqlTestCase):
    async def test_create_and_select_all(self):
        domain1 = "recc"
        name1 = "aiohttp_cors>=0.7.0"
        file1 = "aiohttp_cors-0.7.0-py3-none-any.whl"
        hash_method1 = "sha256"
        hash_value1 = "9ac0d0b3b485d293b8ca1987e6de8658d7dafcca1cddfcd1d506cae8cdebfdd6"
        await self.db.insert_pip(domain1, name1, file1, hash_method1, hash_value1)
        pips = await self.db.select_pip_all()
        self.assertEqual(1, len(pips))
        pip = pips[0]
        self.assertEqual(domain1, pip.domain)
        self.assertEqual(name1, pip.name)
        self.assertEqual(file1, pip.file)
        self.assertEqual(hash_method1, pip.hash_method)
        self.assertEqual(hash_value1, pip.hash_value)

    async def test_select_and_delete(self):
        domain1 = "domain1"
        domain2 = "domain2"
        name1 = "name1"
        name2 = "name2"
        file1 = "file1"
        file2 = "file2"
        hash_method1 = "method1"
        hash_method2 = "method2"
        hash_value1 = "value1"
        hash_value2 = "value2"
        await self.db.insert_pip(domain1, name1, file1, hash_method1, hash_value1)
        await self.db.insert_pip(domain2, name2, file2, hash_method2, hash_value2)
        pips1 = await self.db.select_pip_by_domain_and_name(domain1, name1)
        pips2 = await self.db.select_pip_by_domain_and_name(domain2, name2)
        self.assertEqual(1, len(pips1))
        self.assertEqual(1, len(pips2))
        pip1 = pips1[0]
        pip2 = pips2[0]

        self.assertEqual(domain1, pip1.domain)
        self.assertEqual(domain2, pip2.domain)
        self.assertEqual(name1, pip1.name)
        self.assertEqual(name2, pip2.name)
        self.assertEqual(file1, pip1.file)
        self.assertEqual(file2, pip2.file)
        self.assertEqual(hash_method1, pip1.hash_method)
        self.assertEqual(hash_method2, pip2.hash_method)
        self.assertEqual(hash_value1, pip1.hash_value)
        self.assertEqual(hash_value2, pip2.hash_value)

        await self.db.delete_pip_by_domain_and_name(domain1, name1)
        await self.db.delete_pip_by_domain_and_name(domain2, name2)
        pips = await self.db.select_pip_all()
        self.assertEqual(0, len(pips))


if __name__ == "__main__":
    main()
