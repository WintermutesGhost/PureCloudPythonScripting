import datetime
import logging

import PureCloudPlatformClientV2

# Local reference for recordings API
recApi = PureCloudPlatformClientV2.apis.RecordingApi()

#TODO: Documentation

def deleteInteractionRecordings(conversationId, deleteDate=None):
    # If not specified, delete immediately
    # Time does not actually matter and is discarded by the system
    if deleteDate is None:
        deleteDate = datetime.datetime.utcnow()
    # Create a recording object to patch the recordings with new delete dates
    # TODO: Move out of function?
    deleteRecordingRecord = PureCloudPlatformClientV2.Recording()
    deleteRecordingRecord.delete_date = deleteDate
    recordings = recApi.get_conversation_recordings(conversationId)
    for rec in recordings:
        response = recApi.put_conversation_recording(
            conversationId,rec.id,deleteRecordingRecord)
        logging.info('%s DELETION SET %s',
                     conversationId, response.delete_date.date().isoformat())
        