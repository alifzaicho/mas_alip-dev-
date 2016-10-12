# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import unittest

import responses

from linebot import (
    LineBotApi
)
from linebot.models import (
    VideoSendMessage
)


class TestLineBotApi(unittest.TestCase):
    def setUp(self):
        self.tested = LineBotApi('channel_secret')

        self.video_message = VideoSendMessage(
            original_content_url='https://example.com/original.mp4',
            preview_image_url='https://example.com/preview.jpg'
        )

        self.message = [{
            "type": "video",
            "originalContentUrl": "https://example.com/original.mp4",
            "previewImageUrl": "https://example.com/preview.jpg",
        }]

    @responses.activate
    def test_push_video_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push',
            json={}, status=200
        )

        self.tested.push_message('to', self.video_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push'
        )
        self.assertEqual(
            json.loads(request.body),
            {
                "to": "to",
                "messages": self.message
            }
        )

    @responses.activate
    def test_reply_video_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.video_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply'
        )
        self.assertEqual(
            json.loads(request.body),
            {
                "replyToken": "replyToken",
                "messages": self.message
            }
        )

if __name__ == '__main__':
    unittest.main()
