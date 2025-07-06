from typing import Annotated
from fastapi import APIRouter, File, Form, UploadFile
from pydantic import Base64Encoder


from ...models import *
from ...shared.services.routers.utils import *
from ...shared.services.storage import upload_file
from ...shared.services.servers.utils import *
from ..notifications.api_models import NotificationType, broadcastNotification
from .api_models import *


posts_router = APIRouter(prefix="/posts", tags=["Posts and Comments"])


@posts_router.get(
    "/user/{user_id}",
    name="Get posts of the a user.",
    responses={
        HTTP_200_OK: {
            "model": PostsResponse,
            "description": "Posts returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def posts(
    user_id: str,
    page: int = 1,
    limit: int = 10,
    session: Session = get_session,
) -> PostsResponse:
    if page < 1:
        page = 1
    pages = Posts.count_pages(
        limit,
        dict(user_id=user_id),
    )
    posts: list[Post] = Posts.find(
        dict(user_id=user_id),
        limit=limit,
        skip=(page - 1) * limit,
        sort="created_timestamp",
        descending=True,
    )
    # Collect all user_ids needed (authors, likers, commenters)
    user_ids = set()
    for post in posts:
        user_ids.add(post.user_id)
        user_ids.update(post.likes)
        for comment_id in post.comments_ids:
            comment = Comments.get_child(comment_id)
            if comment:
                user_ids.add(comment.user_id)

    users = {u.id: u for u in Users.find({"id": {"$in": list(user_ids)}})}

    def user_info(user_id):
        user = users.get(user_id)
        if user:
            return dict(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                user_name=user.user_name,
                email=user.email,
            )
        return None

    post_models = []
    for post in posts:
        # Likes users
        likes_users = [user_info(uid) for uid in post.likes if user_info(uid)]
        # Comments with user info
        comments = []
        for comment_id in post.comments_ids:
            comment = Comments.get_child(comment_id)
            if comment:
                commenter = user_info(comment.user_id)
                comments.append(dict(
                    id=comment.id,
                    content=comment.content,
                    user=commenter,
                    created_timestamp=comment.created_timestamp,
                    files=comment.files,
                ))
        post_models.append(dict(
            content=post.content,
            id=post.id,
            created_timestamp=post.created_timestamp,
            author=user_info(post.user_id),
            likes=likes_users,
            comments=comments,
            files=post.files,
        ))
    return dict(
        detail="Posts returned successfully.",
        pages=pages,
        page=page,
        posts=post_models,
    )


@posts_router.get(
    "/",
    name="Get all posts",
    responses={
        HTTP_200_OK: {
            "model": PostsResponse,
            "description": "Posts returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def posts(
    page: int = 1,
    limit: int = 10,
    session: Session = get_session,
) -> PostsResponse:
    if page < 1:
        page = 1
    pages = Posts.count_pages(limit)
    posts: list[Post] = Posts.find(
        limit=limit,
        skip=(page - 1) * limit,
        sort="created_timestamp",
        descending=True,
    )
    # Collect all user_ids needed (authors, likers, commenters)
    user_ids = set()
    for post in posts:
        user_ids.add(post.user_id)
        user_ids.update(post.likes)
        for comment_id in post.comments_ids:
            comment = Comments.get_child(comment_id)
            if comment:
                user_ids.add(comment.user_id)

    users = {u.id: u for u in Users.find({"id": {"$in": list(user_ids)}})}

    def user_info(user_id):
        user = users.get(user_id)
        if user:
            return dict(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                user_name=user.user_name,
                email=user.email,
            )
        return None

    post_models = []
    for post in posts:
        # Likes users
        likes_users = [user_info(uid) for uid in post.likes if user_info(uid)]
        # Comments with user info
        comments = []
        for comment_id in post.comments_ids:
            comment = Comments.get_child(comment_id)
            if comment:
                commenter = user_info(comment.user_id)
                comments.append(dict(
                    id=comment.id,
                    content=comment.content,
                    user=commenter,
                    created_timestamp=comment.created_timestamp,
                    files=comment.files,
                ))
        post_models.append(dict(
            content=post.content,
            id=post.id,
            created_timestamp=post.created_timestamp,
            author=user_info(post.user_id),
            likes=likes_users,
            comments=comments,
            files=post.files,
        ))
    return dict(
        detail="Posts returned successfully.",
        pages=pages,
        page=page,
        posts=post_models,
    )


@posts_router.get(
    "/{post_id}",
    name="Get post detail",
    responses={
        HTTP_200_OK: {
            "model": PostResponse,
            "description": "Post returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def post(
    post_id: str,
    session: Session = get_session,
) -> PostResponse:
    post: Post
    if post := Posts.get_child(post_id):
        # Gather all user info
        author = Users.get_child(post.user_id)
        author_info = dict(
            id=author.id,
            first_name=author.first_name,
            last_name=author.last_name,
            user_name=author.user_name,
            email=author.email,
        ) if author else None
        likes_users = [Users.get_child(uid) for uid in post.likes]
        likes_users = [dict(
            id=u.id,
            first_name=u.first_name,
            last_name=u.last_name,
            user_name=u.user_name,
            email=u.email,
        ) for u in likes_users if u]
        comments = []
        for comment_id in post.comments_ids:
            comment = Comments.get_child(comment_id)
            if comment:
                commenter = Users.get_child(comment.user_id)
                commenter_info = dict(
                    id=commenter.id,
                    first_name=commenter.first_name,
                    last_name=commenter.last_name,
                    user_name=commenter.user_name,
                    email=commenter.email,
                ) if commenter else None
                comments.append(dict(
                    id=comment.id,
                    content=comment.content,
                    user=commenter_info,
                    created_timestamp=comment.created_timestamp,
                    files=comment.files,
                ))
        return dict(
            detail="Posts returned successfully.",
            post=dict(
                content=post.content,
                id=post.id,
                author=author_info,
                likes=likes_users,
                created_timestamp=post.created_timestamp,
                comments=comments,
                files=post.files,
            ),
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid post id.",
        )


@posts_router.post(
    "/{post_id}/comment",
    name="Comment on a post",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Post commented on successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def comment(
    post_id: str,
    content: Annotated[str, Form()] = "",
    gifs: list[Annotated[str, Form()]] = [],
    files: list[Annotated[UploadFile | str, File()]] = [],
    session: Session = get_session,
) -> Response:
    post: Post = Posts.get_child(post_id)
    if post:
        files_paths = []
        files += gifs

        for file in files:
            if not isinstance(file, str):
                file = upload_file(
                    file.filename,
                    await file.read(),
                )
            files_paths.append(file)

        comment = Comments.create(
            post_id=post_id,
            user_id=session.user.id,
            content=content,
            files=files_paths,
        )
        post.comments_ids.append(comment.id)
        post.save()

        notification = Notifications.create(
            user_id=post.user_id,
            uid=post.id,
            uid2=comment.id,
            type=NotificationType.comment,
            username=session.user.user_name,
        )

        await broadcastNotification(notification)

        return dict(detail="Post commented on successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid post id")


@sio_server.event
async def comment(sid: str, data: dict):
    if not (post_id := data.get("post_id")):
        return

    post: Post = Posts.get_child(post_id)
    if not post:
        return

    content = data.get("content") or []
    gifs = data.get("gifs") or []
    files = data.get("files") or []
    files_paths = []
    files += gifs

    if not (isinstance(files, list) and isinstance(gifs, list)):
        return

    if not (session := await get_ws_session(sid)):
        return

    try:
        for file in files:
            if (
                isinstance(file, dict)
                and (filename := file.get("filename"))
                and (data_ := file.get("data"))
            ):
                file = upload_file(
                    filename,
                    Base64Encoder.decode(data_.encode()),
                )
            files_paths.append(file)

        comment = Comments.create(
            post_id=post_id,
            user_id=session.user.id,
            content=content,
            files=files_paths,
        )
        post.comments_ids.append(comment.id)
        post.save()

        notification = Notifications.create(
            user_id=post.user_id,
            uid=post.id,
            uid2=comment.id,
            type=NotificationType.comment,
            username=session.user.user_name,
        )

        await broadcastNotification(notification)
        await sio_server.emit("comment", comment.dict)

    except:
        ...


@posts_router.get(
    "/{post_id}/comments",
    name="Comments of a post",
    responses={
        HTTP_200_OK: {
            "model": CommentsResponse,
            "description": "Comment of a post returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def comments(
    post_id: str,
    page: int = 1,
    limit: int = 0,
    _: Session = get_session,
) -> CommentsResponse:
    if page < 1:
        page = 1
    post: Post = Posts.get_child(post_id)
    if post:
        pages = Comments.count_pages(
            limit,
            dict(post_id=post_id),
        )
        comments: list[Comment] = Comments.find(
            dict(post_id=post_id),
            limit=limit,
            skip=(page - 1) * limit,
            sort="created_timestamp",
            descending=True,
        )
        comments_models: list[CommentModel] = []
        for c in comments:
            commenter: User = Users.get_child(c.user_id)
            comments_models.append(
                CommentModel(
                    post_id=c.post_id,
                    content=c.content,
                    id=c.id,
                    user_id=c.user_id,
                    created_timestamp=c.created_timestamp,
                    user_name=f"{commenter.first_name} {commenter.last_name}",
                    files=c.files,
                )
            )

        return CommentsResponse(
            detail="Comment of a post returned successfully.",
            comments=comments_models,
            pages=pages,
            page=page,
        )
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid post id")


@posts_router.post(
    "/{post_id}/like",
    name="Like a post",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Post liked successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def like(
    post_id: str,
    session: Session = get_session,
) -> Response:
    post: Post = Posts.get_child(post_id)
    if post:
        if session.user.id not in post.likes:
            post.likes.append(session.user.id)
            post.save()

            notification = Notifications.create(
                user_id=post.user_id,
                uid=session.user.id,
                uid2=post.id,
                type=NotificationType.like,
                username=session.user.user_name,
            )

            await broadcastNotification(notification)

        return dict(detail="Post liked successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid post id")


@sio_server.event
async def like(sid: str, post_id: str):
    post: Post = Posts.get_child(post_id)
    if not post:
        return

    if not (session := await get_ws_session(sid)):
        return

    if session.user.id not in post.likes:
        post.likes.append(session.user.id)
        post.save()

        notification = Notifications.create(
            user_id=post.user_id,
            uid=session.user.id,
            uid2=post.id,
            type=NotificationType.like,
            username=session.user.user_name,
        )

        await broadcastNotification(notification)


@posts_router.post(
    "/{post_id}/unlike",
    name="Unlike a post",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Post unliked successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def unlike(
    post_id: str,
    session: Session = get_session,
) -> Response:
    post: Post = Posts.get_child(post_id)
    if post:
        if session.user.id in post.likes:
            post.likes.remove(session.user.id)
            post.save()
        return dict(detail="Post unliked successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid post id")


@sio_server.event
async def unlike(sid: str, post_id: str):
    post: Post = Posts.get_child(post_id)
    if not post:
        return

    if not (session := await get_ws_session(sid)):
        return

    if session.user.id in post.likes:
        post.likes.remove(session.user.id)
        post.save()

        # notification = Notifications.create(
        #     user_id=post.user_id,
        #     uid=session.user.id,
        #     uid2=post.id,
        #     type=NotificationType.like,
        #     username=session.user.user_name,
        # )

        # await broadcastNotification(notification)


@posts_router.get(
    "/{post_id}/likes",
    name="Likes of a post",
    responses={
        HTTP_200_OK: {
            "model": LikesResponse,
            "description": "Post likes returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def like(post_id: str, session: Session = get_session) -> LikesResponse:
    post: Post = Posts.get_child(post_id)
    if post:
        return dict(detail="Post likes returned successfully.", likes=post.likes)
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid post id")


@posts_router.post(
    "/",
    name="Add a new post",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Post added successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def post(
    content: Annotated[str, Form()] = "",
    gifs: list[Annotated[UploadFile | str, File()]] = [],
    files: list[Annotated[UploadFile | str, File()]] = [],
    session: Session = get_session,
) -> Response:
    files_paths = []

    files = files + gifs

    for file in files:
        if not isinstance(file, str):
            file = upload_file(
                file.filename,
                await file.read(),
            )
        files_paths.append(file)

    if Posts.create(
        user_id=session.user.id,
        content=content,
        files=files_paths,
    ):
        return dict(detail="Post added successfully.")
    else:
        raise HTTPException(
            HTTP_503_SERVICE_UNAVAILABLE,
            "Database error, htry again later.",
        )


@sio_server.event
async def post(sid: str, data: dict):
    content = data.get("content") or []
    gifs = data.get("gifs") or []
    files = data.get("files") or []
    files_paths = []
    files += gifs

    if not (isinstance(files, list) and isinstance(gifs, list)):
        return

    if not (session := await get_ws_session(sid)):
        return

    try:
        for file in files:
            if (
                isinstance(file, dict)
                and (filename := file.get("filename"))
                and (data_ := file.get("data"))
            ):
                file = upload_file(
                    filename,
                    Base64Encoder.decode(data_.encode()),
                )
            files_paths.append(file)

        post = Posts.create(
            user_id=session.user.id,
            content=content,
            files=files_paths,
        )

        await sio_server.emit("post", post.dict)

    except:
        ...


@posts_router.delete(
    "/{post_id}",
    name="Delete a post",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Post deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid post id.",
        },
        HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Response,
            "description": "Database error, try again later.",
        },
    },
)
async def post(post_id: str, session: Session = get_session) -> Response:
    post: Post = Posts.get_child(post_id)
    if post:
        Posts.delete_child(post._id)
        return Response(detail="Post deleted successfully.")
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Invalid post id")
