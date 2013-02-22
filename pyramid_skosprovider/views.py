# -*- coding: utf8 -*-

from pyramid_skosprovider import get_skos_registry

from pyramid.view import view_config, view_defaults

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
)


class RestView(object):

    def __init__(self, request):
        self.request = request
        self.skos_registry = get_skos_registry(self.request)

@view_defaults(renderer='json', accept='application/json')
class ProviderView(RestView):

    @view_config(route_name='skosprovider.conceptschemes', request_method='GET')
    def get_conceptschemes(self):
        return [{'id': p.get_vocabulary_id()} for p in self.skos_registry.get_providers()]

    @view_config(route_name='skosprovider.conceptscheme', request_method='GET')
    def get_conceptscheme(self):
        scheme_id = self.request.matchdict['scheme_id']
        provider = self.skos_registry.get_provider(scheme_id)
        if not provider:
            return HTTPNotFound()
        return {'id': provider.get_vocabulary_id()}

    @view_config(route_name='skosprovider.conceptscheme.concepts', request_method='GET')
    def get_conceptscheme_concepts(self):
        scheme_id = self.request.matchdict['scheme_id']
        provider = self.skos_registry.get_provider(scheme_id)
        if not provider:
            return HTTPNotFound()
        return provider.get_all()

    @view_config(route_name='skosprovider.concept', request_method='GET')
    def get_concept(self):
        scheme_id = self.request.matchdict['scheme_id']
        concept_id = self.request.matchdict['concept_id']
        regis = get_skos_registry(self.request)
        provider = self.skos_registry.get_provider(scheme_id)
        return provider.get_by_id(concept_id)
