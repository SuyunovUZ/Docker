from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.transactions import atomic
from pydantic import BaseModel
from typing import List
from models import Post

app = FastAPI()

# Tortoise ORM initialization
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


class PostSchema(BaseModel):
    id: int
    title: str
    content: str


@app.post("/posts/", response_model=PostSchema)
async def create_post(post: PostSchema):
    new_post = await Post.create(**post.dict())
    return new_post


@app.get("/posts/{post_id}", response_model=PostSchema, responses={404: {"model": HTTPNotFoundError}})
async def read_post(post_id: int):
    return await Post.filter(id=post_id).first()


@app.put("/posts/{post_id}", response_model=PostSchema, responses={404: {"model": HTTPNotFoundError}})
async def update_post(post_id: int, post: PostSchema):
    await Post.filter(id=post_id).update(**post.dict())
    return await Post.filter(id=post_id).first()


@app.delete("/posts/{post_id}", response_model=dict, responses={404: {"model": HTTPNotFoundError}})
async def delete_post(post_id: int):
    deleted_count = await Post.filter(id=post_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
