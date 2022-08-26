# -*- coding: utf-8 -*-

from unittest import main

from minio import S3Error

from tester.unittest.minio_test_case import MinioTestCase


class MinioStorageServiceTestCase(MinioTestCase):
    async def test_bucket(self):
        original_buckets = await self.minio.list_buckets()

        self.assertFalse(await self.minio.exists_bucket(self.bucket))
        await self.minio.make_bucket(self.bucket)
        self.assertTrue(await self.minio.exists_bucket(self.bucket))

        updated_buckets = await self.minio.list_buckets()
        self.assertEqual(len(updated_buckets), len(original_buckets) + 1)

        await self.minio.remove_bucket(self.bucket)
        self.assertFalse(await self.minio.exists_bucket(self.bucket))

    async def test_object(self):
        await self.minio.make_bucket(self.bucket)
        objects1 = await self.minio.list_object(self.bucket, "/")
        self.assertEqual(len(objects1), 0)

        object_name = "aaa"
        object_data = b"AAA"
        self.assertFalse(await self.minio.exists_object(self.bucket, object_name))

        await self.minio.put_object(self.bucket, object_name, object_data)
        objects2 = await self.minio.list_object(self.bucket)
        self.assertEqual(len(objects2), 1)
        self.assertEqual(objects2[0], object_name)

        self.assertTrue(await self.minio.exists_object(self.bucket, object_name))
        state = await self.minio.get_state(self.bucket, object_name)
        self.assertEqual(state.bucket, self.bucket)
        self.assertEqual(state.name, object_name)
        self.assertFalse(state.is_dir)

        data = await self.minio.get_object(self.bucket, object_name)
        self.assertEqual(data, object_data)

        await self.minio.remove_object(self.bucket, object_name)
        self.assertFalse(await self.minio.exists_object(self.bucket, object_name))

    async def test_remove_objects(self):
        await self.minio.make_bucket(self.bucket)

        object_name1 = "aaa"
        object_data1 = b"AAA"
        await self.minio.put_object(self.bucket, object_name1, object_data1)

        object_name2 = "bbb"
        object_data2 = b"BBB"
        await self.minio.put_object(self.bucket, object_name2, object_data2)

        objects1 = await self.minio.list_object(self.bucket)
        self.assertEqual(len(objects1), 2)

        await self.minio.remove_objects(self.bucket, [object_name1, object_name2])

        objects2 = await self.minio.list_object(self.bucket)
        self.assertEqual(len(objects2), 0)

        await self.minio.remove_bucket(self.bucket)
        self.assertFalse(await self.minio.exists_bucket(self.bucket))

    async def test_remove_not_empty_bucket(self):
        await self.minio.make_bucket(self.bucket)

        object_name1 = "aaa"
        object_data1 = b"AAA"
        await self.minio.put_object(self.bucket, object_name1, object_data1)

        object_name2 = "bbb"
        object_data2 = b"BBB"
        await self.minio.put_object(self.bucket, object_name2, object_data2)

        objects1 = await self.minio.list_object(self.bucket)
        self.assertEqual(len(objects1), 2)

        with self.assertRaises(S3Error):
            await self.minio.remove_bucket(self.bucket)

        objects2 = await self.minio.list_object(self.bucket)
        self.assertEqual(len(objects2), 2)

        await self.minio.remove_bucket(self.bucket, force=True)
        self.assertFalse(await self.minio.exists_bucket(self.bucket))


if __name__ == "__main__":
    main()
