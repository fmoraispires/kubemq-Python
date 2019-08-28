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
from kubemq.grpc import StreamQueueMessagesRequest
from kubemq.grpc import QueueMessage
from kubemq.queue.stream_request_type import StreamRequestType
from kubemq.tools.id_generator import get_next_id

class TransactionMessagesResponse:
    def __init__(self, stream_queue_messages_response=None,request_id=None,is_error=None,error_message=None,message=None,stream_request=None):
        if stream_queue_messages_response:
            self.request_id = stream_queue_messages_response.RequestID
            """Represents Unique identifier for the Request."""

            self.is_error= stream_queue_messages_response.IsError
            """Returned from KubeMQ, false if no error."""

            self.error=stream_queue_messages_response.Error
            """Error message, valid only if IsError true."""

            self.message=stream_queue_messages_response.Message
            """"The received Message."""
            self.stream_request_type=stream_queue_messages_response.StreamRequestType
            """Request action: ReceiveMessage, AckMessage, RejectMessage, ModifyVisibility, ResendMessage,  SendModifiedMessage, Unknown."""
        else:
            self.message=message
            self.is_error=is_error
            self.error=error_message
            self.request_id=request_id
            self.stream_request_type=stream_request

    def __repr__(self):
        return "<TransactionMessagesResponse request_id:%s is_error:%s error:%s message:%s stream_request_type:%s>" % (
            self.request_id,
            self.is_error,
            self.error,
            self.message,
            self.stream_request_type
        )

def create_stream_queue_message_receive_request(_queue,visibility_seconds,wait_time_seconds=None):
    """Create StreamQueueMessageRequest for receive"""
    return StreamQueueMessagesRequest(
        ClientID=_queue.ClientID,
        Channel=_queue.QueueName,
        RequestID=get_next_id(),
        StreamRequestTypeData=StreamRequestType.ReceiveMessage,
        VisibilitySeconds=visibility_seconds,
        WaitTimeSeconds=wait_time_seconds or _queue.WaitTimeSecondsQueueMessages,
        ModifiedMessage= QueueMessage(),
        RefSequence=0
    )

def create_stream_queue_message_ack_request(_queue,msg_sequence):
    """Create StreamQueueMessageRequest for ack"""
    return StreamQueueMessagesRequest(
        ClientID=_queue.ClientID,
        Channel=_queue.QueueName,
        RequestID=get_next_id(),
        StreamRequestTypeData=StreamRequestType.AckMessage,
        VisibilitySeconds=0,
        WaitTimeSeconds=0,
        ModifiedMessage= None,
        RefSequence=msg_sequence
    )

def create_stream_queue_message_reject_request(_queue,msg_sequence):
    """Create StreamQueueMessageRequest for reject"""
    return StreamQueueMessagesRequest(
        ClientID=_queue.ClientID,
        Channel=_queue.QueueName,
        RequestID=get_next_id(),
        StreamRequestTypeData=StreamRequestType.RejectMessage,
        VisibilitySeconds=0,
        WaitTimeSeconds=0,
        ModifiedMessage= None,
        RefSequence=msg_sequence
    )


def create_stream_queue_message_extend_visibility_request(_queue,visibility):
    """Create StreamQueueMessageRequest for extend_visibility"""
    return StreamQueueMessagesRequest(
        ClientID=_queue.ClientID,
        Channel=_queue.QueueName,
        RequestID=get_next_id(),
        StreamRequestTypeData=StreamRequestType.ModifyVisibility,
        VisibilitySeconds=visibility,
        WaitTimeSeconds=0,
        ModifiedMessage= None,
        RefSequence=0
    )

def create_stream_queue_message_resend_request(_queue,queueName):
    """Create StreamQueueMessageRequest for resend"""
    return StreamQueueMessagesRequest(
        ClientID=_queue.ClientID,
        Channel=queueName,
        RequestID=get_next_id(),
        StreamRequestTypeData=StreamRequestType.ResendMessage,
        VisibilitySeconds=0,
        WaitTimeSeconds=0,
        ModifiedMessage= None,
        RefSequence=0
    )


def create_stream_queue_message_modify_request(_queue,message):
    """Create StreamQueueMessageRequest for modify"""
    return StreamQueueMessagesRequest(
        ClientID=_queue.ClientID,
        Channel="",
        RequestID=get_next_id(),
        StreamRequestTypeData=StreamRequestType.SendModifiedMessage,
        VisibilitySeconds=_queue.convert_to_queue_message(message),
        WaitTimeSeconds=0,
        ModifiedMessage= None,
        RefSequence=0
    )