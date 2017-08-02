import datetime
import logging
import time

import PureCloudPlatformClientV2

# Local reference for recordings API
recApi = PureCloudPlatformClientV2.apis.RecordingApi()

#TODO: Documentation

def deleteInteractionRecordings(conversationIds, deleteDate=None):
    # If not specified, delete immediately
    # Time does not actually matter and is discarded by the system
    if deleteDate is None:
        deleteDate = datetime.datetime.utcnow()
    # Create a recording object to patch the recordings with new delete dates
    # TODO: Move out of function?
    deleteRecordingRecord = PureCloudPlatformClientV2.Recording()
    deleteRecordingRecord.delete_date = deleteDate
    for conversationId in conversationIds:
        time.sleep(2)
        try:
            recordings = recApi.get_conversation_recordings(conversationId)
        except PureCloudPlatformClientV2.rest.ApiException:
            logging.info('%s NO RECORDING FOUND', conversationId)
            continue
        if len(recordings) == 0:
            logging.info('%s NO RECORDING FOUND', conversationId)
            continue
        if recordings[0].file_state == 'DELETED':
            logging.info('%s ALREADY DELETED', conversationId)
            continue
        for rec in recordings:
            response = recApi.put_conversation_recording(
                conversationId,rec.id,deleteRecordingRecord)
            logging.info('%s DELETION SET %s',
                         conversationId, response.delete_date.date().isoformat())
        