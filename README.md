# 親分

_— the extreme path_

A library for building Telegram apps.

![shimizu no jirocho](https://github.com/tgrx/oyabun/raw/main/docs/img/shimizu_no_jirocho.jpg)

![build status](https://github.com/tgrx/oyabun/actions/workflows/development.yaml/badge.svg?branch=main)

## Mission

The mission of this library is to provide a strict interface for the API.
By *strict* we mean that all types and methods in the library interface
are mapped to those described in the Telegram API docs.

You won't meet any auxiliary stuff like sophisticated OOP/async patterns,
obscure event loops and listeners and that like kind of stuff.

API types are Pydantic models with strict type hints.

API methods accept params with exactly the same type and name as described in API.

Any optional field/param is marked as `Optional` or `None | T`. Don't be afraid of tri-state bool types.
