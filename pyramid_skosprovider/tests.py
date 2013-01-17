# -*- coding: utf8 -*-

from pyramid import testing

from pyramid_skosprovider import (
    ISkosRegistry,
    _build_skos_registry,
    get_skos_registry,
    includeme
)

from skosprovider.registry import (
    Registry
)

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestRegistry(object):

    def __init__(self, settings=None):

        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        self.skos_registry = None

    def queryUtility(self, iface):
        return self.skos_registry

    def registerUtility(self, skos_registry, iface):
        self.skos_registry = skos_registry


class TestGetAndBuild(unittest.TestCase):

    def test_get_skos_registry(self):
        r = TestRegistry()
        SR = Registry()
        r.registerUtility(SR, ISkosRegistry)
        SR2 = get_skos_registry(r)
        self.assertEquals(SR, SR2)

    def test_build_skos_registry_already_exists(self):
        r = TestRegistry()
        SR = Registry()
        r.registerUtility(SR, ISkosRegistry)
        SR2 = _build_skos_registry(r)
        self.assertEquals(SR, SR2)

    def test_build_skos_registry_default_settings(self):
        r = TestRegistry()
        SR = _build_skos_registry(r)
        self.assertIsInstance(SR, Registry)