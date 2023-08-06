"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 02.02.2023 19:06
"""
import json

import aiohttp

from ..common import USER_AGENT
from ..common.model.ReelAuthor import ReelAuthor
from ..common.model.ReelModel import ReelModel
from ..common.model.ReelPreview import ReelPreview
from ..common.model.ReelVideo import ReelVideo


class MediaInfo:

    def __init__(
            self,
            session_id: str,
            instagram_app_id_header: str = "936619743392459"
    ):
        self.__headers = {
            "x-ig-app-id": instagram_app_id_header,
            "user-agent": USER_AGENT,
            "cookie": f"sessionid={session_id};"
        }

    async def get(self, media_id: int) -> ReelModel | None:
        async with aiohttp.ClientSession(headers=self.__headers) as session:
            async with session.get(f"https://www.instagram.com/api/v1/media/{media_id}/info/") as response:
                if response.status == 200 and response.content_type == "application/json":
                    return self.parse(await response.text())
                else:
                    return None

    @staticmethod
    def parse(raw_json: str) -> ReelModel | None:
        parsed: dict = json.loads(raw_json)
        media_info_list: list | None = parsed.get("items", None)
        if media_info_list is not None and len(media_info_list) > 0:
            media_info: dict = media_info_list[0]
            reel_caption = media_info["caption"]
            reel_author_user = media_info["user"]
            reel_previews: list = media_info["image_versions2"]["candidates"]
            reel_videos: list = media_info["video_versions"]
            return ReelModel(
                media_id=media_info["pk"],
                code=media_info["code"],
                description=reel_caption["text"] if reel_caption is not None else "",
                duration=float(media_info.get("video_duration", 0)),
                like_count=int(media_info.get("like_count", 0)),
                view_count=int(media_info.get("view_count", 0)),
                play_count=int(media_info.get("play_count", 0)),
                author=ReelAuthor(
                    user_id=reel_author_user["pk"],
                    username=reel_author_user["username"],
                    full_name=reel_author_user.get("full_name", ""),
                    profile_pic_url=reel_author_user.get("profile_pic_url", "")
                ),
                previews=[ReelPreview(
                    width=int(preview["width"]),
                    height=int(preview["height"]),
                    url=preview["url"]
                ) for preview in reel_previews],
                videos=[ReelVideo(
                    video_id=video["id"],
                    width=int(video["width"]),
                    height=int(video["height"]),
                    url=video["url"]
                ) for video in reel_videos]
            )
        else:
            return None
