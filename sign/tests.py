#-*- coding: utf-8 -*-
from django.test import TestCase
import unittest
# Create your tests here.
import os,django

from django.test import Client


class VerifiedSignFuction(TestCase):
    def setUp(self):
        self.c=Client()

    def verifiedMobileEmpty(self):
        response = self.c.post('/sign_index_action/1/',{"phone":""})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"phone error.",response.content)



