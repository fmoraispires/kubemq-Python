# MIT License
#
# Copyright (c) 2018 KubeMQ
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import threading
from kubemq.grpc import SendQueueMessageResult as SendQueueMessageResult
from kubemq.tools.id_generator import get_next_id as get_next_id


class SendMessageResult:
    def __init__(self, send_message_result=None):
        if send_message_result:
            self.message_id = send_message_result.MessageID
            self.expiration_at= send_message_result.ExpirationAt
            self.is_error=send_message_result.IsError
            self.sent_at=send_message_result.SentAt
            self.delayed_to=send_message_result.DelayedTo
            self.error=send_message_result.Error

    def __repr__(self):
        return "<Message message_id:%s expiration_at:%s is_error:%s sent_at:%s delayed_to:%s error:%s>" % (
            self.message_id,
            self.expiration_at,
            self.is_error,
            self.sent_at,
            self.delayed_to,
            self.error,
        )
        

    def convert_to_SendQueueMessageResult(self):
        """Convert a SendMessageResult to an SendQueueMessageResult"""
        return SendQueueMessageResult(
            MessageID=self.message_id or get_next_id(),
            ExpirationAt=self.expiration_at.value or "",
            IsError=self.is_error or "",
            SentAt=self.sent_at,
            DelayedTo=self.delayed_to,
            Error=self.error
        )
       
        

def convert_from_send_queue_message_result(notification):
    """Convert SendQueueMessageResult to SendMessageResult"""
    result = SendMessageResult()
    result.message_id=notification.MessageID
    result.expiration_at=notification.ExpirationAt
    result.is_error=notification.IsError
    result.sent_at=notification.SentAt,
    result.delayed_to=notification.DelayedTo,
    result.error=notification.Error,
    return result