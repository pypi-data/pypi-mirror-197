#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.queries import SBoQueries


class Requires:
    """ Creates a list of dependencies with
    the right order to install. """

    def __init__(self, name: str):
        self.name: str = name

    def resolve(self) -> list:
        """ Resolve the dependencies. """
        requires: list[str] = SBoQueries(self.name).requires()  # type: ignore
        for req in requires:
            if req:
                sub: list[str] = SBoQueries(req).requires()  # type: ignore
                for s in sub:
                    requires.append(s)

        requires.reverse()

        return list(dict.fromkeys(requires))
