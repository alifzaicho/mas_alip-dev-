# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import responses
import unittest

from line_bot import (
    LineBotApi, TemplateSendMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
    ConfirmTemplate, CarouselTemplate, CarouselColumn
)


class TestLineBotApi(unittest.TestCase):
    def setUp(self):
        self.tested = LineBotApi('channel_secret')

        self.button_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu', text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback', text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message', text='message text'
                    ),
                    URITemplateAction(
                        label='uri', uri='http://example.com/'
                    )
                ]
            )
        )

        self.button_message = [{
            "type": "template",
            "altText": "Buttons template",
            "template": {
                "type": "buttons",
                "thumbnailImageUrl":
                    "https://example.com/image.jpg",
                "title": "Menu",
                "text": "Please select",
                "actions": [
                    {
                        "type": "postback",
                        "label": "postback",
                        "text": "postback text",
                        "data": "action=buy&itemid=1"
                    },
                    {
                        "type": "message",
                        "label": "message",
                        "text": "message text"
                    },
                    {
                        "type": "uri",
                        "label": "uri",
                        "uri": "http://example.com/"
                    }
                ]
            }
        }]

        self.confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Are you sure?',
                actions=[
                    PostbackTemplateAction(
                        label='postback', text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message', text='message text'
                    )
                ]
            )
        )

        self.confirm_message = [{
            "type": "template",
            "altText": "Confirm template",
            "template": {
                "type": "confirm",
                "text": "Are you sure?",
                "actions": [
                    {
                        "type": "postback",
                        "label": "postback",
                        "text": "postback text",
                        "data": "action=buy&itemid=1"
                    },
                    {
                        "type": "message",
                        "label": "message",
                        "text": "message text"
                    }
                ]
            }
        }]

        self.carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://example.com'
                                            '/item1.jpg',
                        title='this is menu1', text='description1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1', text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1', text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com'
                                            '/item2.jpg',
                        title='this is menu2', text='description2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2', text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='message2', text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='http://example.com/2'
                            )
                        ]
                    )
                ]
            )
        )

        self.carousel_message = [{
            "type": "template",
            "altText": "Carousel template",
            "template": {
                "type": "carousel",
                "columns": [
                    {
                        "thumbnailImageUrl":
                            "https://example.com/item1.jpg",
                        "title": "this is menu1",
                        "text": "description1",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "postback1",
                                "text": "postback text1",
                                "data": "action=buy&itemid=1"
                            },
                            {
                                "type": "message",
                                "label": "message1",
                                "text": "message text1"
                            },
                            {
                                "type": "uri",
                                "label": "uri1",
                                "uri": "http://example.com/1"
                            }
                        ]
                    },
                    {
                        "thumbnailImageUrl":
                            "https://example.com/item2.jpg",
                        "title": "this is menu2",
                        "text": "description2",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "postback2",
                                "text": "postback text2",
                                "data": "action=buy&itemid=2"
                            },
                            {
                                "type": "message",
                                "label": "message2",
                                "text": "message text2"
                            },
                            {
                                "type": "uri",
                                "label": "uri2",
                                "uri": "http://example.com/2"
                            }
                        ]
                    }
                ]
            }
        }]

    @responses.activate
    def test_push_buttons_template_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push',
            body='{}', status=200
        )

        self.tested.push_message('to', self.button_template_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push'
        )
        self.assertEqual(
            json.loads(request.body.decode("utf-8")),
            {
                "to": "to",
                "messages": self.button_message
            }
        )

    @responses.activate
    def test_reply_buttons_template_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            body='{}', status=200
        )

        self.tested.reply_message('replyToken', self.button_template_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply'
        )
        self.assertEqual(
            json.loads(request.body.decode("utf-8")),
            {
                "replyToken": "replyToken",
                "messages": self.button_message
            }
        )

    @responses.activate
    def test_push_confirm_template_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push',
            body='{}', status=200
        )

        self.tested.push_message('to', self.confirm_template_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push'
        )
        self.assertEqual(
            json.loads(request.body.decode("utf-8")),
            {
                "to": "to",
                "messages": self.confirm_message
            }
        )

    @responses.activate
    def test_reply_confirm_template_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            body='{}', status=200
        )

        self.tested.reply_message('replyToken', self.confirm_template_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply'
        )
        self.assertEqual(
            json.loads(request.body.decode("utf-8")),
            {
                "replyToken": "replyToken",
                "messages": self.confirm_message
            }
        )

    @responses.activate
    def test_push_carousel_template_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push',
            body='{}', status=200
        )

        self.tested.push_message('to', self.carousel_template_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/push'
        )
        self.assertEqual(
            json.loads(request.body.decode("utf-8")),
            {
                "to": "to",
                "messages": self.carousel_message
            }
        )

    @responses.activate
    def test_reply_carousel_template_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            body='{}', status=200
        )

        self.tested.reply_message('replyToken', self.carousel_template_message)

        request = responses.calls[0].request
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply'
        )
        self.assertEqual(
            json.loads(request.body.decode("utf-8")),
            {
                "replyToken": "replyToken",
                "messages": self.carousel_message
            }
        )
