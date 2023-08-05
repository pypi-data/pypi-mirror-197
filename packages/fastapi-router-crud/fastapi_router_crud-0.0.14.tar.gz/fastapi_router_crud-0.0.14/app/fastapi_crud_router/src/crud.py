import asyncio
from inspect import (
    iscoroutinefunction,
    iscoroutine,
    isawaitable
)
from fastapi import APIRouter
from typing import List
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from .exceptions.model import CrudRouterConfigError


class CRUD(APIRouter):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        meta = getattr(self, 'Meta', None)
        if not meta:
            return

        database = getattr(meta, 'database', None)

        if not database:
            return

        if iscoroutinefunction(database) or \
                iscoroutine(database) or isawaitable(database):
            # try:
            #     loop = asyncio.get_running_loop()
            # except RuntimeError:
            #     loop = asyncio.new_event_loop()
            #     asyncio.set_event_loop(loop)

            # loop.run_until_complete(database())
            asyncio.run(database())
        else:
            database()

        model = getattr(meta, 'model', None)
        model_name = f"/{model.__mro__[0].__name__}"
        path = getattr(meta, 'path', model_name)
        all_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        methods = getattr(meta, 'methods', [])
        dependencies = getattr(meta, 'dependencies', [])
        queryset = model.all()

        if not model or not queryset:
            raise CrudRouterConfigError(
                "model and queryset are required."
            )

        if not path.startswith("/"):
            raise CrudRouterConfigError(
                "path must start with a forward slash."
            )

        if not issubclass(model, Model):
            raise CrudRouterConfigError(
                f"{model} not subclass of {Model}."
            )

        if path.endswith("/"):
            path = f"{path.rstrip('/')}/"

        route_model = pydantic_model_creator(
            cls=model,
            name=f"{model_name}Model",
        )

        route_model_in = pydantic_model_creator(
            model,
            name=f"{model_name}ModelIn",
            exclude_readonly=True
        )

        for method in methods or all_methods:
            method = method.upper()
            if method not in all_methods:
                raise CrudRouterConfigError(
                    f"Invalid method {method}."
                )

            if method == "GET":
                async def get_all():
                    return await route_model.from_queryset(
                        queryset=queryset.all()
                    )

                async def get_one(id: int):
                    return await route_model.from_queryset_single(
                        queryset=queryset.get(id=id)
                    )

                self.add_api_route(
                    path=path,
                    endpoint=get_all,
                    methods=[method],
                    response_model=List[route_model],
                    status_code=200,
                    summary="Get all items.",
                    description="Get all items.",
                    dependencies=dependencies
                )
                self.add_api_route(
                    path=path + "{id}/",
                    endpoint=get_one,
                    methods=[method],
                    response_model=route_model,
                    status_code=200,
                    summary="Get one item.",
                    description="Get one item.",
                    dependencies=dependencies
                )

            elif method == "POST":
                async def post_one(item: route_model_in):
                    return await route_model.from_tortoise_orm(
                        await model.create(
                            **item.dict(exclude_unset=True)
                        )
                    )

                self.add_api_route(
                    path=path,
                    endpoint=post_one,
                    methods=[method],
                    response_model=route_model,
                    status_code=201,
                    summary="Create one item.",
                    description="Create one item.",
                    dependencies=dependencies
                )

            elif method == "PUT":
                async def put_one(id: int, item: route_model_in):
                    await model.filter(id=id).update(
                        **item.dict(exclude_unset=True)
                    )
                    return await route_model.from_queryset_single(
                        model.get(id=id)
                    )

                self.add_api_route(
                    path=path + "{id}/",
                    endpoint=put_one,
                    methods=[method],
                    response_model=route_model,
                    status_code=200,
                    summary="Update one item.",
                    description="Update one item.",
                    dependencies=dependencies
                )

            # elif method == "PATCH":
            #     async def patch_one(id: int, item: route_model_in):
            #         await model.filter(id=id).update(
            #             **item.dict(exclude_unset=True)
            #         )
            #         return await route_model.from_queryset_single(
            #             model.get(id=id)
            #         )

            #     self.add_api_route(
            #         path=path + "{id}/",
            #         endpoint=patch_one,
            #         methods=[method],
            #         response_model=route_model,
            #         status_code=200,
            #         summary="Update one item.",
            #         description="Update one item.",
            #         dependencies=dependencies
            #     )

            elif method == "DELETE":
                async def delete_one(id: int):
                    return await model.filter(id=id).delete()

                self.add_api_route(
                    path=path + "{id}/",
                    endpoint=delete_one,
                    methods=[method],
                    status_code=204,
                    summary="Delete one item.",
                    description="Delete one item.",
                    dependencies=dependencies
                )
