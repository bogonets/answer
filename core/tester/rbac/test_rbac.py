# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.rbac.rbac import Rbac
from recc.rbac.rbac_exception import RbacMismatchContextError


class RbacTestCase(TestCase):
    def test_basic_scenario(self):
        rbac = Rbac()

        # Permissions
        view = rbac.create_permission("view")
        edit = rbac.create_permission("edit")

        # Roles
        admin = rbac.create_role("admin")
        guest = rbac.create_role("guest")

        # Role to Permission
        admin.allow_permission(edit, view)
        guest.allow_permission(view)

        # Users
        user1 = rbac.create_subject("user1")
        user2 = rbac.create_subject("user2")
        user3 = rbac.create_subject("user3")

        # Groups
        group1 = rbac.create_domain("group1")

        # Projects
        project1 = group1.create_subdomain("project1")
        project2 = group1.create_subdomain("project2")

        # Group members
        group1.add_subject(user1, admin)
        group1.add_subject(user2, guest)
        self.assertTrue(group1.has_permission(user1, view))
        self.assertTrue(group1.has_permission(user1, edit))
        self.assertTrue(group1.has_permission(user2, view))
        self.assertFalse(group1.has_permission(user2, edit))
        self.assertFalse(group1.has_permission(user3, view))
        self.assertFalse(group1.has_permission(user3, edit))

        # Project members
        project1.add_subject(user1, guest)
        project1.add_subject(user2, admin)
        self.assertTrue(project1.has_permission(user1, view))
        self.assertFalse(project1.has_permission(user1, edit))
        self.assertTrue(project1.has_permission(user2, view))
        self.assertTrue(project1.has_permission(user2, edit))
        self.assertFalse(project1.has_permission(user3, view))
        self.assertFalse(project1.has_permission(user3, edit))

        project2.add_subject(user3, guest)
        self.assertTrue(project2.has_permission(user1, view))
        self.assertTrue(project2.has_permission(user1, edit))
        self.assertTrue(project2.has_permission(user2, view))
        self.assertFalse(project2.has_permission(user2, edit))
        self.assertTrue(project2.has_permission(user3, view))
        self.assertFalse(project2.has_permission(user3, edit))

        self.assertFalse(project2.has_permission(user1, view, inherit=False))
        self.assertFalse(project2.has_permission(user1, edit, inherit=False))
        self.assertFalse(project2.has_permission(user2, view, inherit=False))
        self.assertFalse(project2.has_permission(user2, edit, inherit=False))
        self.assertTrue(project2.has_permission(user3, view, inherit=False))
        self.assertFalse(project2.has_permission(user3, edit, inherit=False))

    def test_context_mismatch(self):
        rbac1 = Rbac()
        view1 = rbac1.create_permission("view")
        role1 = rbac1.create_role("role")

        rbac2 = Rbac()
        view2 = rbac2.create_permission("view")
        role2 = rbac2.create_role("role")

        with self.assertRaises(RbacMismatchContextError):
            role2.allow_permission(view1)
        with self.assertRaises(RbacMismatchContextError):
            role1.allow_permission(view2)


if __name__ == "__main__":
    main()
