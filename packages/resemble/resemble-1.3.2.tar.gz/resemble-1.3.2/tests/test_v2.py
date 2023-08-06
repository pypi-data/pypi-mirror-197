import os
import unittest
from resemble import Resemble

def _get_test_voice_uuid():
  voice_uuid = os.environ.get('TEST_VOICE_UUID')
  if not voice_uuid:
    raise Exception('Invalid voice_uuid provided; please set the TEST_VOICE_UUID environment variable')
  return voice_uuid

def _get_test_callback_uri():
  callback_uri = os.environ.get('TEST_CALLBACK_URI')
  if not callback_uri:
    raise Exception('Invalid callback_uri provided; please set the TEST_CALLBACK_URI environment variable')
  return callback_uri

class TestResembleV2API(unittest.TestCase):
  def setUp(self):
    if os.environ.get('TEST_BASE_URL'):
      Resemble.base_url(os.environ.get('TEST_BASE_URL'))
    if os.environ.get('TEST_API_KEY'):
      Resemble.api_key(os.environ.get('TEST_API_KEY'))
    if os.environ.get('TEST_SYN_SERVER_URL'):
      Resemble.syn_server_url(os.environ.get('TEST_SYN_SERVER_URL'))
    else:
      raise Exception('No API key set; please set the TEST_API_KEY environment variable')
    
    return super().setUp()

  def test_v2_projects(self):
    projects = Resemble.v2.projects.all(1)
    self.assertTrue(projects['success'])
    project = Resemble.v2.projects.create('Test Project', 'Test Description')
    self.assertTrue(project['success'])
    updated_project = Resemble.v2.projects.update(project['item']['uuid'], 'Updated Project Title', 'Updated Description')
    self.assertTrue(updated_project['success'])
    fetched_project = Resemble.v2.projects.get(project['item']['uuid'])
    self.assertTrue(fetched_project['success'])
    delete_op = Resemble.v2.projects.delete(project['item']['uuid'])
    self.assertTrue(delete_op['success'])

  def test_v2_clips(self):
    project = Resemble.v2.projects.create('Test Project', 'Test Description')
    project_uuid = project['item']['uuid']
    
    clips = Resemble.v2.clips.all(project_uuid, 1)
    self.assertTrue(clips['success'])
    
    sync_clip = Resemble.v2.clips.create_sync(project_uuid, _get_test_voice_uuid(), 'This is a test')
    self.assertTrue(sync_clip['success'])

    async_clip = Resemble.v2.clips.create_async(project_uuid, _get_test_voice_uuid(), _get_test_callback_uri(), 'This is a test')
    self.assertTrue(async_clip['success'])

    for chunk in Resemble.v2.clips.stream(project_uuid, _get_test_voice_uuid(), 'This is a test'):
      self.assertIsNotNone(chunk)

    update_async_clip = Resemble.v2.clips.update_async(project_uuid, sync_clip['item']['uuid'], _get_test_voice_uuid(), _get_test_callback_uri(), 'This is another test')
    self.assertTrue(update_async_clip['success'])

    clip = Resemble.v2.clips.get(project_uuid, sync_clip['item']['uuid'])
    self.assertTrue(clip['success'])

    delete_op = Resemble.v2.clips.delete(project_uuid, clip['item']['uuid'])
    self.assertTrue(delete_op['success'])

  def test_v2_voices(self):
    voices = Resemble.v2.voices.all(1)
    self.assertTrue(voices['success'])
    voice = Resemble.v2.voices.create('Test Voice')
    self.assertTrue(voice['success'])
    updated_voice = Resemble.v2.voices.update(voice['item']['uuid'], 'NewVoiceName')
    self.assertTrue(updated_voice['success'])
    fetched_voice = Resemble.v2.voices.get(voice['item']['uuid'])
    self.assertTrue(fetched_voice['success'])
    delete_op = Resemble.v2.voices.delete(voice['item']['uuid'])
    self.assertTrue(delete_op['success'])

  def test_v2_recordings(self):
    voice = Resemble.v2.voices.create('Test Voice')
    voice_uuid = voice['item']['uuid']
    
    recordings = Resemble.v2.recordings.all(voice_uuid, 1)
    self.assertTrue(recordings['success'])
    recording = None
    with open("tests/spec_sample_audio.wav", 'rb') as file:
      recording = Resemble.v2.recordings.create(voice_uuid, file, 'Test recording', 'transcription', True, 'neutral')
      self.assertTrue(recording['success'])
    updated_recording = Resemble.v2.recordings.update(voice_uuid, recording['item']['uuid'], 'New name', 'new transcription', True, 'neutral')
    self.assertTrue(updated_recording['success'])
    fetched_recording = Resemble.v2.recordings.get(voice_uuid, recording['item']['uuid'])
    self.assertTrue(fetched_recording['success'])
    delete_op = Resemble.v2.recordings.delete(voice_uuid, recording['item']['uuid'])
    self.assertTrue(delete_op['success'])

if __name__ == '__main__':
    unittest.main()
